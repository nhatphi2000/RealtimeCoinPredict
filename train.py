
import pandas as pd
import numpy as np
from crypto_data import get_historical_prices

def get_train_data(coinname):
    coin_name = coinname
    vs_currency = "usd"
    days = 1000

    cryptoData = get_historical_prices(coin_name, vs_currency, days)
    df_nse = pd.DataFrame(cryptoData, columns=['Date','Close','ROC'])
    df_nse["Date"]=pd.to_datetime(df_nse.Date,format="%Y-%m-%d")

    df_nse.index=df_nse['Date']
    data=df_nse.sort_index(ascending=True,axis=0)
    new_data=pd.DataFrame(index=range(0,len(df_nse)),columns=['Date','Close'])
    for i in range(0,len(data)):
        new_data["Date"][i]=data['Date'][i]
        new_data["Close"][i]=data["Close"][i]

    new_data.index=new_data.Date
    new_data.drop("Date",axis=1,inplace=True)
    dataset=new_data.values
    train=dataset[0:999,:]
    train=new_data[:999]

    return train