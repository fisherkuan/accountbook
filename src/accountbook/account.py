from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import json

from config import ACCOUNTS, config_account
from constant.members import AccountEnum


@dataclass
class Account:
    owner: str
    bank: str
    vault: str
    default_balance: float = field(repr=False)
    id: str = field(init=False)
    _balance: float = field(init=False, repr=False)
    balance: float
    description: str = None

    def __post_init__(self) -> None:
        self.id: str = f"{self.owner}-{self.bank}-{self.vault}"
        self.file_path = ACCOUNTS / f"{self.id}.json"
        if not self.file_path.exists():
            self.initiate_file()

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        if not isinstance(new_value, (float, int)):
            raise TypeError("Balance is numeric.")
        self._balance = float(new_value)

        file_path = ACCOUNTS / f"{self.owner}-{self.bank}-{self.vault}.json"
        if file_path.exists():
            with open(file_path) as file:
                data = json.load(file)
            with open(file_path, "w") as file:
                data["profile"]["balance"] = new_value
                json.dump(data, file, indent=4)

    @staticmethod
    def from_file(file_path: Path | str) -> Account:
        with open(file_path) as f:
            attributes = json.load(f)["profile"]
        return Account(**attributes)

    def initiate_file(self) -> None:
        profile_attributes = config_account["profile_attributes"]
        profile = {attr: getattr(self, attr) for attr in profile_attributes}
        with open(self.file_path, "w") as file:
            json.dump(dict(profile=profile), file, indent=4)
        print(f"Created a new file {self.file_path}")

    def load(self):
        with open(self.file_path) as file:
            return json.load(file)

    def take_snapshot(self, label: str = None) -> None:
        with open(self.file_path) as file:

            def fn_defaultdict_list(d):
                return defaultdict(list, d)

            data = json.load(file, object_hook=fn_defaultdict_list)

        snapshot = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": self.balance,
        }
        if label:
            snapshot["label"] = label
        data["snapshots"].append(snapshot)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)


def main():
    a = Account(*AccountEnum.TEST.value, balance=100)
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
