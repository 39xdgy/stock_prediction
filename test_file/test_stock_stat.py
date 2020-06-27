import pandas_datareader as web
import matplotlib.pyplot as plt
import stockstats
import tushare as ts
plt.style.use('fivethirtyeight')

begin_time = '2018-01-01'
end_time = '2020-06-27'
name = 'LYFT'
stock = web.DataReader(name, data_source = 'yahoo', start = begin_time, end = end_time)
#stock = ts.get_hist_data('000001', start=begin_time, end=end_time)
#stock["date"] = stock.index.values
stock = stock.sort_index(0)
#print(stock)
#print(stock)
stockStat = stockstats.StockDataFrame.retype(stock)
print("init finish. ")
'''
stockStat[['close', 'kdjk', 'kdjd', 'kdjj']].plot()
plt.show()
'''
info_list = ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']
#print(stockStat[info_list])

check_list = ['macdh', 'kdjj', 'rsi_6']
for info in info_list:
    stock[info] = stockStat[[info]]

total_count = 0
true_count = 0
next_day = False
pred_macdh = 0
for title in check_list:
    total_count = 0
    true_count = 0
    next_day = False
    pred_macdh = 0
    for key in stock.index:
        gain = stock.loc[key]['close'] - stock.loc[key]['open']

        if next_day and gain >= 0:
            true_count += 1

        if title == 'macdh':
            if stock.loc[key][title] > 0:
                total_count += 1
                next_day = True
            else:
                next_day = False

        if title == 'kdjj':
            if stock.loc[key][title] < 0:
                next_day = True
                total_count += 1
            else:
                next_day = False

        if title == 'rsi_6':
            if stock.loc[key][title] < 20:
                next_day = True
                total_count += 1
            else:
                next_day = False
    print(title)
    print(total_count)
    print(true_count)
    print(true_count*100 / total_count)


#print(stock)
