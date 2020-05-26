import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from datetime import date



class stock_model:

    def __init__(self, stock_name, training_time_zone):
        self.stock_name = stock_name
        self.start_time = training_time_zone[0]
        self.end_time = training_time_zone[1]
        self.all_data = web.DataReader(self.stock_name, data_source = 'yahoo', start = self.start_time, end = self.end_time)
        #print(self.all_data)
        self.data = self.all_data.filter(['Close'])#['High', 'Low', 'Open', 'Close'])#, 'Volume'])
        de_scale_data = self.all_data.filter(['Close'])
        self.dataset = self.data.values
        de_scale_data = de_scale_data.values
        self.training_data_len = math.ceil(len(self.dataset) * .8)
        self.x_train = []
        self.y_train = []
        self.scaler = MinMaxScaler(feature_range = (0, 1))
        self.de_scaler = MinMaxScaler(feature_range = (0, 1))
        self.scaled_data = self.scaler.fit_transform(self.dataset)
        __ = self.de_scaler.fit_transform(de_scale_data)
        self.model = None
        self.pred_price = 0
        self.rmse = 0
        self.len_train_data = 0
        self.epoch = 0

    def draw_plot(self):
        #Visualize the closing price history
        fig_size = (16, 8)
        title = 'Close Price History'
        x_name = 'Date'
        y_name = 'Close Price USD ($)'
        self.plot_stock(fig_size, title, self.data, x_name, y_name)


    def plot_stock(self, fig_size, title, plot_data, x_name, y_name):
        plt.figure(figsize = fig_size)
        plt.title(title)
        plt.plot(plot_data)
        plt.xlabel(x_name, fontsize = 18)
        plt.ylabel(y_name, fontsize = 18)
        plt.show()




    def generate_train_data(self):
        #Scale the data


        #create the training data set
        #Create the scaled training data set
        train_data = self.scaled_data[0:self.training_data_len, :]

        for i in range(60, len(train_data)):
            self.x_train.append(train_data[i-60:i, 0])
            self.y_train.append(train_data[i, 0])

        self.len_train_data = len(self.x_train)
        self.epoch = 6000 // self.len_train_data
        if (self.epoch > 15): self.epoch = 15
        #convert the x_train and y_train to numpy arrays
        self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)

        #Reshape the data
        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))



    def generate_model(self):

        self.model = Sequential()
        self.model.add(LSTM(50, return_sequences = True, input_shape = (self.x_train.shape[1], 1)))
        self.model.add(LSTM(50, return_sequences = False))
        self.model.add(Dense(25))
        self.model.add(Dense(1))

        self.model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    def create_brain(self):
        self.generate_train_data()

        self.generate_model()

        self.model.fit(self.x_train, self.y_train, batch_size = 1, epochs = self.epoch)
        self.get_RMSE()


    def get_RMSE(self):

        #create the testing data set
        #create a new array containing scaled values from index 1543 to 2003
        test_data = self.scaled_data[self.training_data_len - 60: , :]


        #create the datasets x_test and y_test
        x_test = []
        y_test = self.dataset[self.training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])


        #Convert the data to a numpy array
        x_test = np.array(x_test)

        #Reshape data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        #print("x_test shape is: ", x_test.shape)
        #Get the models predicted price values
        predictions = self.model.predict(x_test)
        predictions = self.de_scaler.inverse_transform(predictions)

        #Get the root mean squared error(RMSE)
        self.rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        print(self.rmse)


        '''
        #Plot the data
        train = self.data[ : self.training_data_len]
        valid = self.data[self.training_data_len : ]
        valid['Predictions'] = predictions

        #Visualize the data
        plt.figure(figsize = (16, 8))
        plt.title('Model')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price USD ($)', fontsize = 18)
        plt.plot(train['Close'])
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right' )
        #plt.show()
        '''
        #Show the valid and predicted prices
        #print(valid)



    def use_brain(self):
        last_60_days = self.data[-60:].values
        last_60_days_scaled = self.scaler.transform(last_60_days)
        x_predict = []
        x_predict.append(last_60_days_scaled)
        x_predict = np.array(x_predict)
        x_predict = np.reshape(x_predict, (1, x_predict.shape[1], 1))
        #print("x_predict shape is :", x_predict.shape)
        self.pred_price = self.model.predict(x_predict)
        self.pred_price = self.de_scaler.inverse_transform(self.pred_price)[0][0]
        #print(pred_price)
        print("Predict finish")

    def create_report(self):
        pred_price_str = "Predicted price: " + str(self.pred_price) + ", "
        range_str = "Range: +- "+ str(self.rmse) + "."
        final = self.stock_name + " " + pred_price_str + range_str
        return final


if __name__ == "__main__":
    x = stock_model('AAPL', ('2012-01-01', '2020-05-20'))
    x.create_brain()
    x.use_brain()
