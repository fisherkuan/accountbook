from pathlib import Path

SECRETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/secrets")
SCHEMA = Path("/Users/fisherkuan/Projects/fisher/accountbook/schema")
ACCOUNTS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/accounts")
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
