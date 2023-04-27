from accountbook.account import Account
from accountbook.gbq import Table
from constant.table import ColRawData
from typing import List
import pandas as pd
from config import CHECKPOINTS


def snapshot_transactions(
    transactions: Table, year: int = None, month: int = None
) -> None:
    conditions = []
    sort = {
        ColRawData.YEAR: "asc",
        ColRawData.MONTH: "asc",
        ColRawData.DAY: "asc",
        ColRawData.ACCOUNT_ID: "asc",
        ColRawData.BUDGET_ID: "asc",
    }
    filename = "transactions"
    if year:
        conditions.append(f"{ColRawData.YEAR} = {year}")
        filename += f"_{year}"
    if month:
        conditions.append(f"{ColRawData.MONTH} = {month}")
        filename += f"_{month}"
    df = transactions.load_data(conditions=conditions, sort=sort)
    CHECKPOINTS.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CHECKPOINTS / f"{filename}.parquet", index=False)


def init_account_files(transactions: Table, year: int = 2023) -> None:
    df_default = transactions.load_data(
        conditions=[f"{ColRawData.YEAR} = {year}", f"{ColRawData.MONTH} = 0"]
    )

    for _, r in df_default.iterrows():
        owner, bank, vault = r[ColRawData.ACCOUNT_ID].split("-")
        default_balance = r[ColRawData.VALUE]
        description = r[ColRawData.DESCRIPTION]
        account = Account(
            owner=owner,
            bank=bank,
            vault=vault,
            default_balance=default_balance,
            balance=default_balance,
            description=description,
        )
        yield account


def update_accounts_balance(accounts: List[Account], transactions: Table) -> None:
    df = transactions.load_data()
    dict_balance = (
        df.groupby(ColRawData.ACCOUNT_ID)[ColRawData.VALUE].sum().round(2).to_dict()
    )
    for account in accounts:
        account.balance = dict_balance[account.id]


def has_tag(df: pd.DataFrame, tag: str) -> pd.Series[bool]:
    return df.tags.apply(lambda string: tag in string.split(", "))


def main():
    # options = {"skip_leading_rows": 1}

    t = Table("data", "transactions")
    # t.handler.create_or_update_tables_from_file(
    #     dataset_name="data",
    #     sheet_name="kuan-wu-accountbook",
    #     schema_path=SCHEMA / "kuan-wu.json",
    #     **options,
    # )

    accounts = init_account_files(transactions=t)
    update_accounts_balance(accounts, t)


if __name__ == "__main__":
    main()
