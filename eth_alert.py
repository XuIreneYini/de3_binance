import sys
from binance.client import Client
import apprise

def main():
    # Initialize Binance client
    client = Client()
    
    # Fetch the past hour's 1-minute interval klines data for ETHUSDT
    try:
        klines = client.get_klines(symbol='ETHUSDT', interval='1m', limit=60)
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # Extract closing prices (index 4 in Binance kline response)
    close_prices = [float(kline[4]) for kline in klines]
    
    # Calculate minimum and maximum prices
    min_price = min(close_prices)
    max_price = max(close_prices)

    # Initialize Apprise for MS Teams notification
    poster = apprise.Apprise()
    
    # Replace 'YOUR_WEBHOOK_URL' with the actual MS Teams webhook URL 
    # (or fetch it securely from AWS Systems Manager Parameter Store)
    webhook_url = 'https://defaultd9c4591376534be2920bbdb0386381.84.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/8a468fa405f641ada4e140722f64d341/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=eErf-DwghzZVXEkhwSLPUlvGE9giZYeka90pr6N5yBE'
    poster.add(webhook_url)

    # Define message content with custom emoji and username identity
    title = '📈 ETH Hourly Price Alert'
    body = f'🤖 Irene-Bot:\nOver the past hour, ETH minimum price was ${min_price:.2f} and maximum price was ${max_price:.2f}.'

    # Send notification
    result = poster.notify(
        title=title,
        body=body,
    )
    
    if result:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification.")
        sys.exit(1)

if __name__ == "__main__":
    main()