import os
import requests
from binance.client import Client
import pandas as pd

# 1. Fetch data from Binance
client = Client()
# Get ETHUSDT klines for the past 1 hour (60 minutes)
klines = client.get_klines(symbol='ETHUSDT', interval='1m', limit=60)
df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])

# 2. Calculate statistics
# Convert strings to float for calculation
max_price = df['high'].astype(float).max()
min_price = df['low'].astype(float).min()

# 3. Send MS Teams notification (Replace with your actual Webhook URL)
webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')
if webhook_url:
    payload = {
        "title": "ETH Price Monitor Report",
        "text": f"User: Irene \n\nMax price in the past hour: ${max_price} \n\nMin price in the past hour: ${min_price}",
        "themeColor": "0076D7"
    }

    # Post to Teams channel
    response = requests.post(webhook_url, json=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code in [200, 202]:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")
else:
    print("TEAMS_WEBHOOK_URL environment variable not set. Skipping notification.")