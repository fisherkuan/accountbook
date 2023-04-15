from __future__ import annotations

from dataclasses import dataclass
import json

from account import Account
from table_properties import Month
from account_properties import AccountEnum


@dataclass
class Budget:
    account: Account
    description: str = None

    def __post_init__(self) -> None:
        if not self.account.file_path.exists():
            self.account.initiate_file()

    def add(self, month: Month, budget: float) -> None:
        with open(self.account.file_path) as file:
            data = json.load(file)

        if not data.get("budget"):
            data["budget"] = {}

        if not data["budget"].get(month.name):
            data["budget"][month.name] = [budget]
        else:
            data["budget"][month.name].append(budget)

        with open(self.account.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def remove(self, month: Month, budget: float) -> None:
        with open(self.account.file_path) as file:
            data = json.load(file)

        if (
            not data.get("budget")
            or not data["budget"].get(month.name)
            or budget not in data["budget"][month.name]
        ):
            raise ValueError(f"Budget {budget} not found.")
        data["budget"][month.name].remove(budget)

        with open(self.account.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def update(self, month: Month, as_is: float, to_be: float) -> None:
        self.remove(month=month, budget=as_is)
        self.add(month=month, budget=to_be)


def main():
    a = Account(
        *AccountEnum.TEST.value,
        default_balance=0,
        balance=100,
    )
    b = Budget(account=a)
    b.add(month=Month(1), budget=1000)
    b.add(month=Month(1), budget=1000)
    b.update(month=Month(1), as_is=1000, to_be=1500)
    b.update(month=Month(1), as_is=5000, to_be=1500)


if __name__ == "__main__":
    main()
