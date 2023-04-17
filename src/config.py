from pathlib import Path

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
    ]
}

config_budget = {
    "profile_attributes": [
        "description",
        "owner",
        "budget_category",
    ]
}
