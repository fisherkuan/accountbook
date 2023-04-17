from enum import Enum


class Owner:
    FISHER = "fisher"
    RUHAN = "ruhan"
    SHARED = "shared"
    TEST = "test_owner"


class Bank:
    KBC = "kbc"
    REVOLUT = "revolut"
    CRYPTO_COM = "crypto.com"
    DEGIRO = "degiro"
    TEST = "test_bank"


class Vault:
    BASIC = "basic"
    PRO = "pro"
    TWD = "twd"
    TRAVEL = "travel"
    E0 = "e0"
    CREDIT_CARD = "credit_card"
    TEST = "test_vault"


class BudgetCategory:
    SALARY = "salary"
    PERSONAL = "personal"
    SHARED = "shared"
    HOMELOAN = "homeloan"
    STOCK = "stock"
    CRYPTO = "crypto"
    PENSION = "pension"
    TWD = "twd"
    TRAVEL = "travel"
    E0 = "e0"
    OTHERS = "others"
    TEST = "test_budget"


class BudgetEnum(Enum):
    TEST = (Owner.TEST, BudgetCategory.TEST)

    FISHER_SALARY = (Owner.FISHER, BudgetCategory.SALARY)
    FISHER_PERSONAL = (Owner.FISHER, BudgetCategory.PERSONAL)
    FISHER_TWD = (Owner.FISHER, BudgetCategory.TWD)
    FISHER_PENSION = (Owner.FISHER, BudgetCategory.PENSION)
    FISHER_OTHERS = (Owner.FISHER, BudgetCategory.OTHERS)

    RUHAN_SALARY = (Owner.RUHAN, BudgetCategory.SALARY)
    RUHAN_PERSONAL = (Owner.RUHAN, BudgetCategory.PERSONAL)
    RUHAN_TWD = (Owner.RUHAN, BudgetCategory.TWD)
    RUHAN_PENSION = (Owner.RUHAN, BudgetCategory.PENSION)
    RUHAN_OTHERS = (Owner.RUHAN, BudgetCategory.OTHERS)

    SHARED_SHARED = (Owner.SHARED, BudgetCategory.SHARED)
    SHARED_HOMELOAN = (Owner.SHARED, BudgetCategory.HOMELOAN)
    SHARED_STOCK = (Owner.SHARED, BudgetCategory.STOCK)
    SHARED_CRYPTO = (Owner.SHARED, BudgetCategory.CRYPTO)
    SHARED_TRAVEL = (Owner.SHARED, BudgetCategory.TRAVEL)
    SHARED_E0 = (Owner.SHARED, BudgetCategory.E0)
    SHARED_OTHERS = (Owner.SHARED, BudgetCategory.OTHERS)

    @classmethod
    def all(cls):
        return list(cls)


class AccountEnum(Enum):
    TEST = (Owner.TEST, Bank.TEST, Vault.TEST, 0.0)

    FISHER_KBC_BASIC = (Owner.FISHER, Bank.KBC, Vault.BASIC, 1487.67)
    FISHER_KBC_TWD = (Owner.FISHER, Bank.KBC, Vault.TWD, 401.64)
    FISHER_REVOLUT_BASIC = (Owner.FISHER, Bank.REVOLUT, Vault.BASIC, 240.02)
    FISHER_REVOLUT_PRO = (Owner.FISHER, Bank.REVOLUT, Vault.PRO, 0.0)

    RUHAN_KBC_BASIC = (Owner.RUHAN, Bank.KBC, Vault.BASIC, 4237.32)
    RUHAN_KBC_TWD = (Owner.RUHAN, Bank.KBC, Vault.TWD, 0.26)
    RUHAN_REVOLUT_BASIC = (Owner.RUHAN, Bank.REVOLUT, Vault.BASIC, 27.5)

    SHARED_KBC_BASIC = (Owner.SHARED, Bank.KBC, Vault.BASIC, 201.9)
    SHARED_KBC_CARD = (Owner.SHARED, Bank.KBC, Vault.CREDIT_CARD, 0.0)
    SHARED_KBC_E0 = (Owner.SHARED, Bank.KBC, Vault.E0, 0.8)
    SHARED_REVOLUT_TRAVEL = (Owner.SHARED, Bank.REVOLUT, Vault.TRAVEL, 500.0)
    SHARED_CRYPTO_BASIC = (Owner.SHARED, Bank.CRYPTO_COM, Vault.BASIC, 443.48)

    @classmethod
    def all(cls):
        return list(cls)
