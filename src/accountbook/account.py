from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

from config import RECORDS


@dataclass
class Account:
    owner: str
    bank: str
    product: str
    default_balance: float = field(repr=False)
    _balance: float = field(init=False, repr=False)
    balance: float = field(repr=False)
    description: str = None

    def __post_init__(self) -> None:
        file_path = RECORDS / f"{self.owner}-{self.bank}-{self.product}.json"
        if file_path.exists():
            print("File already created.")
        else:
            print(f"Create a new file {file_path}")
            with open(file_path, "w") as file:
                init = dict(properties=vars(self).copy(), records=[])
                init["properties"]["balance"] = init["properties"].pop("_balance")
                json.dump(init, file, indent=4)
        self.file_path = file_path

    @staticmethod
    def from_file(file_path: Path | str) -> Account:
        with open(file_path) as f:
            attributes = json.load(f)["properties"]
        return Account(**attributes)

    def take_snapshot(self, label: str = None) -> None:
        snapshot = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": self.balance,
        }
        if label:
            snapshot["label"] = label
        with open(self.file_path) as file:
            data = json.load(file)
        with open(self.file_path, "w") as file:
            data["records"].append(snapshot)
            json.dump(data, file, indent=4)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        if not isinstance(new_value, (float, int)):
            raise TypeError("Balance is numeric.")
        self._balance = float(new_value)

        file_path = RECORDS / f"{self.owner}-{self.bank}-{self.product}.json"
        if file_path.exists():
            with open(file_path) as file:
                data = json.load(file)
            with open(file_path, "w") as file:
                data["properties"]["balance"] = new_value
                json.dump(data, file, indent=4)


def main():
    a = Account(
        owner="fisher",
        bank="bank_test",
        product="card_test",
        balance=100,
        default_balance=50,
    )
    print(f"{a=}")
    a.balance = 150
    print(f"{a=}")
    a.take_snapshot()
    a.balance = 200
    a.take_snapshot(label="Xmas")

    b = Account.from_file(a.file_path)
    print(f"{b=}")
    b.take_snapshot()


if __name__ == "__main__":
    main()
