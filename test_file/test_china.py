import tushare as ts
import baostock as bs
from datetime import date
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


'''
TOKEN = 'd2d91d5981a4e6c58fc75e74eb518c166d883ab34fe2b7387dee75fb'
test = ts.get_hist_data('603888')
pro = ts.pro_api(token = TOKEN)
name_data = pro.stock_basic()
print(name_data[name_data['symbol'] == '603888']['name'])#.encode('utf-8'))

### terminal无法显示中文，必须要用idle或者tkinter来显示中文字符
### tushare有账号积分要求，读取缓慢，但是有中文股票名称


###baostock方便，容易读取，但是只有股票代号


'''

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
#print('login respond error_code:'+lg.error_code)
#print('login respond  error_msg:'+lg.error_msg)

#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
all = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
close = "close"
rs = bs.query_history_k_data_plus("sh.603888",
    close,
    start_date='2012-01-01', end_date=str(date.today()),
    frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

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


dataset = result.values
print(dataset)
