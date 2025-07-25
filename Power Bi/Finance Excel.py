import pandas as pd # type: ignore

income_statement = pd.DataFrame({
    "Month": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"],
    "Revenue": [100000, 110000, 105000, 115000, 120000],
    "COGS": [40000, 45000, 42000, 46000, 47000],
    "GrossProfit": [60000, 65000, 63000, 69000, 73000],
    "OperatingExpense": [20000, 21000, 22000, 23000, 24000],
    "NetProfit": [40000, 44000, 41000, 46000, 49000]
})

balance_sheet = pd.DataFrame({
    "Date": ["2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", "2024-05-31"],
    "TotalAssets": [500000, 510000, 520000, 530000, 540000],
    "TotalLiabilities": [200000, 205000, 210000, 215000, 220000],
    "Equity": [300000, 305000, 310000, 315000, 320000]
})

cash_flow = pd.DataFrame({
    "Month": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"],
    "CashInflow": [120000, 125000, 123000, 130000, 135000],
    "CashOutflow": [90000, 95000, 94000, 98000, 100000],
    "NetCash": [30000, 30000, 29000, 32000, 35000]
})

forecast_plan = pd.DataFrame({
    "Month": ["2024-06", "2024-07", "2024-08", "2024-09", "2024-10"],
    "Category": ["Revenue", "Revenue", "Revenue", "Revenue", "Revenue"],
    "Budgeted": [125000, 130000, 135000, 140000, 145000],
    "Forecasted": [123000, 132000, 134000, 139000, 146000]
})

with pd.ExcelWriter("Financial_Health_SampleData.xlsx") as writer:
    income_statement.to_excel(writer, sheet_name="IncomeStatement", index=False)
    balance_sheet.to_excel(writer, sheet_name="BalanceSheet", index=False)
    cash_flow.to_excel(writer, sheet_name="CashFlow", index=False)
    forecast_plan.to_excel(writer, sheet_name="ForecastPlan", index=False)

print("Excel file 'Financial_Health_SampleData.xlsx' created successfully!")
