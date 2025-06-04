import pandas as pd

years = [2026, 2027, 2028, 2029, 2030]

salary = [65000, 65000, 65000,65000, 65000]

state_pension = [25000, 25000, 25000, 25000, 25000]

expense_target = 200_000

df_liquidity_needs = pd.DataFrame({
    "Year": years,
    "Salary": salary,
    "Pension": state_pension,
    "Expense Target": expense_target
})
df_liquidity_needs["Total Income"] = df_liquidity_needs["Salary"] + df_liquidity_needs["Pension"]
df_liquidity_needs["Shortfall"] = df_liquidity_needs["Expense Target"] - df_liquidity_needs["Total Income"]

print("=" * 70)
print(df_liquidity_needs)
print("\n-->" + " Liquidity Needs Over 5 Years")
print("\nTotal cash needed from the portfolio over 5 years:"
      f"£{df_liquidity_needs['Shortfall'].sum():,.2f}")
print("=" * 70)