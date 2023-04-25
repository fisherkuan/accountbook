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
    DEBIT_CARD = "debit_card"
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
    TEST = f"{Owner.TEST}-{BudgetCategory.TEST}"

    FISHER_SALARY = f"{Owner.FISHER}-{BudgetCategory.SALARY}"
    FISHER_PERSONAL = f"{Owner.FISHER}-{BudgetCategory.PERSONAL}"
    FISHER_TWD = f"{Owner.FISHER}-{BudgetCategory.TWD}"
    FISHER_PENSION = f"{Owner.FISHER}-{BudgetCategory.PENSION}"
    FISHER_OTHERS = f"{Owner.FISHER}-{BudgetCategory.OTHERS}"

    RUHAN_SALARY = f"{Owner.RUHAN}-{BudgetCategory.SALARY}"
    RUHAN_PERSONAL = f"{Owner.RUHAN}-{BudgetCategory.PERSONAL}"
    RUHAN_TWD = f"{Owner.RUHAN}-{BudgetCategory.TWD}"
    RUHAN_PENSION = f"{Owner.RUHAN}-{BudgetCategory.PENSION}"
    RUHAN_OTHERS = f"{Owner.RUHAN}-{BudgetCategory.OTHERS}"

    SHARED_SHARED = f"{Owner.SHARED}-{BudgetCategory.SHARED}"
    SHARED_HOMELOAN = f"{Owner.SHARED}-{BudgetCategory.HOMELOAN}"
    SHARED_STOCK = f"{Owner.SHARED}-{BudgetCategory.STOCK}"
    SHARED_CRYPTO = f"{Owner.SHARED}-{BudgetCategory.CRYPTO}"
    SHARED_TRAVEL = f"{Owner.SHARED}-{BudgetCategory.TRAVEL}"
    SHARED_E0 = f"{Owner.SHARED}-{BudgetCategory.E0}"
    SHARED_OTHERS = f"{Owner.SHARED}-{BudgetCategory.OTHERS}"

    @classmethod
    def all(cls):
        return [attr.value for attr in list(cls)]


class AccountEnum(Enum):
    TEST = f"{Owner.TEST}-{Bank.TEST}-{Vault.TEST}"

    FISHER_KBC_BASIC = f"{Owner.FISHER}-{Bank.KBC}-{Vault.BASIC}"
    FISHER_KBC_TWD = f"{Owner.FISHER}-{Bank.KBC}-{Vault.TWD}"
    FISHER_REVOLUT_BASIC = f"{Owner.FISHER}-{Bank.REVOLUT}-{Vault.BASIC}"
    FISHER_REVOLUT_PRO = f"{Owner.FISHER}-{Bank.REVOLUT}-{Vault.PRO}"

    RUHAN_KBC_BASIC = f"{Owner.RUHAN}-{Bank.KBC}-{Vault.BASIC}"
    RUHAN_KBC_TWD = f"{Owner.RUHAN}-{Bank.KBC}-{Vault.TWD}"
    RUHAN_REVOLUT_BASIC = f"{Owner.RUHAN}-{Bank.REVOLUT}-{Vault.BASIC}"

    SHARED_KBC_BASIC = f"{Owner.SHARED}-{Bank.KBC}-{Vault.BASIC}"
    SHARED_KBC_CARD = f"{Owner.SHARED}-{Bank.KBC}-{Vault.CREDIT_CARD}"
    SHARED_KBC_E0 = f"{Owner.SHARED}-{Bank.KBC}-{Vault.E0}"
    SHARED_REVOLUT_TRAVEL = f"{Owner.SHARED}-{Bank.REVOLUT}-{Vault.TRAVEL}"
    SHARED_CRYPTO_CARD = f"{Owner.SHARED}-{Bank.CRYPTO_COM}-{Vault.DEBIT_CARD}"
    SHARED_CRYPTO_BASIC = f"{Owner.SHARED}-{Bank.CRYPTO_COM}-{Vault.BASIC}"
    SHARED_DEGIRO_BASIC = f"{Owner.SHARED}-{Bank.DEGIRO}-{Vault.BASIC}"

    @classmethod
    def all(cls):
        return [attr.value for attr in list(cls)]
