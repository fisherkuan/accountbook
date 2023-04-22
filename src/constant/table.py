from typing import Callable


class BaseConstant:
    def keys():
        return [
            attr
            for attr in vars(ColRawData)
            if not attr.startswith("__")
            and not isinstance(getattr(ColRawData, attr), Callable)
        ]

    def values():
        return [getattr(ColRawData, attr) for attr in ColRawData.keys()]

    def items():
        return dict(zip(ColRawData.keys(), ColRawData.values()))


class ColRawData(BaseConstant):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    VALUE = "eur"
    ACCOUNT_ID = "account"
    BUDGET_ID = "budget_category"
    DESCRIPTION = "description"
    TAGS = [
        "salary",
        "deposit",
        "direct_debit",
    ]
