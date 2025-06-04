import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tabulate import tabulate

def analyze_etf_data_return_dict(file_path, sheet_name='Sheet1', risk_free_rate=2.67/100):
    """
    Analyze ETF data and return results as dictionary (for batch processing).
    """
    try:
        # Load price data
        df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0, parse_dates=True)
        # Drop missing values
        df.dropna(subset=["Last Price"], inplace=True)
        
        # Get name
        name = df["Name"].dropna().iloc[0] if "Name" in df.columns and not df["Name"].dropna().empty else os.path.basename(file_path)
        
        # Compute daily returns
        daily_returns = df["Last Price"].pct_change().dropna()
        
        # Compute key stats
        mean = daily_returns.mean()
        std_dev = daily_returns.std()
        ann_ret = (1 + daily_returns.mean()) ** 252 - 1
        ann_vol = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = (ann_ret - risk_free_rate) / ann_vol
        
        return {
            'Name': name,
            'Mean Daily Return': mean,
            'Daily Volatility': std_dev,
            'Annualized Return': ann_ret,
            'Annualized Volatility': ann_vol,
            'Sharpe Ratio': sharpe_ratio,
            'File': os.path.basename(file_path)
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def analyze_all_etfs_in_folder(folder_path='Min_vol', risk_free_rate=2.67/100):
    """
    Analyze all Excel files in a folder and create comparison table.
    """
    # Get all Excel files in the folder
    excel_files = []
    for file in os.listdir(folder_path):
        if file.endswith(('.xlsx', '.xls')):
            excel_files.append(os.path.join(folder_path, file))
    
    print(f"Found {len(excel_files)} Excel files in {folder_path}")
    print("Files to analyze:", [os.path.basename(f) for f in excel_files])
    print("\n" + "="*80 + "\n")
    
    # Analyze each file
    all_results = []
    for file_path in excel_files:
        print(f"Analyzing: {os.path.basename(file_path)}")
        result = analyze_etf_data_return_dict(file_path, risk_free_rate=risk_free_rate)
        if result:
            all_results.append(result)
        print("-" * 40)
    
    # Create comparison DataFrame
    if all_results:
        df_results = pd.DataFrame(all_results)
        
        # Sort by Sharpe Ratio (descending)
        df_results = df_results.sort_values('Sharpe Ratio', ascending=False)
        
        return df_results
    else:
        print("No valid results found.")
        return None

def print_beautiful_table(df_results):
    """
    Print results in a beautiful formatted table.
    """
    if df_results is None or df_results.empty:
        print("No data to display.")
        return
    
    # Create a formatted version for display
    display_df = df_results.copy()
    
    # Format percentages and numbers
    display_df['Mean Daily Return'] = display_df['Mean Daily Return'].apply(lambda x: f"{x:.4%}")
    display_df['Daily Volatility'] = display_df['Daily Volatility'].apply(lambda x: f"{x:.4%}")
    display_df['Annualized Return'] = display_df['Annualized Return'].apply(lambda x: f"{x:.2%}")
    display_df['Annualized Volatility'] = display_df['Annualized Volatility'].apply(lambda x: f"{x:.2%}")
    display_df['Sharpe Ratio'] = display_df['Sharpe Ratio'].apply(lambda x: f"{x:.3f}")
    
    # Shorten names if too long
    display_df['Name'] = display_df['Name'].apply(lambda x: x[:30] + "..." if len(x) > 30 else x)
    
    # Remove File column for cleaner display
    display_df = display_df.drop('File', axis=1)
    
    print("ETF PERFORMANCE COMPARISON")
    print("=" * 120)
    print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    original_df = df_results.copy()
    print(f"Number of ETFs analyzed: {len(original_df)}")
    print(f"Best Sharpe Ratio: {original_df['Sharpe Ratio'].max():.3f} ({original_df.loc[original_df['Sharpe Ratio'].idxmax(), 'Name']})")
    print(f"Highest Return: {original_df['Annualized Return'].max():.2%} ({original_df.loc[original_df['Annualized Return'].idxmax(), 'Name']})")
    print(f"Lowest Volatility: {original_df['Annualized Volatility'].min():.2%} ({original_df.loc[original_df['Annualized Volatility'].idxmin(), 'Name']})")
    
    print(f"\nAverage Annualized Return: {original_df['Annualized Return'].mean():.2%}")
    print(f"Average Annualized Volatility: {original_df['Annualized Volatility'].mean():.2%}")
    print(f"Average Sharpe Ratio: {original_df['Sharpe Ratio'].mean():.3f}")

def create_comparison_charts(df_results):
    """
    Create visualization charts for comparison.
    """
    if df_results is None or df_results.empty:
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Shorten names for charts
    short_names = [name[:15] + "..." if len(name) > 15 else name for name in df_results['Name']]
    
    # 1. Annualized Return vs Volatility (Risk-Return scatter)
    ax1.scatter(df_results['Annualized Volatility'], df_results['Annualized Return'], 
                c=df_results['Sharpe Ratio'], cmap='RdYlGn', s=100, alpha=0.7)
    ax1.set_xlabel('Annualized Volatility')
    ax1.set_ylabel('Annualized Return')
    ax1.set_title('Risk-Return Profile (Color = Sharpe Ratio)')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(ax1.collections[0], ax=ax1)
    cbar.set_label('Sharpe Ratio')
    
    # 2. Sharpe Ratio comparison
    bars1 = ax2.bar(range(len(df_results)), df_results['Sharpe Ratio'], 
                    color=['green' if x > 0 else 'red' for x in df_results['Sharpe Ratio']])
    ax2.set_xlabel('ETFs')
    ax2.set_ylabel('Sharpe Ratio')
    ax2.set_title('Sharpe Ratio Comparison')
    ax2.set_xticks(range(len(df_results)))
    ax2.set_xticklabels(short_names, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # 3. Annualized Returns
    bars2 = ax3.bar(range(len(df_results)), df_results['Annualized Return'], 
                    color='skyblue', alpha=0.7)
    ax3.set_xlabel('ETFs')
    ax3.set_ylabel('Annualized Return')
    ax3.set_title('Annualized Returns Comparison')
    ax3.set_xticks(range(len(df_results)))
    ax3.set_xticklabels(short_names, rotation=45, ha='right')
    ax3.grid(True, alpha=0.3)
    
    # Format y-axis as percentage
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # 4. Volatility comparison
    bars3 = ax4.bar(range(len(df_results)), df_results['Annualized Volatility'], 
                    color='orange', alpha=0.7)
    ax4.set_xlabel('ETFs')
    ax4.set_ylabel('Annualized Volatility')
    ax4.set_title('Volatility Comparison')
    ax4.set_xticks(range(len(df_results)))
    ax4.set_xticklabels(short_names, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3)
    
    # Format y-axis as percentage
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    # Analyze all ETFs in the Min_vol folder
    results_df = analyze_all_etfs_in_folder('Min_vol')
    
    if results_df is not None:
        # Print beautiful table
        print_beautiful_table(results_df)
        
        # Create charts
        create_comparison_charts(results_df)
        
        # Optionally save to Excel
        results_df.to_excel('etf_comparison_results.xlsx', index=False)
        print(f"\nResults saved to 'etf_comparison_results.xlsx'")


results_df = analyze_all_etfs_in_folder('Min_vol')
print_beautiful_table(results_df)
create_comparison_charts(results_df)
