import pandas_datareader as web
import matplotlib.pyplot as plt
import stockstats
from datetime import date
import time
import tushare as ts
import sys
# insert at 1, 0 is the script path (or '' in REPL)
#a = 'C:\Users\39xdg\Desktop\git\stock_prodection\class_file'
sys.path.insert(1, "..\class_file")
from pick_stock_tool import pick_stock_tool


plt.style.use('fivethirtyeight')

file_path = "..\csv_file\companylist.csv"

wb = open(file_path, 'r')
today_date = str(date.today())
pick_file = open('..\\txt_file\{}_pick_file.txt'.format(today_date), 'w')
title = wb.readline()
start = time.time()
doesnot_work_count = 0
total_stock = 0

begin_time = '2018-01-01'
test_time = '2020-06-27'
info_list = ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']
#print(stockStat[info_list])

check_list = ['macdh', 'kdjj', 'rsi_6']

min_precentage = 70
for line in wb:
    list_all = line.split("\"")
    list_all = [e for e in list_all if e not in ('', ',')]
    #print(list_all[3])

    market_cap = list_all[3]
    if market_cap[-1] != 'B': continue
    market_cap_num = float(market_cap[1:-1])
    if market_cap_num < 2: continue
    try:
        stock = pick_stock_tool(list_all[0], (begin_time, today_date), info_list, check_list)
    except:
        continue
    if len(stock.stock.index) <= 50: continue


    total_stock += 1
    write_first = True

    if stock.check_today_kdjj():
        total_count, true_count, precentage = stock.accurate_kdjj()
        if precentage > min_precentage:
            if write_first:
                pick_file.write(list_all[0] + '\n')
                write_first = not write_first
            pick_file.write('\tkdj j\n\ttotal count is: {}\n\twork count is: {}\n\tprecentage: {}%\n\n'.format(total_count, true_count, precentage))




    if stock.check_today_macdh():
        total_count, true_count, precentage = stock.accurate_macdh()
        if precentage > min_precentage:
            if write_first:
                pick_file.write(list_all[0] + '\n')
                write_first = not write_first
            pick_file.write('\tmacdh\n\ttotal count is: {}\n\twork count is: {}\n\tprecentage: {}%\n\n'.format(total_count, true_count, precentage))


    if stock.check_today_macdh_slope():
        total_count, true_count, precentage = stock.accurate_macdh_slope()
        if precentage > min_precentage:
            if write_first:
                pick_file.write(list_all[0] + '\n')
                write_first = not write_first
            pick_file.write('\tmacdh slope\n\ttotal count is: {}\n\twork count is: {}\n\tprecentage: {}%\n\n'.format(total_count, true_count, precentage))



    if stock.check_today_rsi_6():
        total_count, true_count, precentage = stock.accurate_rsi_6()
        if precentage > min_precentage:
            if write_first:
                pick_file.write(list_all[0] + '\n')
                write_first = not write_first
            pick_file.write('\trsi 6\n\ttotal count is: {}\n\twork count is: {}\n\tprecentage: {}%\n\n'.format(total_count, true_count, precentage))



total_min = str((time.time() - start)/60)
print("used that many min", total_min)
print("Total number of stock that run over: ", total_stock)
#print(stock)
