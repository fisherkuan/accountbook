import pandas as pd
from datetime import date

import config
from accountbook.helper import has_tag, load_metadata
import accountbook.gbq as gbq
from accountbook.balance_optimization import main as optimize_balance


def tags_summary(df: pd.DataFrame, tags: list[str], save: bool = True) -> list[tuple[str, pd.DataFrame]]:
    if save:
        output_dir = config.DATA / "output" / date.today().strftime("%Y-%m-%d")
        output_dir.mkdir(parents=True, exist_ok=True)
    for tag in tags:
        print(f"Processing {tag} summary...")
        df_tag = (
            df.loc[has_tag(df, tag)]
            .groupby(["year", "month", "budget_id"])["eur"]
            .sum()
            .unstack()
            .fillna(0)
            .reset_index()
        )
        if save:
            df_tag.to_csv(output_dir / f"{tag}.csv", index=False)
        yield tag, df_tag


def balance_sheet(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    if save:
        output_dir = config.DATA / "output" / date.today().strftime("%Y-%m-%d")
        output_dir.mkdir(parents=True, exist_ok=True)
    budget = (
        df.loc[(has_tag(df, "deposit")) & (df.apply(lambda r: r["budget_id"] in r["associate_budgets"], axis=1))]
        .groupby(["month", "budget_id"], as_index=False)["eur"]
        .sum()
    )
    expense = df.groupby(["month", "budget_id"], as_index=False)["eur"].sum()
    balance = budget.merge(expense, on=["month", "budget_id"], suffixes=["_plan", "_expense"]).fillna(0)
    if save:
        balance.to_csv(output_dir / "balance_sheet.csv", index=False)
    return balance


def main():
    if config.update_gbq:
        gbq.main()

    df = gbq.Table("data", "transactions").load_data(schema=config.TRANSACTIONS_SCHEMA)
    print("Total transactions:", len(df))

    metadata = load_metadata(config.DATA / "metadata.csv")
    df = df.merge(
        metadata[["account_id", "master_account", "associate_budgets", "active"]], on="account_id", how="left"
    )
    print("Total transactions after merging metadata:", len(df))

    print("Saving tags summary...")
    list(tags_summary(df, [tag for tag in config.TAGS if tag != "deposit"]))

    print("Saving balance sheet...")
    balance_sheet(df)

    print("Optimize balance...")
    print(optimize_balance(df))


if __name__ == "__main__":
    main()
