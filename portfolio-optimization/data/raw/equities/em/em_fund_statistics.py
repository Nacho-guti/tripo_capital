import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def analyze_etf_data(file_path, risk_free_rate= 0.0444):
    '''Analyze ETF data from an Excel file and compute key statistics.
    Parameters:
    file_path (str): Path to the Excel file containing ETF data.
    risk_free_rate: calculated in other python script, default is 2.67% as a decimal.
    '''

    # load price data
    df = pd.read_excel(file_path, sheet_name='Sheet1', index_col=0, parse_dates=True)
    
    # Get name of the ETF
    name = df["Name"].dropna().iloc[0]
    print(name)
    
    # Filter to last 3 years max
    cutoff_date = df.index.max() - pd.DateOffset(years=3)
    df = df[df.index >= cutoff_date]
    data_years = len(df) / 252 

    # Organise from old to new
    df.sort_index(inplace=True)
    # Drop missing values
    df.dropna(subset=["Last Price"], inplace=True)

    # daily_returns = df["Last Price"].pct_change().dropna()
    
    # Compute daily log returns

    daily_returns = np.log(df["Last Price"] / df["Last Price"].shift(1)).dropna()

    # Compute key stats
    mean = daily_returns.mean()
    std_dev = daily_returns.std()
    ann_ret = daily_returns.mean() * 252  # Annualized return of log returns
    ann_vol = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (ann_ret - risk_free_rate ) / ann_vol

    # Calculate CAGR (actual compound annual growth rate)
    start_price = df["Last Price"].iloc[0]
    end_price = df["Last Price"].iloc[-1]
    n_years = len(df) / 252
    cagr = (end_price / start_price) ** (1/n_years) - 1

    #Print key stats
    print(f"Name of the ETF: {name}")
    print(f"Mean Daily Return: {mean:.4%}")
    print(f"Standard Deviation of Daily Returns: {std_dev:.4%}")
    print(f"CAGR: {cagr:.2%}")
    print(f"Annualised Log Return: {ann_ret:.2%}")
    print(f"Annualised Log Volatility: {ann_vol:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Years of fata used: {data_years:.1f}")
    

# analyze_etf_data('Min_vol/em_min_vol_etf.xlsx', risk_free_rate=2.67/100)
# analyze_etf_data('apple_stock.xlsx', risk_free_rate=4.25/100)

data_path = os.path.join("portfolio-optimization", "data", "raw", "equities", "em")

files = [
'artemis_em_etf.xlsx',
'hsbc_china_em_etf.xlsx',
'hsbc_frontier_etf.xlsx',
]

# Run each one
for file in files:
    full_path = os.path.join(data_path, file)
    print("="*60)
    

    # Check if file exists before trying to analyze it
    if os.path.exists(full_path):
        analyze_etf_data(full_path)
    else:
        print(f"File {full_path} does not exist. Skipping analysis.")
    
    
    print("\n")
    