from pathlib import Path
from constant.table import TransactionField, SchemaTransactionField

# paths
HOME = Path("/Users/fisherkuan/Projects/fisher/accountbook/src")
SECRETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/secrets")
SCHEMA = Path("/Users/fisherkuan/Projects/fisher/accountbook/schema")
DATA = Path("/Users/fisherkuan/Projects/fisher/accountbook/data")

# metadata
METADATA_LIST_COLUMNS = ["associate_budgets", "tags"]
TRANSACTIONS_SCHEMA = [
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

TAGS = ["salary", "deposit", "direct_debit"]
