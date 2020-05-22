import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from datetime import date
import baostock as bs
plt.style.use('fivethirtyeight')




def Chinese_data():
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节
    all = "date,code,open,high,low,Close,preClose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
    Close = "Close"
    rs = bs.query_history_k_data_plus("sh.603888",
        Close,
        start_date='2012-01-01', end_date=str(date.today()),
        frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
    #print('query_history_k_data_plus respond error_code:'+rs.error_code)
    #print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    #result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
    #print(result)#.dtypes)

    #### 登出系统 ####
    bs.logout()
    #print(result)
    return result







def create_model(x_train):
    #Create the model
    model = Sequential()
    model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences = False))
    model.add(Dense(25))
    model.add(Dense(1))

    #Compile the model
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    return model

def plot_stock(fig_size, title, plot_data, x_name, y_name):
    plt.figure(figsize = fig_size)
    plt.title(title)
    plt.plot(plot_data)
    plt.xlabel(x_name, fontsize = 18)
    plt.ylabel(y_name, fontsize = 18)
    plt.show()



#Get the stock quote
df = web.DataReader('AAPL', data_source = 'yahoo', start = '2016-01-01', end = '2020-05-01')
#print(df.filter)


#Get the number of rows and columns in the data set
#'''#print(df.shape)'''

#Visualize the closing price history
fig_size = (16, 8)
title = 'Close Price History'
x_name = 'Date'
y_name = 'Close Price USD ($)'
'''#plot_stock(fig_size, title, df['Close'], x_name, y_name)'''


#print(df)
#Create a new dataframe with only the 'Close column'
data = df.filter(['High', 'Close'])
output_scale_data = df.filter(['Close'])
data_China = Chinese_data()
#print(data_US)
#print(data)
#print(data_China.shape)
#print(data.shape)
#convert the dataframe to a numpy array
dataset = data.values#.astype(float)
output_scale_dataset = output_scale_data.values
#Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * .8)


'''#print(training_data_len)
'''
print(data)

#Scale the data
scaler = MinMaxScaler(feature_range = (0, 1))
de_scaler = MinMaxScaler(feature_range = (0, 1))
scaled_data = scaler.fit_transform(dataset)
only_close_data  = de_scaler.fit_transform(output_scale_dataset)
'''#print(scaled_data)'''


for i in range(0, len(only_close_data[0])):
    if(scaled_data[i][1] == only_close_data[0][i]):
        print(scaled_data[i][1] , "does not equal to ", only_close_data[0][i])



#create the training data set
#Create the scaled training data set
train_data = scaled_data[0:training_data_len, :]
#split the data into x_train and y_train data sets
x_train = []
y_train = []


for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    '''#
    if i <= 60:
        print(x_train)
        print(y_train)
        print()
    #'''


#convert the x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

#Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
print(x_train.shape)


model = create_model(x_train)
#'''
model.fit(x_train, y_train, batch_size = 1, epochs = 5)
#'''


#create the testing data set
#create a new array containing scaled values from index 1543 to 2003
test_data = scaled_data[training_data_len - 60: , :]
#create the datasets x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])


#Convert the data to a numpy array
x_test = np.array(x_test)

#Reshape data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#Get the models predicted price values
predictions = model.predict(x_test)
predictions = de_scaler.inverse_transform(predictions)

#Get the root mean squared error(RMSE)
#print(predictions)
#print(y_test)
#print(np.mean(predictions - y_test))
rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
print(rmse)



#Plot the data
train = data[ : training_data_len]
valid = data[training_data_len : ]
valid['Predictions'] = predictions

#Visualize the data
plt.figure(figsize = (16, 8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize = 18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right' )
plt.show()

print("Prediction is: ", predictions)
#Show the valid and predicted prices
#print(valid)
