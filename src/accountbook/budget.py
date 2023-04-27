from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from datetime import datetime
from accountbook.abc import AccountBookMemberABC
from accountbook.helper import nested_defaultdict
from collections import defaultdict
import json

from enum import Enum
from constant.members import BudgetEnum
from config import BUDGETS, config_budget


class Month(Enum):
    DEFAULT = 0
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


@dataclass
class Budget(AccountBookMemberABC):
    owner: str
    budget_category: str
    _config: dict = field(default_factory=lambda: config_budget, repr=False)
    init: InitVar[bool] = False

    def __post_init__(self, init) -> None:
        self.id: str = f"{self.owner}-{self.budget_category}"
        self.file_path = BUDGETS / f"{self.id}.json"
        super().__post_init__(init)

    @staticmethod
    def from_id(id: str, **kwargs) -> Budget:
        owner, budget_category = id.split("-")
        return Budget(owner=owner, budget_category=budget_category, **kwargs)

    def initiate_file(self) -> None:
        BUDGETS.mkdir(parents=True, exist_ok=True)
        profile = {
            attr: getattr(self, attr) for attr in config_budget["profile_attributes"]
        }
        data = dict(profile=profile)
        data["latest_profile_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Created a new file {self.file_path}")

    # TODO: review this method
    def add(self, month: Month, budget: float, year: int | str = 2023) -> None:
        def _fn_nested_defaultdict_object_hook(d):
            return defaultdict(nested_defaultdict, d)

        with open(self.file_path) as file:
            data = json.load(file, object_hook=_fn_nested_defaultdict_object_hook)

        year = str(year)
        if not data["deposit"][year][month.name]:
            data["deposit"][year][month.name] = [budget]
        else:
            data["deposit"][year][month.name].append(budget)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Budget {budget} added to {year}-{month.name}.")

    # TODO: review this method
    def remove(self, month: Month, budget: float, year: int | str = 2023) -> None:
        with open(self.file_path) as file:
            data = json.load(
                file, object_hook=Budget._fn_nested_defaultdict_object_hook
            )

        year = str(year)
        if (
            not data["deposit"][year][month.name]
            or budget not in data["deposit"][year][month.name]
        ):
            raise ValueError(f"Budget {budget} not found.")
        data["deposit"][year][month.name].remove(budget)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Budget {budget} removed from {year}-{month.name}.")

    def update(
        self, month: Month, as_is: float, to_be: float, year: int = 2023
    ) -> None:
        self.remove(year=year, month=month, budget=as_is)
        self.add(year=year, month=month, budget=to_be)


def main():
    b = Budget(*BudgetEnum.TEST.value)
    b.add(month=Month(1), budget=1000)
    b.add(month=Month(1), budget=1000)
    b.update(month=Month(1), as_is=1000, to_be=1500)
    try:
        b.update(month=Month(1), as_is=5000, to_be=1500)
    except ValueError:
        print("ValueError caught!")


if __name__ == "__main__":
    main()
