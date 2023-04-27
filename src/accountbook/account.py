from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from datetime import datetime
import json
from accountbook.abc import AccountBookMemberABC

from config import ACCOUNTS, config_account
from constant.members import AccountEnum


@dataclass(kw_only=True)
class Account(AccountBookMemberABC):
    owner: str
    bank: str
    vault: str
    _config: dict = field(default_factory=lambda: config_account, repr=False)
    default_balance: float = field(default=None, repr=False)
    init: InitVar[bool] = False

    def __post_init__(self, init) -> None:
        self.id: str = f"{self.owner}-{self.bank}-{self.vault}"
        self.file_path = ACCOUNTS / f"{self.id}.json"
        super().__post_init__(init)

    @property
    def balance(self):
        assert hasattr(self, "_balance"), AttributeError(
            "balance has not been defined yet."
        )
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        assert isinstance(new_value, (float, int)), TypeError(
            "balance must be numeric."
        )
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
    def from_id(id: str, **kwargs) -> Account:
        owner, bank, vault = id.split("-")
        return Account(owner=owner, bank=bank, vault=vault, **kwargs)

    def initiate_file(self) -> None:
        ACCOUNTS.mkdir(parents=True, exist_ok=True)
        assert self.default_balance is not None, ValueError(
            "Default balance must be set with attribute 'default_balance'."
        )
        profile = {
            attr: getattr(self, attr) for attr in self._config["profile_attributes"]
        }
        data = dict(balance=self.default_balance, profile=profile)
        data["latest_balance_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["latest_profile_update"] = data["latest_balance_update"]

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Created a new file {self.file_path}")


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
