from itertools import combinations
from collections import defaultdict
import pandas as pd
import config

from accountbook.helper import has_tag, budget_master_account, load_metadata


def calculate_balance(transactions: list[tuple[str, str, float]]) -> dict[str, float]:
    balance = defaultdict(int)
    for person1, person2, money in transactions:
        balance[person1] += money
        balance[person2] -= money
    return balance


def optimal_reimburse(balance: dict[str, float]) -> list[tuple[str, str, float]]:
    def balance_close_group(balance):
        positives = {person: money for person, money in balance.items() if money > 0}
        negatives = {person: money for person, money in balance.items() if money < 0}

        while len(positives) + len(negatives) > 0:
            positive = positives.popitem()
            negative = negatives.popitem()
            new_value = round(positive[1] + negative[1], 2)
            if new_value > 0:
                positives[positive[0]] = new_value
                yield (negative[0], positive[0], -negative[1])
            elif new_value < 0:
                negatives[negative[0]] = new_value
                yield (negative[0], positive[0], positive[1])
            else:
                yield (negative[0], positive[0], positive[1])

    balance = {person: money for person, money in balance.items() if money != 0}
    assert len(balance) > 1, f"Not enough non-zero balances (size={len(balance)}) to optimize."
    assert sum(balance.values()) == 0, "Impossible to balance because the sum of balances is non-zero."

    optimal = []
    for size in range(2, len(balance) + 1):
        if size <= len(balance):
            for group in combinations(balance.keys(), size):
                if all(person in balance.keys() for person in group) and (
                    sum(balance[person] for person in group) == 0
                ):
                    optimal += balance_close_group({person: balance.pop(person) for person in group})
    return optimal


def main(transactions: pd.DataFrame) -> list[tuple[str, str, int]]:
    df = transactions.copy()
    metadata = load_metadata(config.DATA / "metadata.csv")
    df = df.loc[(df.apply(lambda x: x["budget_id"] not in x["associate_budgets"], axis=1)) & ~has_tag(df, "deposit")]
    df["master_account_of_budget"] = df["budget_id"].map(budget_master_account(metadata))
    balance = df.groupby(["master_account_of_budget", "master_account"])["eur"].sum()
    balance = balance.where(balance != 0).dropna()
    trans = [(index[0], index[1], value) for index, value in zip(balance.index, balance.values)]
    return optimal_reimburse(calculate_balance(trans))
