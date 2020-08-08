import pandas_datareader as web
import stockstats
from datetime import date
import time

file_path = "..\csv_file\companylist.csv"

wb = open(file_path, 'r')
pick_file = open('pick_file.txt', 'w')
title = wb.readline()
first = wb.readline()

start = time.time()
doesnot_work_count = 0
total_stock = 0
info_list = ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']
check_list = ['macdh', 'kdjj', 'rsi_6']

#pred_macd = 0
for line in wb:
    list_all = line.split("\"")
    list_all = [e for e in list_all if e not in ('', ',')]
    total_stock += 1
    #print(list_all[0])
    try:
        stock = web.DataReader(list_all[0], data_source = 'yahoo', start = '2018-01-01', end = '2020-06-26')
        #print(stock)
    except:
        print(list_all[0])
        continue
    '''
    if stock.loc[-1]['volumn'] <= 500000:
        continue
    '''
    stockStat = stockstats.StockDataFrame.retype(stock)
    info_list = ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']
    stockStat = stockStat[info_list]
    for info in info_list:
        stock[info] = stockStat[[info]]

    for title in check_list:
        total_count = 0
        true_count = 0
        next_day = False
        pred_macdh = 0
        try:
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
            '''
            print(title)
            print(total_count)
            print(true_count)
            print(true_count*100 / total_count)
            '''
        except:
            print("Fail: ", list_all[0])
            doesnot_work_count += 1


total_min = str((time.time() - start)/60)
print("cost time: ", total_min)
'''
    #print(stockStat)
    #print(stockStat[info_list])
    for key in stock.index:
        #print(key)
        #print(stock.loc[key])
        print(stockStat['macd'][-1])
'''
