import pandas as pd
from pathlib import Path


def load_metadata(file_path: Path | str) -> pd.DataFrame:
    metadata = pd.read_csv(file_path)

    def string_to_list(x):
        return x.split(";") if x == x else []

    metadata.associate_budgets = metadata.associate_budgets.apply(string_to_list)
    metadata.tags = metadata.tags.apply(string_to_list)
    return metadata


def has_tag(df: pd.DataFrame, tag: str) -> pd.Index:
    return df.tags.apply(lambda x: tag in x)


def account_budgets(metadata: pd.DataFrame) -> dict[str, list[str]]:
    return dict(zip(metadata.account_id, metadata.associate_budgets))


def budget_accounts(metadata: pd.DataFrame) -> dict[str, list[str]]:
    dict_account_budgets = account_budgets(metadata)
    budget_accounts = {}
    for k, v in dict_account_budgets.items():
        for budget in v:
            budget_accounts.setdefault(budget, []).append(k)
    return budget_accounts


def master_accounts(metadata: pd.DataFrame) -> dict[str, list[str]]:
    return metadata.account_id[metadata.master_account == metadata.account_id].to_list()


def budget_master_account(metadata: pd.DataFrame) -> dict[str, str]:
    metadata = metadata[["associate_budgets", "master_account"]].explode("associate_budgets").drop_duplicates().dropna()
    return dict(zip(metadata.associate_budgets, metadata.master_account))
