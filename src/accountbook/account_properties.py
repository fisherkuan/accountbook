from enum import Enum


class Owner:
    FISHER = "fisher"
    RUHAN = "ruhan"
    SHARED = "shared"
    TEST = "test_owner"


class Bank:
    KBC = "kbc"
    REVOLUT = "revolut"
    REVOLUT_PRO = "revolut_pro"
    CRYPTO_COM = "crypto.com"
    DEGIRO = "degiro"
    TEST = "test_bank"


class Vault:
    GENERAL = "general"
    TWD = "twd"
    TRAVEL = "travel"
    E0 = "e0"
    HOMELOAN = "homeloan"
    PENSION = "pension"
    TEST = "test_vault"


class AccountEnum(Enum):
    TEST = (Owner.TEST, Bank.TEST, Vault.TEST)
    FISHER_KBC_GENERAL = (Owner.FISHER, Bank.KBC, Vault.GENERAL)
    FISHER_KBC_TWD = (Owner.FISHER, Bank.KBC, Vault.TWD)
    FISHER_KBC_PENSION = (Owner.FISHER, Bank.KBC, Vault.PENSION)
    FISHER_REVOLUT_GENERAL = (Owner.FISHER, Bank.REVOLUT, Vault.GENERAL)
    FISHER_REVOLUT_PRO_GENERAL = (Owner.FISHER, Bank.REVOLUT, Vault.GENERAL)

    @classmethod
    def all(cls):
        return list(cls)
