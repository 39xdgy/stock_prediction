from stock_info import stock_info as si
import pandas_datareader as web
from datetime import date
import time
#https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download

file_path = ".\companylist.csv"

wb = open(file_path, 'r')
pick_file = open('pick_file.txt', 'w')
title = wb.readline()
first = wb.readline()
'''
list_all = first.split("\"")
list_all = [e for e in list_all if e not in ('', ',')]
pick = si(str(list_all[0]), ("2018-01-01", date.today()))
output = pick.auto_run_output()
output_line = "Name:" + str(list_all[0]) + "\n\tprice: " + str(list_all[2]) + "\n\trate:"+ str(output[-2]) + "%\n"
#print(len(first.split(",")))
print(output_line)
'''
start = time.time()
doesnot_work_count = 0
total_stock = 0

for line in wb:
    list_all = line.split("\"")
    list_all = [e for e in list_all if e not in ('', ',')]
    total_stock += 1
    #print(list_all)

    #print(str(list_all[0]))
    #print(str(list_all[0]) == "TXG")
    try:
        pick = si(str(list_all[0]), ("2018-01-01", date.today()))
        output = pick.auto_run_output()
        if output[-1] and output[-2] > 70 and output[0] >= 50:
            output_line = "Name:" + str(list_all[0]) + "\n\tprice: " + str(list_all[2]) + "\n\tTotal test data: " + str(output[0]) +  "\n\trate:"+ str(output[-2]) + "%\n"
            pick_file.write(output_line)
            #print(putput_line)

    except:
        print("Did not work: ", str(list_all[0]))
        doesnot_work_count += 1

pick = si("AAPL", ("2018-01-01", "2020-06-06"))
output = pick.auto_run_output()
total_min = str((time.time() - start)/60)
print("used that many min", total_min)
print("In total there are", str(total_stock))
print("The number of stock did work:", str(total_stock - doesnot_work_count))
print("The number of stock did not work:", str(doesnot_work_count))
    #print(list_all)
