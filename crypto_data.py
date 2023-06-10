import requests
from datetime import datetime
import json

def get_historical_prices(coin_name, vs_currency, days):
    # Define the API endpoint and parameters
    api_url = "https://api.coingecko.com/api/v3"
    coin_id = coin_name.lower()  # Convert the coin name to lowercase for the API
    vs_currency = vs_currency.lower()  # Convert the currency to lowercase for the API

    # Construct the API URL
    endpoint = f"/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    url = api_url + endpoint

    # Send the GET request to the API
    response = requests.get(url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Retrieve the historical data from the response
        data = response.json()
        prices = data["prices"]

        # Process the closing prices for unique dates and calculate ROC
        unique_dates = set()
        historical_data = []
        previous_price = None
        for price in prices:
            timestamp = price[0] / 1000  # Divide by 1000 to convert milliseconds to seconds
            price_value = price[1]
            date = datetime.fromtimestamp(timestamp).date()
            if date not in unique_dates:
                unique_dates.add(date)
                roc = None
                if previous_price is not None:
                    roc = (price_value - previous_price) / previous_price
                historical_data.append({"Date": date, "Close": price_value, "ROC": roc})
                previous_price = price_value

        return historical_data

    else:
        print(f"Error occurred. Status Code: {response.status_code}")
        return None
    
def get_formatted_coin_list(limit=100):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
    response = requests.get(url)
    if response.status_code == 200:
        coin_list = response.json()
        formatted_coins = []
        for coin in coin_list:
            label = coin['symbol'].upper()
            value = coin['id']
            formatted_coin = {"label": label, "value": value}
            formatted_coins.append(formatted_coin)
        return formatted_coins
    else:
        return None
