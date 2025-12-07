import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os 
load_dotenv()   

API_KEY = os.getenv("API_KEY")

def fetch_crypto_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets?{API_KEY}"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }

    response = requests.get(url, params=params)
    raw_json = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(raw_json)

    # Keep final filtered columns
    df_filtered = df[[
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "total_volume",
        "circulating_supply",
        "price_change_percentage_1h_in_currency",
        "price_change_percentage_24h_in_currency",
        "price_change_percentage_7d_in_currency"
    ]]

    # Add timestamp column
    df_filtered["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------------------------
    # Save to CSV (append mode)
    # ---------------------------
    df_filtered.to_csv("crypto_data.csv", mode='a', index=False, header=False)

    # ---------------------------
    # Save raw JSON to TXT
    # ---------------------------
    with open("crypto_raw.txt", "a") as file:
        file.write(f"\n--- Fetch at {df_filtered['timestamp'].iloc[0]} ---\n")
        file.write(str(raw_json))
        file.write("\n\n")

    return df_filtered


if __name__ == "__main__":
    df = fetch_crypto_data()
    print(df.head())
