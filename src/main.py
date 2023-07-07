from accountbook.gbq import Table
import pandas as pd
from config import SCHEMA


def has_tag(df: pd.DataFrame, tag: str) -> "pd.Series[bool]":
    return df.tags.apply(lambda string: tag in string.split(", "))


def balance_sheet_by_month(transactions: pd.DataFrame) -> pd.DataFrame:
    ...


def main():
    options = {"skip_leading_rows": 1}

    t = Table("data", "transactions")
    t.handler.create_or_update_tables_from_file(
        dataset_name="data",
        sheet_name="kuan-wu-accountbook",
        schema_path=SCHEMA / "kuan-wu.json",
        **options,
    )


if __name__ == "__main__":
    main()
