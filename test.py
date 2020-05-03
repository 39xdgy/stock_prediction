import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')



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
df = web.DataReader('AAPL', data_source = 'yahoo', start = '2016-01-01', end = '2020-04-25')
print(df.filter(['previous Close']))


#Get the number of rows and columns in the data set
#'''#print(df.shape)'''

#Visualize the closing price history
fig_size = (16, 8)
title = 'Close Price History'
x_name = 'Date'
y_name = 'Close Price USD ($)'
'''#plot_stock(fig_size, title, df['Close'], x_name, y_name)'''



#Create a new dataframe with only the 'close column'
data = df.filter(['Close'])

#convert the dataframe to a numpy array
dataset = data.values

#Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * .8)


'''#print(training_data_len)

#print(dataset)'''

#Scale the data
scaler = MinMaxScaler(feature_range = (0, 1))
scaled_data = scaler.fit_transform(dataset)

'''#print(scaled_data)'''


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
#print(x_train.shape)


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
predictions = scaler.inverse_transform(predictions)

#Get the root mean squared error(RMSE)
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

#Show the valid and predicted prices
#print(valid)

    
