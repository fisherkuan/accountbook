from itertools import combinations
from typing import Dict, List, Tuple
from collections import defaultdict


def calculate_balance(transactions: List[Tuple[str, str, float]]) -> Dict[str, float]:
    balance = defaultdict(int)
    for person1, person2, money in transactions:  # Get final balance of each person
        balance[person1] -= money
        balance[person2] += money
    return balance


def optimal_balancing(balance: Dict[str, float]) -> List[Tuple[str, str, float]]:
    def balance_close_group(balance):
        positives = {person: money for person, money in balance.items() if money > 0}
        negatives = {person: money for person, money in balance.items() if money < 0}

        while len(positives) + len(negatives) > 0:
            positive = positives.popitem()
            negative = negatives.popitem()
            new_value = positive[1] + negative[1]
            if new_value > 0:
                positives[positive[0]] = new_value
                yield (negative[0], positive[0], negative[1])
            elif new_value < 0:
                negatives[negative[0]] = new_value
                yield (negative[0], positive[0], positive[1])
            else:
                yield (negative[0], positive[0], positive[1])

    balance = {person: money for person, money in balance.items() if money != 0}
    assert (
        len(balance) > 1
    ), f"Not enough non-zero balances (size={len(balance)}) to optimize."
    assert (
        sum(balance.values()) == 0
    ), "Impossible to balance because the sum of balances is non-zero."

    optimal = []
    for size in range(2, len(balance) + 1):
        if size <= len(balance):
            for group in combinations(balance.keys(), size):  # Get all combinations
                if all(person in balance.keys() for person in group) and (
                    sum(balance[person] for person in group) == 0
                ):  # If they can cancel each others debts
                    optimal += balance_close_group(
                        {person: balance.pop(person) for person in group}
                    )
    return optimal
