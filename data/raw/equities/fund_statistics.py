import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def analyze_etf_data(file_path, risk_free_rate= 4.25/100):
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
    
    # Organise from old to new
    df.sort_index(inplace=True)
    # Drop missing values
    df.dropna(subset=["Last Price"], inplace=True)

    
    
    # Compute daily returns
    daily_returns = df["Last Price"].pct_change().dropna()

    # Compute key stats
    mean = daily_returns.mean()
    std_dev = daily_returns.std()
    ann_ret = (1 + mean) ** 252 - 1
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
    print(f"Annualised Return: {ann_ret:.2%}")
    print(f"Annualised Volatility: {ann_vol:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    

# analyze_etf_data('Min_vol/em_min_vol_etf.xlsx', risk_free_rate=2.67/100)
# analyze_etf_data('apple_stock.xlsx', risk_free_rate=4.25/100)

files = [
    'Min_vol/em_min_vol_etf.xlsx',
    'Min_vol/euro_min_vol_etf.xlsx',
    'Min_vol/snp_min_vol_etf.xlsx',
    'Min_vol/world_min_vol_etf.xlsx'
]

# Run each one
for file in files:
    print("="*60)
    analyze_etf_data(file)
    print("\n")
    