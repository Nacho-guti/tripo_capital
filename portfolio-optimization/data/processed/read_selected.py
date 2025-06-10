import pandas as pd

# Read the selected assets summary
df = pd.read_excel("../../results/selected_assets_summary.xlsx")

# Display the selected assets and their weights
print("\nSelected Assets in Optimized Portfolio:")
print("=======================================")
for _, row in df.iterrows():
    print(f"{row['Ticker']}: {row['Weight']:.2%}")

print(f"\nTotal number of selected assets: {len(df)}") 