from itertools import combinations
from collections import defaultdict


def calculate_balance(transactions: list[tuple[str, str, float]]) -> dict[str, float]:
    balance = defaultdict(float)
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


def main():
    transactions = [
        ("A", "B", 100),  # B owes A 100
        ("A", "C", 200),  # C owes A 200
        ("B", "C", 100),  # C owes B 100
        ("B", "D", 100),  # D owes B 100
        ("C", "D", 200),  # D owes C 200
        ("D", "E", 100),  # E owes D 100
    ]

    # Calculate net balance for each person
    print(f"Balance: {calculate_balance(transactions)}")
    # Find optimal way to reimburse
    print(f"Optimal: {optimal_reimburse(calculate_balance(transactions))}")


if __name__ == "__main__":
    main()
