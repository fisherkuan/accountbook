from dataclasses import dataclass, field
import config
from constant.component import AccountId, Owner, Bank, Vault

import pandas as pd
import numpy as np


@dataclass
class Account:
    id: str | AccountId = field(repr=False, default=None)
    owner: Owner = field(kw_only=True, default=None)
    bank: Bank = field(kw_only=True, default=None)
    vault: Vault = field(kw_only=True, default=None)

    def __post_init__(self) -> None:
        if self.id is not None:
            self.owner, self.bank, self.vault = self.id.split("-")

        self.id = f"{self.owner}-{self.bank}-{self.vault}"
        self.metadata = self.load_metadata()

    @property
    def balance(self):
        assert hasattr(self, "_balance"), AttributeError("Balance has not been defined yet.")
        return self._balance

    @balance.setter
    def balance(self, new_value: float):
        assert isinstance(new_value, (float, int)), TypeError(
            f"Balance must be numeric. Got {type(new_value)} instead."
        )
        self._balance = round(float(new_value), 2)

    def load_metadata(self) -> dict:
        df = pd.read_csv(config.DATA / "account-metadata.csv").replace(np.nan, None)
        try:
            metadata = df[df["account_id"] == self.id].to_dict(orient="records")[0]
        except IndexError:
            raise ValueError(f"Account {self.id} does not exist.")

        for col in config.METADATA_LIST_COLUMNS:
            if metadata[col] is None:
                metadata[col] = []
            else:
                metadata[col] = metadata[col].split(";")
        return metadata


def main():
    a = Account(AccountId.TEST)
    print(f"{a=}")
    a.balance = 150
    print(f"{a.balance=}")
    print(f"{a.metadata=}")

    b = Account(owner=Owner.FISHER, bank=Bank.KBC, vault=Vault.CREDIT_CARD)
    print(f"{b=}")


if __name__ == "__main__":
    main()
