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
import time



class stock_model_latest:

    def __init__(self, stock_name, training_time_zone, model_data, train_title):
        self.stock_name = stock_name
        self.start_time, self.end_time = training_time_zone
        self.all_data = web.DataReader(self.stock_name, data_source = 'yahoo', start = self.start_time, end = self.end_time)
        self.batch_num, self.epoch_num, self.learning_len = model_data
        self.train_title = train_title
        self.data = self.all_data.filter([self.train_title])
        self.dataset = self.data.values
        self.x_train = []
        self.y_train = []
        self.training_data_len = len(self.dataset)#math.ceil(len(self.dataset) * .8)
        self.scaler = MinMaxScaler(feature_range = (0, 1))
        self.scaled_data = self.scaler.fit_transform(self.dataset)
        self.model = None
        self.pred_price = 0
        self.rmse = 0
        self.len_train_data = 0

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
        train_data = self.scaled_data#[0:self.training_data_len, :]
        for i in range(self.learning_len, len(train_data)):
            self.x_train.append(train_data[i-self.learning_len:i])
            self.y_train.append(train_data[i])

        self.len_train_data = len(self.x_train)
        self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)

        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))



    def generate_model(self):

        self.model = Sequential()
        self.model.add(LSTM(200, return_sequences = True, input_shape = (self.x_train.shape[1], 1)))
        self.model.add(LSTM(200, return_sequences = False))
        self.model.add(Dense(130))
        self.model.add(Dense(1))

        self.model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

    def create_brain(self):
        self.generate_train_data()

        self.generate_model()

        self.model.fit(self.x_train, self.y_train, batch_size = self.batch_num, epochs = self.epoch_num)
        #self.get_RMSE()


    def get_RMSE(self):

        test_data = self.scaled_data[self.training_data_len - self.learning_len: , :]


        x_test = []
        y_test = self.dataset[self.training_data_len:, :]
        for i in range(self.learning_len, len(test_data)):
            x_test.append(test_data[i-self.learning_len:i])


        x_test = np.array(x_test)


        x_test = np.reshape(x_test, (1, x_test.shape[1], 4))

        predictions = self.model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)


        self.rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        #print(self.rmse)


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
        last_60_days = self.data[(-1*self.learning_len):].values
        last_60_days_scaled = self.scaler.transform(last_60_days)
        x_predict = []
        x_predict.append(last_60_days_scaled)
        x_predict = np.array(x_predict)
        x_predict = np.reshape(x_predict, (x_predict.shape[0], x_predict.shape[1], 1))
        #print("x_predict shape is :", x_predict.shape)
        self.pred_price = self.model.predict(x_predict)
        self.pred_price = self.scaler.inverse_transform(self.pred_price)

    def create_report(self):
        pred_price_str = "Predicted price for {}: ".format(self.train_title) + str(self.pred_price[0, 0]) + "."
        #range_str = "Range: +- "+ str(self.rmse) + "."
        final = self.stock_name + " " + pred_price_str# + range_str
        return final




if __name__ == "__main__":
    #x = stock_model_latest('AAPL', ('2018-01-01', '2020-06-15'), (1, 10, 60))
    #x.create_brain()
    #x.use_brain()
    #print(x.pred_price)

    calculate = []
    #start = time.time()
    for i in range(0, 10):
        x = stock_model_latest('ZM', ('2018-01-01', '2020-06-18'), (1, 10, 60))
        x.create_brain()
        x.use_brain()
        print(x.pred_price)
        calculate.append(x.pred_price)
    '''
    calculate.remove(max(calculate))
    calculate.remove(max(calculate))
    calculate.remove(min(calculate))
    calculate.remove(min(calculate))
    '''
    high = []
    low = []
    open = []
    close = []
    for element in calculate:
        thigh, tlow, topen, tclose = element[0]
        high.append(thigh)
        low.append(tlow)
        open.append(topen)
        close.append(tclose)
    high.sort()
    low.sort()
    open.sort()
    close.sort()
    print("top:\t", str(sum(high[2:-2])/6), "\t", str(high[5]), "diff:\t", str((sum(high[2:-2])/6)-high[5]))
    print("low:\t", str(sum(low[2:-2])/6), "\t", str(low[5]), "diff:\t", str((sum(low[2:-2])/6)-low[5]))
    print("open:\t", str(sum(open[2:-2])/6), "\t", str(open[5]), "diff:\t", str((sum(open[2:-2])/6)-open[5]))
    print("close:\t", str(sum(close[2:-2])/6), "\t", str(close[5]), "diff:\t", str((sum(close[2:-2])/6)-close[5]))
    #total_min = str((time.time() - start)/60)
    #print("used that many min", total_min)
