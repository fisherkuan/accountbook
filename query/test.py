tags = """SELECT
  year,
  month,
  eur,
  account,
  budget_category,
  ARRAY(
    SELECT AS STRUCT
      `tag: salary` AS salary,
      `tag: deposit` AS deposit,
      `tag: direct_debit` AS direct_debit
    FROM `kuan-wu-accounting.data.transactions`
  )
  FROM `kuan-wu-accounting.data.transactions`"""
