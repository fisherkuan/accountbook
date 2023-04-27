from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import json

from config import ACCOUNTS, config_account
from constant.members import AccountEnum


@dataclass
class Account:
    owner: str
    bank: str
    vault: str
    id: str = field(init=False)
    description: str = None
    default_balance: float = field(default=None, repr=False)
    init: bool = field(default=False, repr=False)
    _balance: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.id: str = f"{self.owner}-{self.bank}-{self.vault}"
        self.file_path = ACCOUNTS / f"{self.id}.json"
        if self.init and not self.file_path.exists():
            self.initiate_file()

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        assert isinstance(new_value, (float, int)), TypeError("Balance is numeric.")
        self._balance = round(float(new_value), 2)
        if self.file_path and self.file_path.exists():
            with open(self.file_path) as file:
                data = json.load(file)
            with open(self.file_path, "w") as file:
                data["balance"] = self._balance
                data["latest_balance_update"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                print(f"Balance set to {self._balance:.2f}")
                json.dump(data, file, indent=4)

    @staticmethod
    def from_id(account_id: str, **kwargs) -> Account:
        owner, bank, vault = account_id.split("-")
        return Account(owner=owner, bank=bank, vault=vault, **kwargs)

    def initiate_file(self) -> None:
        ACCOUNTS.mkdir(parents=True, exist_ok=True)
        assert self.default_balance is not None, ValueError(
            "Default balance must be set."
        )
        profile = {
            attr: getattr(self, attr) for attr in config_account["profile_attributes"]
        }
        data = dict(balance=self.default_balance, profile=profile)
        data["latest_balance_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["latest_profile_update"] = data["latest_balance_update"]

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Created a new file {self.file_path}")

    def update_profile(self, **kwargs) -> None:
        with open(self.file_path) as file:
            data = json.load(file)
        data["profile"].update(kwargs)
        data["latest_profile_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print("Updated profile.")

    def load(self):
        with open(self.file_path) as file:
            return json.load(file)

    def take_snapshot(self, label: str = None) -> None:
        with open(self.file_path) as file:

            def fn_defaultdict_list(d):
                return defaultdict(list, d)

            data = json.load(file, object_hook=fn_defaultdict_list)

        snapshot = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": data["profile"],
            "balance": data["balance"],
        }
        if label:
            snapshot["label"] = label
        data["snapshots"].append(snapshot)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)


def main():
    a = Account.from_id(AccountEnum.TEST.value)
    a.file_path.unlink(missing_ok=True)
    a.default_balance = 100
    a.description = "Test account"
    a.initiate_file()
    print(f"{a=}")
    a.balance = 150
    a.take_snapshot()
    a.update_profile(description="Test account for testing")
    a.balance = 200
    a.take_snapshot(label="Cheese!")


if __name__ == "__main__":
    main()
