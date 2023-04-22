from pathlib import Path
from constant.table import ColRawData

SECRETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/secrets")
SCHEMA = Path("/Users/fisherkuan/Projects/fisher/accountbook/schema")
ACCOUNTS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/accounts")
BUDGETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/budgets")
HOME = Path("/Users/fisherkuan/Projects/fisher/accountbook/src")

config_account = {
    "profile_attributes": [
        "description",
        "owner",
        "bank",
        "vault",
        "default_balance",
        "balance",
        "last_balance_update",
    ]
}

config_budget = {
    "profile_attributes": [
        "description",
        "owner",
        "budget_category",
        "default_budget",
    ]
}

# TODO: remove this
config_table = {
    "budget_summary": {
        "header": [
            "owner",
            "budget_category",
            "default_budget",
        ],
        "columns": [
            ColRawData.YEAR,
            ColRawData.MONTH,
            ColRawData.DAY,
            ColRawData.VALUE,
            ColRawData.BUDGET_ID,
        ],
    }
}
