from pathlib import Path
from constant import members

SECRETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/secrets")
SCHEMA = Path("/Users/fisherkuan/Projects/fisher/accountbook/schema")
ACCOUNTS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/accounts")
BUDGETS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/budgets")
CHECKPOINTS = Path("/Users/fisherkuan/Projects/fisher/accountbook/data/checkpoints")
HOME = Path("/Users/fisherkuan/Projects/fisher/accountbook/src")

config_account = {
    "profile_attributes": [
        "description",
        "owner",
        "bank",
        "vault",
        "default_balance",
    ],
    "snapshot_attributes": [
        "profile",
        "balance",
    ],
}

config_budget = {
    "profile_attributes": [
        "description",
        "owner",
        "budget_category",
        "default_budget",
    ],
    "snapshot_attributes": [
        "profile",
        "deposit",
    ],
}

budget_holders = {
    members.BudgetEnum.FISHER_OTHERS: [
        members.AccountEnum.FISHER_KBC_BASIC,
        members.AccountEnum.FISHER_REVOLUT_BASIC,
        members.AccountEnum.FISHER_REVOLUT_PRO,
    ],
    members.BudgetEnum.FISHER_PENSION: [members.AccountEnum.FISHER_KBC_BASIC],
    members.BudgetEnum.FISHER_PERSONAL: [
        members.AccountEnum.FISHER_KBC_BASIC,
        members.AccountEnum.FISHER_REVOLUT_BASIC,
        members.AccountEnum.FISHER_REVOLUT_PRO,
    ],
    members.BudgetEnum.FISHER_SALARY: [members.AccountEnum.FISHER_KBC_BASIC],
    members.BudgetEnum.FISHER_TWD: [members.AccountEnum.FISHER_KBC_TWD],
    members.BudgetEnum.RUHAN_OTHERS: [
        members.AccountEnum.RUHAN_KBC_BASIC,
        members.AccountEnum.RUHAN_REVOLUT_BASIC,
    ],
    members.BudgetEnum.RUHAN_PENSION: [members.AccountEnum.RUHAN_KBC_BASIC],
    members.BudgetEnum.RUHAN_PERSONAL: [
        members.AccountEnum.RUHAN_KBC_BASIC,
        members.AccountEnum.RUHAN_REVOLUT_BASIC,
    ],
    members.BudgetEnum.RUHAN_SALARY: [members.AccountEnum.RUHAN_KBC_BASIC],
    members.BudgetEnum.RUHAN_TWD: [members.AccountEnum.RUHAN_KBC_TWD],
    members.BudgetEnum.SHARED_CRYPTO: [members.AccountEnum.SHARED_CRYPTO_BASIC],
    members.BudgetEnum.SHARED_STOCK: [members.AccountEnum.SHARED_DEGIRO_BASIC],
    members.BudgetEnum.SHARED_SHARED: [
        members.AccountEnum.SHARED_KBC_BASIC,
        members.AccountEnum.SHARED_KBC_CARD,
        members.AccountEnum.SHARED_CRYPTO_CARD,
    ],
    members.BudgetEnum.SHARED_E0: [members.AccountEnum.SHARED_KBC_E0],
    members.BudgetEnum.SHARED_HOMELOAN: [members.AccountEnum.SHARED_KBC_BASIC],
    members.BudgetEnum.SHARED_TRAVEL: [members.AccountEnum.SHARED_REVOLUT_TRAVEL],
    members.BudgetEnum.SHARED_OTHERS: [members.AccountEnum.SHARED_KBC_BASIC],
}
budget_holders = {
    budget.value: [i.value for i in list_acccounts]
    for budget, list_acccounts in budget_holders.items()
}
