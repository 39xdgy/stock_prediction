import pandas_datareader as web
import stockstats


class pick_stock_tool:

    def __init__(self, name, date_range, info_list, check_list):
        self.begin_time, self.end_time = date_range
        self.stock = web.DataReader(name, data_source = 'yahoo', start = self.begin_time, end = self.end_time)
        stockStat = stockstats.StockDataFrame.retype(self.stock)
        self.info_list = info_list
        self.check_list = check_list
        self.last_date = str(self.stock.index[-1])[:10]
        #print(self.stock)
        for info in self.info_list:
            self.stock[info] = stockStat[[info]]

    def volume_check(self, miniumn_number):
        last_volumn = self.stock.loc[self.last_date]['volume']
        if last_volumn <= miniumn_number: return False
        return True


    def check_today_kdjj(self, flag = 5):
        last_j = self.stock.loc[self.last_date]['kdjj']
        #print(last_j)
        if last_j < flag:
            return True
        return False

    def accurate_kdjj(self, flag = 5):
        total_count = 0
        true_count = 0
        next_day = False
        for date in self.stock.index:
            gain = self.stock.loc[date]['close'] - self.stock.loc[date]['open']

            if next_day and gain >= 0:
                true_count += 1

            if self.stock.loc[date]['kdjj'] < flag:
                total_count += 1
                next_day = True
            else:
                next_day = False

        return (total_count, true_count, true_count*100/total_count)



    def check_today_macdh(self, flag = 0):
        last_macdh = self.stock.loc[self.last_date]['macdh']
        if last_macdh > flag:
            return True
        return False


    def accurate_macdh(self, flag = 0):
        total_count = 0
        true_count = 0
        next_day = False
        for date in self.stock.index:
            gain = self.stock.loc[date]['close'] - self.stock.loc[date]['open']

            if next_day and gain >= 0:
                true_count += 1

            if self.stock.loc[date]['macdh'] > flag:
                total_count += 1
                next_day = True
            else:
                next_day = False
        return (total_count, true_count, true_count*100/total_count)


    def check_today_macdh_slope(self, flag = 0):
        last_macdh = self.stock.loc[self.last_date]['macdh']
        last2_macdh = self.stock.loc[str(self.stock.index[-2])[:10]]['macdh']
        diff = last_macdh - last2_macdh
        if diff > flag: return True
        return False

    def accurate_macdh_slope(self, flag = 0):
        total_count = 0
        true_count = 0
        next_day = False
        pred_macdh = None
        for date in self.stock.index:
            gain = self.stock.loc[date]['close'] - self.stock.loc[date]['open']

            if next_day and gain >= 0:
                true_count += 1

            if pred_macdh == None:
                pred_macdh = self.stock.loc[date]['macdh']
                continue

            now_macdh = self.stock.loc[date]['macdh']

            if now_macdh - pred_macdh >= 0:
                total_count += 1
                next_day = True
            else:
                next_day = False

            pred_macdh = now_macdh

        return (total_count, true_count, true_count*100/total_count)




    def check_today_rsi_6(self, flag = 15):
        last_rsi_6 = self.stock.loc[self.last_date]['rsi_6']
        if last_rsi_6 < flag:
            return True
        return False


    def accurate_rsi_6(self, flag = 15):
        total_count = 0
        true_count = 0
        next_day = False
        for date in self.stock.index:
            gain = self.stock.loc[date]['close'] - self.stock.loc[date]['open']

            if next_day and gain >= 0:
                true_count += 1

            if self.stock.loc[date]['rsi_6'] < flag:
                total_count += 1
                next_day = True
            else:
                next_day = False

        return (total_count, true_count, true_count*100/total_count)

'''
x = pick_stock_tool('AAPL', ('2018-01-01', '2020-01-01'), ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14'], ['macdh', 'kdjj', 'rsi_6'])
x.check_today_kdjj()
x.accurate_kdjj()
print(x.volume_check(500000))
'''
