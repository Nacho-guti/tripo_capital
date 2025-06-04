import pandas as pd
import refinitiv.data as rd
import os
from datetime import datetime

# Your API key
API_KEY = "cf65c1e122da4ebaaeefa4eecf002fed1b7b9d95"

def create_output_folder():
    """Create a folder for storing output files"""
    # Create folder name with current date
    today = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"uk_zero_curve_data_{today}"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Created folder: {folder_name}")
    else:
        print(f"📁 Using existing folder: {folder_name}")
    
    return folder_name

def main():
    print("🇬🇧 UK Zero-Coupon Yield Curve Fetcher")
    print("=" * 45)
    
    # Create output folder
    output_folder = create_output_folder()
    
    try:
        print("🔄 Connecting to Refinitiv...")
        rd.open_session(app_key=API_KEY)
        print("✅ Connected successfully!")
        
        print("📊 Fetching UK zero-coupon yields...")
        
        # The exact zero-coupon yield RICs we need
        zero_yield_rics = [
            'GBGOV1YZ=R',  # 1Y Zero Yield
            'GBGOV2YZ=R',  # 2Y Zero Yield
            'GBGOV3YZ=R',  # 3Y Zero Yield
            'GBGOV4YZ=R',  # 4Y Zero Yield
            'GBGOV5YZ=R',  # 5Y Zero Yield
        ]
        
        print("🎯 Fetching zero-coupon yields with specific RICs...")
        print("Instruments:")
        for i, ric in enumerate(zero_yield_rics, 1):
            print(f"   {i}Y: {ric}")
        
        try:
            df = rd.get_data(
                universe=zero_yield_rics,
                fields=['CF_LAST', 'CF_BID', 'CF_ASK', 'CF_DATE', 'CF_TIME']
            )
            
            print("✅ Zero-coupon yield data retrieved!")
            print("\n📈 Raw data:")
            print(df)
            
            if df is not None and not df.empty:
                # Clean and format the data
                df_clean = df.reset_index()
                
                # Add tenor labels
                df_clean['Tenor'] = ['1Y', '2Y', '3Y', '4Y', '5Y']
                
                # Reorder columns for better readability
                if 'Instrument' in df_clean.columns:
                    cols = ['Tenor', 'Instrument'] + [col for col in df_clean.columns if col not in ['Tenor', 'Instrument']]
                    df_clean = df_clean[cols]
                
                print("\n📋 Formatted Zero-Coupon Yield Curve:")
                print(df_clean.to_string(index=False))
                
                # Create timestamp for files
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create filenames
                csv_filename = f"uk_zero_coupon_yields_{timestamp}.csv"
                xlsx_filename = f"uk_zero_coupon_yields_{timestamp}.xlsx"
                
                # Full paths
                csv_path = os.path.join(output_folder, csv_filename)
                xlsx_path = os.path.join(output_folder, xlsx_filename)
                
                # Save files
                df_clean.to_csv(csv_path, index=False)
                df_clean.to_excel(xlsx_path, index=False)
                
                print(f"\n💾 Files saved successfully:")
                print(f"   📄 CSV:  {csv_path}")
                print(f"   📊 Excel: {xlsx_path}")
                
                # Display key rates
                if 'CF_LAST' in df_clean.columns:
                    print(f"\n🎯 Current UK Zero-Coupon Yields:")
                    for i, (tenor, rate) in enumerate(zip(df_clean['Tenor'], df_clean['CF_LAST'])):
                        if pd.notna(rate):
                            print(f"   {tenor}: {rate:.3f}%")
                        else:
                            print(f"   {tenor}: No data")
                
                print(f"\n🎉 Success! Zero-coupon yield curve data saved in: {output_folder}")
                
            else:
                print("❌ No data returned - the RICs might not be available or accessible")
                
        except Exception as e:
            print(f"❌ Error fetching zero-coupon yields: {e}")
            print("\n🔍 This could mean:")
            print("   • RICs require special permissions")
            print("   • RICs might be slightly different")
            print("   • Need to check exact ticker format")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        
    finally:
        try:
            rd.close_session()
            print("\n🔒 Session closed")
        except:
            pass

if __name__ == "__main__":
    main()
