import pandas as pd
import os

def get_risk_free_rate(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path, index_col=0, parse_dates=True)
    
    # Sort from oldest to newest (in case it's not already sorted properly)
    df = df.sort_index()
    
    # Filter to last 3 years
    end_date = df.index.max()
    start_date = end_date - pd.DateOffset(years=3)
    df_filtered = df[df.index >= start_date]
    
    # Calculate average (assuming the rate column is the first data column)
    # Replace 'Rate' with your actual column name
    avg_rate = df_filtered.iloc[:, 0].mean()
    
    print(f"Period: {df_filtered.index.min().date()} to {df_filtered.index.max().date()}")
    print(f"Average 3-month T-bill rate: {avg_rate:.2f}%")
    print(f"As decimal for your code: {avg_rate/100:.4f}")
    
    return avg_rate / 100  # Return as decimal


# Define the base directory
base_dir = os.path.join('portfolio-optimization', 'data', 'raw', 'risk_free')

filename = 'uk_3m_tb.xlsx'

full_path = os.path.join(base_dir, filename)
uk_risk_free_rate = get_risk_free_rate(full_path)

