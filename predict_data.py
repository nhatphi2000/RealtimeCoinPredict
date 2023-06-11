from train import get_train_data
from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM,Dropout,Dense
from crypto_data import get_historical_prices
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def predictLSTM(coinname):

    time_step=60
    coin_name = coinname
    vs_currency = "usd"
    days = 1200

    cryptoData = get_historical_prices(coin_name, vs_currency, days)
    df = pd.DataFrame(cryptoData, columns=['Date','Close','ROC'])
    df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")


    df.index=df['Date']
    data=df.sort_index(ascending=True,axis=0)
    new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])
    for i in range(0,len(data)):
        new_dataset["Date"][i]=data['Date'][i]
        new_dataset["Close"][i]=data["Close"][i]    

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

    print(new_dataset)

    lstm_model=Sequential()
    lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error',optimizer='adam')
    lstm_model.fit(x_train_data,y_train_data,epochs=1,batch_size=1,verbose=2)


    #start predict next 5 days
    closedf=scaler.fit_transform(np.array(final_dataset).reshape(-1,1))
    test_data=closedf[1000:len(closedf),:1]
    x_input=test_data[len(test_data)-time_step:].reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    lst_output=[]
    n_steps=time_step
    i=0
    pred_days = 5
    while(i<pred_days):
        
        if(len(temp_input)>time_step):
            
            x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            
            yhat = lstm_model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
        
            lst_output.extend(yhat.tolist())
            i=i+1
            
        else:
            
            x_input = x_input.reshape((1, n_steps,1))
            yhat = lstm_model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            
            lst_output.extend(yhat.tolist())
            i=i+1

    # Get today's date
    start_date = datetime.now().date()
    start_date = start_date + timedelta(days=1)

    # Create an empty list to store the dictionaries
    next5days = []

    # Generate the next 5 days
    for i in range(5):
        # Create a dictionary with the keys "Date" and "Predictions"
        day_dict = {"Date": start_date, "Predictions": None}
        
        # Add the dictionary to the list
        next5days.append(day_dict)
        
        # Increment the date by 1 day
        start_date += timedelta(days=1)

    # Create a DataFrame from the list of dictionaries

    Predict = pd.DataFrame(next5days)
    Predict.index=Predict.Date
    Predict.drop("Date",axis=1,inplace=True)


    last_days=np.arange(1,time_step+1)
    day_pred=np.arange(time_step+1,time_step+pred_days+1)
    temp_mat = np.empty((len(last_days)+pred_days+1,1))
    temp_mat[:] = np.nan
    temp_mat = temp_mat.reshape(1,-1).tolist()[0]

    last_original_days_value = temp_mat
    next_predicted_days_value = temp_mat

    last_original_days_value[0:time_step+1] = scaler.inverse_transform(closedf[len(closedf)-time_step:]).reshape(1,-1).tolist()[0]
    next_predicted_days_value[time_step+1:] = scaler.inverse_transform(np.array(lst_output).reshape(-1,1)).reshape(1,-1).tolist()[0]

    for i in range(61,66):
        Predict["Predictions"][i-61]= next_predicted_days_value[i]

    print(Predict.tail())


    inputs_data=new_dataset[len(new_dataset)-len(valid_data)-60:].values
    inputs_data=inputs_data.reshape(-1,1)
    inputs_data=scaler.transform(inputs_data)

    X_test=[]
    for i in range(60,inputs_data.shape[0]):
        X_test.append(inputs_data[i-60:i,0])
        
    X_test=np.array(X_test)
    X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

    predicted_closing_price=lstm_model.predict(X_test)
    predicted_closing_price=scaler.inverse_transform(predicted_closing_price)

    train_data=new_dataset[:1000]
    valid_data=new_dataset[1000:]
    valid_data["Predictions"]=predicted_closing_price




    
    return train_data, valid_data, Predict, df


