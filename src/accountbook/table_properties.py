from enum import Enum


class ColRawData:
    YEAR = "year"
    MONTH = "month"
    NOTE = "note"
    VALUE = "eur"
    ACCOUNT = "category"
    TAGS = [
        "is_salary",
        "is_deposit",
        "is_direct_debit",
    ]


class Month(Enum):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12
