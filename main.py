from crypto_data import get_historical_prices

# Example usage
coin_name = "bitcoin"
vs_currency = "usd"
days = 30

data = get_historical_prices(coin_name, vs_currency, days)
if data:
    for item in data:
        date = item["date"]
        close_price = item["close_price"]
        roc = item["roc"]
        print(f"Date: {date}, Close Price: {close_price}, Roc: {roc}")