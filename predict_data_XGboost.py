from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM,Dropout,Dense,SimpleRNN
from crypto_data import get_historical_prices
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from xgboost import XGBRegressor
import numpy as np
import pandas as pd

def createData(df):
     df['dayofweek']=df.index.dayofweek
     df['quarter']=df.index.quarter
     df['month']=df.index.month
     df['year']=df.index.year
     df['dayofyear']=df.index.dayofyear
     
     return df

def predict_XGboost(coinname,type):

    time_step=60
    coin_name = coinname
    vs_currency = "usd"
    days = 1200
  
    cryptoData = get_historical_prices(coin_name, vs_currency, days)
    df = pd.DataFrame(cryptoData, columns=['Date','Close','ROC'])
    df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")


    df.index=df['Date']
    data=df.sort_index(ascending=True,axis=0)
    if type =="Close":
            new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])
            for i in range(0,len(data)):
                new_dataset["Date"][i]=data['Date'][i]
                new_dataset["Close"][i]=data["Close"][i]    
    else:
            new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])
            for i in range(0,len(data)):
                new_dataset["Date"][i]=data['Date'][i]
                new_dataset["Close"][i]=data["ROC"][i]   

    new_dataset["Close"] = new_dataset["Close"].fillna(0)
    scaler=MinMaxScaler(feature_range=(0,1))
    new_dataset.index=new_dataset.Date
    new_dataset.drop("Date",axis=1,inplace=True)
    createData(new_dataset)
    train_data=new_dataset.head(1000)
    valid_data=new_dataset.tail(200)
    print(new_dataset)
    createData(new_dataset)


    print(train_data)
    print(valid_data)

    FEATURES =['dayofweek', 'quarter', 'month', 'year','dayofyear']
    TARGET = 'Close'


    reg=XGBRegressor(n=1000, early_stopping_round=50)
    reg.fit(train_data[FEATURES],train_data[TARGET])


    
    # Get today's date
    start_date = datetime.now().date()
    start_date = start_date + timedelta(days=1)

    # Create an empty list to store the dictionaries
    nextday = []

    # Generate the next 5 days
    for i in range(1):
        # Create a dictionary with the keys "Date" and "Predictions"
        day_dict = {"Date": start_date, "Predictions": None}
        
        # Add the dictionary to the list
        nextday.append(day_dict)
        
        # Increment the date by 1 day
        start_date += timedelta(days=1)

    # Create a DataFrame from the list of dictionaries

    Predict = pd.DataFrame(nextday)
    Predict.index=Predict.Date
    Predict.drop("Date",axis=1,inplace=True)
    Predict.index = pd.to_datetime(Predict.index)
    createData(Predict)
    Predict["Predictions"][0] =reg.predict(Predict[FEATURES])[0]
    print(Predict)


    predicted_closing_price=reg.predict(valid_data[FEATURES])
    valid_data["Predictions"]=predicted_closing_price
    print(valid_data)
    
    
    return train_data, valid_data, Predict, df


predict_XGboost("bitcoin","Close")


