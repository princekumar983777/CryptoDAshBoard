import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv("API_KEY")

# url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&x_cg_demo_api_key={API_KEY}"
# url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,dogecoin&vs_currencies=usd&x_cg_demo_api_key={API_KEY}"

url = f"https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key={API_KEY}"
response = requests.get(url)
data = response.json()

print(data)
