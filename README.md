# accountbook
The accountbook app takes the raw transactions from Google Sheets ([example](https://docs.google.com/spreadsheets/d/1UmX-s_Pp_5cDsw0i9jq4cbiHqBtZzIiKCik6cQ-0n7o/edit?usp=sharing)) and summarize them in statistics listed below. This app also includes a feature that balance the accounts in the simplest way.

Current statistics includes:
- Monthly deposit and expense for each budget
- Monthly subtotal of each tag for each budget (an output file per tag)

## Terminology
### Account
An account is a **physical** vault that holds money. An account id is in the format of `owner-bank-vault`, for example, `robert-kbc-basic` is the basic account of Robert in KBC bank.

### Budget
A budget is a **conceptual** category of the expense. A budget id is in the format of `owner-category`, for example, `shared-travel` can be one that keeps track of the travel expense of a commonly owned budget.

### Master account
It's convenient to have a master account for each budget. It is the main account accountable for the budget.

---

An account can associate multiple budgets, and a budget can be spent on multiple accounts. For example, Robert's KBC basic account (`account`) can hold his salary (`budget`), personal expense (`budget`), and his pension (`budget`). Meanwhile, he has another Revolut account (`account`) that also serves as a source to spend his personal expense (`budget`).

At the end of the day, accounts are just pockets with or without money in it. What we should care about is the planning and expense of budgets. In other words, the purpose for the accountbook app is getting budget point of view insights from the transactions of accounts.

## TODO
- Streamlit
- Prefect
- Data validation with Pydantic and Pandera
