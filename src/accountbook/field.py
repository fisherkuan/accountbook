from dataclasses import dataclass
from datetime import datetime
import json

from config import RECORDS


@dataclass
class Field:
    name: str
    owner: str
    default_balance: float
    description: str = None

    def __post_init__(self):
        self.default_balance = self.balance
        self.file_path = RECORDS / f"{self.owner}-{self.bank}-{self.product}.json"

    def take_snapshot(self):
        snapshot = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": self.balance,
        }

        if not self.file_path.exists():
            print(f"File not found. Create a new file {self.file_path}")
            with open(self.file_path, "w") as f:
                json.dump([snapshot], f, indent=4)
                return

        with open(self.file_path) as f:
            snapshots = json.load(f)
            snapshots.append(snapshot)
        with open(self.file_path, "w") as f:
            json.dump(snapshots, f, indent=4)


def main():
    pass


if __name__ == "__main__":
    main()
