from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM,Dropout,Dense
from crypto_data import get_historical_prices
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def predictLSTM(coinname,type):

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
    final_dataset=new_dataset.values

    train_data=final_dataset[0:1000,:]
    valid_data=final_dataset[1000:,:]

    scaled_data=scaler.fit_transform(final_dataset)
    x_train_data,y_train_data=[],[]
    for i in range(60,len(train_data)):
        x_train_data.append(scaled_data[i-60:i,0])
        y_train_data.append(scaled_data[i,0])
        
    x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)
    x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))

    lstm_model=Sequential()
    lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error',optimizer='adam')
    lstm_model.fit(x_train_data,y_train_data,epochs=1,batch_size=1,verbose=2)

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

    #predict 1 day later
    X_input = new_dataset.iloc[-time_step:].Close.values               # getting last 60 rows and converting to array
    X_input = scaler.fit_transform(X_input.reshape(-1,1))      # converting to 2D array and scaling
    X_input = np.reshape(X_input, (1,time_step,1))                    # reshaping : converting to 3D array
    LSTM_prediction = scaler.inverse_transform(lstm_model.predict(X_input))
    Predict["Predictions"][0] = LSTM_prediction[0][0]
    print(LSTM_prediction)


    inputs_data=new_dataset[len(new_dataset)-len(valid_data)-60:].values
    inputs_data=inputs_data.reshape(-1,1)
    inputs_data=scaler.transform(inputs_data)

    X_test=[]
    for i in range(60,inputs_data.shape[0]):
        X_test.append(inputs_data[i-60:i,0])
        
    X_test=np.array(X_test)
    X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
    print("do dai ne:",len(X_test))

    predicted_closing_price=lstm_model.predict(X_test)
    predicted_closing_price=scaler.inverse_transform(predicted_closing_price)

    train_data=new_dataset[:1000]
    valid_data=new_dataset[1000:]
    valid_data["Predictions"]=predicted_closing_price




    
    return train_data, valid_data, Predict, df


