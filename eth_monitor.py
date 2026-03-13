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
min_price = df['low'].astype(float).min()Z

# 3. Send MS Teams notification (Replace with your actual Webhook URL)
webhook_url = "https://defaultd9c4591376534be2920bbdb0386381.84.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/0511520dd1fe40f2b1e362b3b6786011/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=hWNGEPyNmBTkq-BvI31OW1frckeaZF5aHYwJMDzszV0"
payload = {
    "title": "ETH Price Monitor Report",
    "text": f"User: [Your Username] \n\nMax price in the past hour: ${max_price} \n\nMin price in the past hour: ${min_price}",
    "themeColor": "0076D7"
}

# Post to Teams channel
response = requests.post(webhook_url, json=payload)
if response.status_code in [200, 202]:
    print("Notification sent successfully.")
else:
    print(f"Failed to send notification. Status code: {response.status_code}")