from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field, InitVar
from datetime import datetime
import json
from pathlib import Path


class AccountBookABC(ABC):
    ...


@dataclass(kw_only=True)
class AccountBookMemberABC(ABC):
    id: str = field(init=False)
    _config: dict = field(repr=False)
    description: str = None
    init: InitVar[bool] = False

    def __post_init__(self, init) -> None:
        assert hasattr(self, "id"), AttributeError("id must be defined.")
        assert hasattr(self, "file_path"), AttributeError("file_path must be defined.")
        assert isinstance(self.file_path, Path), TypeError(
            "file_path must be a pathlib.Path object."
        )
        if init and not self.file_path.exists():
            self.initiate_file()

    @property
    def initialized(self) -> bool:
        return self.file_path.exists()

    def load_file(self) -> None:
        with open(self.file_path) as file:
            return json.load(file)

    def update_profile(self, **kwargs) -> None:
        with open(self.file_path) as file:
            data = json.load(file)
        data["profile"].update(kwargs)
        data["latest_profile_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            print("Updated profile.")

    def take_snapshot(self, label: str = None) -> None:
        assert self.initialized, ValueError(
            "File has not been initialized yet. Try calling 'initiate_file()'."
        )
        with open(self.file_path) as file:

            def fn_defaultdict_list(d):
                return defaultdict(list, d)

            data = json.load(file, object_hook=fn_defaultdict_list)

        snapshot = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for attr in self._config["snapshot_attributes"]:
            if attr in data:
                snapshot[attr] = data[attr]
        if label:
            snapshot["label"] = label
        data["snapshots"].append(snapshot)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    @abstractmethod
    def from_id(id: str, **kwargs) -> AccountBookMemberABC:
        ...

    @abstractmethod
    def initiate_file(self) -> None:
        ...
