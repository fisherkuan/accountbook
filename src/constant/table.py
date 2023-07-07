from enum import StrEnum, auto
from dataclasses import dataclass, field
from typing import Literal


class TransactionField(StrEnum):
    YEAR = auto()
    MONTH = auto()
    DAY = auto()
    VALUE = "eur"
    ACCOUNT_ID = auto()
    BUDGET_ID = auto()
    DESCRIPTION = auto()
    TAG_SALARY = auto()
    TAG_DEPOSIT = auto()
    TAG_DIRECT_DEBIT = auto()

    @property
    def tags(self):
        return [name[4:] for name in TransactionField.__members__ if name.startswith("TAG_")]


class Order(StrEnum):
    ASC = auto()
    DESC = auto()


@dataclass
class SchemaTransactionField:
    name: TransactionField
    type: Literal["string", "int64", "float64", "boolean"]
    mode: Literal["nullable", "required", "repeated"] = "nullable"
    transform: str | None = field(default=None, repr=False, kw_only=True)


transaction_schema = [
    SchemaTransactionField(TransactionField.YEAR, "int64", "required"),
    SchemaTransactionField(TransactionField.MONTH, "int64", "required"),
    SchemaTransactionField(TransactionField.DAY, "int64", "required"),
    SchemaTransactionField(TransactionField.VALUE, "int64", "required", transform="CAST((-eur * 100) AS INT64)"),
    SchemaTransactionField(TransactionField.ACCOUNT_ID, "string", "required"),
    SchemaTransactionField(TransactionField.BUDGET_ID, "string", "required"),
    SchemaTransactionField(TransactionField.DESCRIPTION, "string", "nullable"),
    SchemaTransactionField(TransactionField.TAG_SALARY, "boolean", "nullable"),
    SchemaTransactionField(TransactionField.TAG_DEPOSIT, "boolean", "nullable"),
    SchemaTransactionField(TransactionField.TAG_DIRECT_DEBIT, "boolean", "nullable"),
]
