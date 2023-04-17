from accountbook.account import Account
from accountbook.gbq import Table
from constant.table import ColRawData
from config import ACCOUNTS
from typing import List


def update_account_balance(account: Account, raw_data: Table) -> None:
    account.balance = raw_data.data[ColRawData.VALUE].sum()


def summarize_budget(account: Account):
    ...


def generate_budget_summary(accounts: List[Account]):
    ...


def generate_account_summary(accounts: List[Account]):
    ...


def main():
    # account = Account(
    #     owner="Fisher",
    #     bank="KBC",
    #     product="Basic",
    #     default_balance=645.38,
    #     balance=920.71,
    #     description="default personal account"
    # )
    # account.take_snapshot(label="2023-04-14")
    account = Account.from_file(ACCOUNTS / "Fisher-KBC-Basic.json")
    print(account)
    print(vars(account))


if __name__ == "__main__":
    main()
