from accountbook.account import Account
from accountbook.budget import Budget, Month
from accountbook.gbq import Table
from constant.table import ColRawData
from config import config_table
from typing import List
import pandas as pd


def update_account_balance(account: Account, raw_data: Table) -> None:
    account.balance = raw_data.data[ColRawData.VALUE].sum()


def budget_plan(budget: Budget) -> pd.Series:
    data = budget.load()
    d = data["profile"]
    for year in data["deposit"]:
        d_year = data["deposit"][year]
        d_year = {f"{year}-{month}": sum(deposit) for month, deposit in d_year.items()}
        d.update(d_year)
    return pd.Series(d)


def budget_expense(budget: Budget, gbq_table: Table) -> pd.Series:
    """gbq_table is on an account-level.
    An account holds balance, an expense belongs to a budget (category).

    Args:
        budget (Budget): _description_
        gbq_table (Table): _description_

    Returns:
        pd.Series: _description_
    """
    profile = budget.load()["profile"]
    df = gbq_table.data[config_table["budget_summary"]["columns"]]
    df = df.loc[df[ColRawData.BUDGET] == budget.budget_category]
    df[ColRawData.MONTH] = df[ColRawData.MONTH].apply(lambda m: Month(m).name)
    df["year_month"] = df[ColRawData.YEAR].astype(str) + "-" + df[ColRawData.MONTH]
    df = df[["year_month", ColRawData.VALUE]].groupby("year_month", sort=False).sum()
    df[ColRawData.VALUE] = df[ColRawData.VALUE].cumsum()
    series = pd.concat([pd.Series(profile), -df[ColRawData.VALUE]])
    return series


def account_stats(account: Account, raw_data: Table) -> pd.Series:
    data = account.load()
    data["profile"]

    raw_data.groupby()
    # for year in data["deposit"]:
    #     d_year = data["deposit"][year]
    #     d_year = {f"{year}-{month}": sum(deposit) for month, deposit in d_year.items()}
    #     d.update(d_year)
    # return pd.Series(d)


def generate_budget_summary(budgets: List[Budget]):
    df = pd.DataFrame([budget_plan(budget) for budget in budgets])
    df = df.set_index(config_table["budget_summary"]["header"])
    return df.T


def generate_account_summary(accounts: List[Account]):
    ...


def init_account_files(transaction_table: Table, year: int = 2023) -> None:
    df = transaction_table.load_data()
    df_default = df.loc[(df.year == year) & (df.month == 0)]
    dict_balance = (
        df[[ColRawData.ACCOUNT, ColRawData.VALUE]]
        .groupby(ColRawData.ACCOUNT)[ColRawData.VALUE]
        .sum()
        .round(2)
        .to_dict()
    )
    for _, r in df_default.iterrows():
        account_id = r[ColRawData.ACCOUNT]
        owner, bank, vault = account_id.split("-")
        default_balance = r[ColRawData.VALUE]
        description = r[ColRawData.DESCRIPTION]
        Account(
            owner,
            bank,
            vault,
            default_balance,
            balance=dict_balance[account_id],
            description=description,
        )


def main():
    t = Table("data", "transactions")
    init_account_files(transaction_table=t)


if __name__ == "__main__":
    main()
