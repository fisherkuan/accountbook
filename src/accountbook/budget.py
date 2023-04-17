from dataclasses import dataclass
from helper import nested_defaultdict
from collections import defaultdict
import json

from enum import Enum
from constant.members import BudgetEnum
from config import BUDGETS, config_budget


class Month(Enum):
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
class Budget:
    owner: str
    budget_category: str
    description: str = None

    def __post_init__(self) -> None:
        self.id: str = f"{self.owner}-{self.budget_category}"
        self.file_path = BUDGETS / f"{self.id}.json"
        if not self.file_path.exists():
            self.initiate_file()

    @staticmethod
    def _fn_nested_defaultdict_object_hook(d):
        return defaultdict(nested_defaultdict, d)

    def initiate_file(self) -> None:
        profile_attributes = config_budget["profile_attributes"]
        profile = {attr: getattr(self, attr) for attr in profile_attributes}
        with open(self.file_path, "w") as file:
            json.dump(dict(profile=profile), file, indent=4)
        print(f"Created a new file {self.file_path}")

    def add(self, month: Month, budget: float, year: int | str = 2023) -> None:
        with open(self.file_path) as file:
            data = json.load(
                file, object_hook=Budget._fn_nested_defaultdict_object_hook
            )

        year = str(year)
        if not data["deposit"][year][month.name]:
            data["deposit"][year][month.name] = [budget]
        else:
            data["deposit"][year][month.name].append(budget)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Budget {budget} added to {year}-{month.name}.")

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
