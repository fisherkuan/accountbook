import json
from pathlib import Path
from typing import List
from dataclasses import dataclass, field

import pandas as pd
import pandas_gbq as pdgbq
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from accountbook.credentials import get_creds
from config import SCHEMA, SECRETS
from constant.table import ColRawData


class GoogleBigQueryHandler:
    def __init__(
        self, project: str = "kuan-wu-accounting", auth_from_service_account_file=False
    ) -> None:
        self.cred = get_creds(auth_from_service_account_file)
        self.client = bigquery.Client(project=project, credentials=self.cred)
        pdgbq.context.credentials = self.cred

    def dataset_exists(self, dataset_id: str) -> bool:
        try:
            self.client.get_dataset(dataset_id)
            return True
        except NotFound:
            return False

    def table_exists(self, table_id: str) -> bool:
        try:
            self.client.get_table(table_id)
            return True
        except NotFound:
            return False

    def create_dataset(self, name: str, location: str = "EU") -> None:
        dataset_id = f"{self.client.project}.{name}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location

        # Send the dataset to the API for creation, with an explicit timeout.
        # Raises google.api_core.exceptions.Conflict if the Dataset already
        # exists within the project.
        dataset = self.client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {self.client.project}.{dataset.dataset_id}")

    def create_table(
        self,
        name: str,
        dataset_id: str,
        schema: List[bigquery.SchemaField],
        external_config: bigquery.ExternalConfig = None,
    ) -> None:
        table_id = f"{dataset_id}.{name}"
        table = bigquery.Table(table_id, schema=schema)
        table.external_data_configuration = external_config
        table = self.client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    def update_table_metadata(
        self,
        table_id: str,
        schema: List[bigquery.SchemaField] = None,
        external_config: bigquery.ExternalConfig = None,
    ) -> None:
        table = bigquery.Table(table_id, schema=schema)
        table.external_data_configuration = external_config
        self.client.update_table(table, ["schema", "external_data_configuration"])
        print(f"Updated table {table.project}.{table.dataset_id}.{table.table_id}")

    def remove_table(self, table_id: str, not_found_ok: bool = True) -> None:
        self.client.delete_table(table_id, not_found_ok)
        print(f"Deleted table {table_id}")

    def generate_external_config(
        self, sheet_url: str, range: str, **options
    ) -> bigquery.ExternalConfig:
        """External configuration defines advanced options when creating an external table like GoogleSheets.

        Args:
            sheet_url (str): Sharing URL of the Google Sheets file
            range (str): Name of the spreadsheet and the range inside it
            **options: Additional configurations

        Returns:
            bigquery.ExternalConfig object
        """
        external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
        external_config.source_uris = [sheet_url]
        external_config.options.range = range
        # example of options: {"skip_leading_rows": 1}
        for option, value in options.items():
            setattr(external_config.options, option, value)
        return external_config

    def get_sheet_url_from_json(
        self, sheet_name: str, json_path: Path = SECRETS / "sheet_urls.json"
    ) -> str:
        with open(json_path) as f:
            sheet_urls = json.load(f)
            sheet_url = sheet_urls.get(sheet_name)
            if not sheet_url:
                raise KeyError(f"URL of {sheet_name=} is not found.")
            return sheet_url

    def get_schema_from_json(
        self, table_name: str, json_path: Path
    ) -> List[bigquery.SchemaField]:
        with open(json_path) as f:
            schema = json.load(f)
            schema = [bigquery.SchemaField(**field) for field in schema[table_name]]
        return schema

    def query(self, query: str) -> pd.DataFrame:
        return pd.read_gbq(query, self.client.project)

    def create_or_update_tables_from_file(
        self, dataset_name: str, sheet_name: str, schema_path: Path, **options
    ) -> None:
        dataset_id = f"{self.client.project}.{dataset_name}"
        if not self.dataset_exists(dataset_id):
            self.create_dataset(name=dataset_name)
        with open(schema_path) as f:
            schemas = json.load(f)
            for table_name, schema in schemas.items():
                schema = [bigquery.SchemaField(**field) for field in schema]
                sheet_url = self.get_sheet_url_from_json(sheet_name=sheet_name)
                external_config = self.generate_external_config(
                    sheet_url, table_name, **options
                )
                table_id = f"{dataset_id}.{table_name}"
                if self.table_exists(table_id):
                    self.update_table_metadata(table_id, schema, external_config)
                else:
                    self.create_table(table_name, dataset_id, schema, external_config)
        print(f"All tables in {dataset_name=} are updated.")


@dataclass
class Table:
    dataset: str
    name: str
    project: str = "kuan-wu-accounting"
    table_id: str = field(init=False, repr=False)
    auth_from_service_account_file: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        self.table_id = f"{self.project}.{self.dataset}.{self.name}"
        self.handler = GoogleBigQueryHandler(
            project=self.project,
            auth_from_service_account_file=self.auth_from_service_account_file,
        )

    def query(self, query) -> pd.DataFrame:
        return self.handler.query(query)

    def _generate_col_string(self) -> str:
        col_all_except_tags = ColRawData.values()[:-1]
        col_tags = [f"tag_{tag}" for tag in ColRawData.TAGS]
        return ", ".join(col_all_except_tags + col_tags)

    def _convert_tags_column(self, df: pd.DataFrame) -> pd.DataFrame:
        col_tags = [col for col in df.columns if col.startswith("tag_")]
        col_out = [col for col in df.columns if not col.startswith("tag_")] + ["tags"]
        for col in col_tags:
            tag = col[4:]
            df[col] = df[col].apply(lambda x: tag if x else None)
        df["tags"] = df[col_tags].values.tolist()
        df["tags"] = df["tags"].apply(
            lambda list_tags: ", ".join(filter(None, list_tags))
        )
        return df[col_out]

    def load_data(self) -> pd.DataFrame:
        data: pd.DataFrame = self.query(
            f"SELECT {self._generate_col_string()} FROM {self.table_id} "
            f"WHERE {ColRawData.VALUE} IS NOT NULL"
        )
        data[ColRawData.VALUE] = -data[ColRawData.VALUE].round(2)
        data = self._convert_tags_column(data)
        return data


def main():
    handler = GoogleBigQueryHandler()
    options = {"skip_leading_rows": 1}
    handler.create_or_update_tables_from_file(
        dataset_name="data",
        sheet_name="kuan-wu-accountbook",
        schema_path=SCHEMA / "kuan-wu.json",
        **options,
    )


if __name__ == "__main__":
    main()
