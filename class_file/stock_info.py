import pandas_datareader as web
from day_info import day_info as di
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

class stock_info:

    def __init__(self, stock_name, time_range):
        self.stock_name = stock_name
        self.start_time, self.end_time = time_range
        data = web.DataReader(self.stock_name, data_source = 'yahoo', start = self.start_time, end = self.end_time)
        self.data_list = ['High', 'Low', 'Open', 'Close']
        self.main_data_dic = {}
        self.suggestion = []
        data.filter(self.data_list)
        for date in data.index:
            High, Low, Open, Close = data.loc[date][self.data_list]
            temp_di = di(High, Low, Open, Close)
            self.main_data_dic[str(date)[0:10]] = temp_di


    def MACD_update(self):
        day_count = 1
        MACD_count = 1
        use_data_12 = []
        use_data_26 = []
        use_data_MACD = []
        pred_key_12 = None
        pred_key_26 = None
        pred_key_MACD = None
        OSC_slope_flag = False
        for key in self.main_data_dic:
            day_data = self.main_data_dic[key]
            EMA12 = None
            EMA26 = None
            DIF = None
            MACD = None
            OSC = None
            OSCS = None
            if day_count <= 12:
                use_data_12.append(self.main_data_dic[key].DI)
            if day_count == 12:
                EMA12 = sum(use_data_12)/12
                self.main_data_dic[key].set_EMA12(EMA12)
                pred_key_12 = key
            if day_count > 12:
                EMA12 = (self.main_data_dic[pred_key_12].EMA12 * 11/13) + (day_data.DI * 2/13)
                self.main_data_dic[key].set_EMA12(EMA12)
                pred_key_12 = key

            if day_count <= 26:
                use_data_26.append(self.main_data_dic[key].DI)
            if day_count == 26:
                EMA26 = sum(use_data_26)/26
                self.main_data_dic[key].set_EMA26(EMA26)
                pred_key_26 = key
            if day_count > 26:
                EMA26 = (self.main_data_dic[pred_key_26].EMA26 * 25/27) + (day_data.DI * 2/27)
                self.main_data_dic[key].set_EMA26(EMA26)
                pred_key_26 = key

            if day_count >= 26:
                DIF = self.main_data_dic[key].EMA12 - self.main_data_dic[key].EMA26
                self.main_data_dic[key].set_DIF(DIF)


            if self.main_data_dic[key].DIF != None:
                if MACD_count <= 9:
                    use_data_MACD.append(self.main_data_dic[key].DIF)
                if MACD_count == 9:
                    MACD = sum(use_data_MACD)/9
                    self.main_data_dic[key].set_MACD(MACD)

                if MACD_count > 9:
                    MACD = (self.main_data_dic[pred_key_MACD].MACD*8/10) + (self.main_data_dic[key].DIF*2/10)
                    self.main_data_dic[key].set_MACD(MACD)
                    OSC_slope_flag = True

                if MACD_count >= 9:
                    OSC = DIF - MACD
                    self.main_data_dic[key].set_OSC(OSC)

                if OSC_slope_flag:
                    OSCS = self.main_data_dic[pred_key_MACD].OSC - OSC
                    self.main_data_dic[key].set_OSCS(OSCS)
                pred_key_MACD = key
                MACD_count += 1
            day_count += 1
        print(use_data_MACD)


    def RSI_calculate(self, use_data, last_RSI):
        gain_total = 0
        loss_total = 0
        gain_count = 0
        loss_count = 0
        gain_radio = 0
        loss_radio = 0
        RSI = 0
        for value in use_data:
            if value > 0:
                gain_total += value
                gain_count += 1
            else:
                loss_total += value
                loss_count += 1
        loss_total = -loss_total
        if gain_count != 0: gain_radio = gain_total/gain_count
        if loss_count != 0: loss_radio = loss_total/loss_count
        if gain_radio + loss_radio != 0: RSI = (gain_radio / (gain_radio + loss_radio)) * 100
        else: RSI = last_RSI
        return RSI

    def RSI_update(self):
        use_data_6 = []
        use_data_12 = []
        RSI6, RSI12 = [0, 0]
        last_RSI6, last_RSI12 = [0, 0]
        for key in self.main_data_dic:
            temp_gl = self.main_data_dic[key].close - self.main_data_dic[key].open
            #print("Date", key, "close: ", self.main_data_dic[key].close,"open: ", self.main_data_dic[key].open)
            use_data_6.append(temp_gl)
            use_data_12.append(temp_gl)
            if len(use_data_6) == 6:
                RSI6 = self.RSI_calculate(use_data_6, last_RSI6)
                self.main_data_dic[key].set_RSI6(RSI6)
                use_data_6 = use_data_6[1:]
                last_RSI6 = RSI6
            if len(use_data_12) == 12:
                RSI12 = self.RSI_calculate(use_data_12, last_RSI12)
                self.main_data_dic[key].set_RSI12(RSI12)
                self.main_data_dic[key].set_RSI_diff(RSI6 - RSI12)
                last_RSI12 = RSI12
                use_data_12 = use_data_12[1:]

    def KDJ_update(self):
        RSV_low = []
        RSV_high = []
        pred_key = None
        K, D, J = [0, 0, 0]
        for key in self.main_data_dic:
            day_value = self.main_data_dic[key]
            RSV_low.append(day_value.low)
            RSV_high.append(day_value.high)
            if (len(RSV_low) == 9):
                sorted_low = sorted(RSV_low)
                sorted_high = sorted(RSV_high)
                RSV = ((day_value.close - sorted_low[0])/(sorted_high[-1] - sorted_low[0]))*100
                self.main_data_dic[key].set_RSV(RSV)
                RSV_low = RSV_low[1:]
                RSV_high = RSV_high[1:]
                if pred_key == None:
                    K = (100/3) + (1/3)*RSV
                    self.main_data_dic[key].set_K(K)
                    D = (100/3) + (1/3)*K
                    self.main_data_dic[key].set_D(D)
                else:
                    K = (2/3)*self.main_data_dic[pred_key].K + (1/3)*RSV
                    self.main_data_dic[key].set_K(K)
                    D = (2/3)*self.main_data_dic[pred_key].D + (1/3)*K
                    self.main_data_dic[key].set_D(D)

                J = 3*D - 2*K
                self.main_data_dic[key].set_J(J)
                print(J)
                pred_key = key


    def auto_run_output(self):
        self.MACD_update()
        self.RSI_update()
        self.KDJ_update()
        fin = self.run_output()
        return fin

    def run_output(self):
        gain_count = 0
        loss_count = 0

        pred_key = None
        get_flag = False
        RSI_diff_list = []
        '''更改方向: 通过今天的数值去抓取下一天的情况'''
        for key in self.main_data_dic:
            value = self.main_data_dic[key]
            flag_list = value.get_all_flag()
            #print(flag_list)

            if get_flag:
                value = self.main_data_dic[pred_key]
                real_out = value.close - value.open
                #print("in pred gain day")
                if real_out > 0: gain_count += 1
                else: loss_count += 1

            if None not in flag_list:
                #print("None not in flag_list")
                EMA12, EMA26, DIF, MACD, OSC, OSCS, RSI6, RSI12, RSI_diff, RSV, K, D, J = flag_list
                RSI_diff_list.append(RSI_diff)
                RSI_diff = RSI6 - RSI12
                #if OSC > 0:
                if J < 20:# and RSI12 < 50:#DIF > 0 and OSC > 0 and RSI12 < 50:
                #if K < 30 and D < 30:
                    get_flag = True
                    '''
                    value = self.main_data_dic[pred_key]
                    real_out = value.close - value.open
                    #print("in pred gain day")
                    if real_out > 0: gain_count += 1
                    else: loss_count += 1
                    '''
                else:
                    get_flag = False
            pred_key = key
        '''
        plt.title("RSI diff")
        plt.plot(RSI_diff_list)
        plt.show()
        '''
        '''
        print("Total number: ", str(gain_count+loss_count))
        print("Days that earn money in prediction: ", str(gain_count))
        print("Days that loss money in prediction: ", str(loss_count))
        print("Rate: ", str(gain_count*100/(gain_count+loss_count)), "%")
        '''
        last_day = list(self.main_data_dic.keys())[-1]
        last_day = self.main_data_dic[last_day]
        EMA12, EMA26, DIF, MACD, OSC, OSCS, RSI6, RSI12, RSI_diff, RSV, K, D, J = value.get_all_flag()
        will_earn = False
        if J < 20:
            will_earn = True
        suggestion = [gain_count+loss_count, gain_count, loss_count, gain_count*100/(gain_count+loss_count), will_earn]
        return suggestion

    def print_output(self, suggestion):
        print("Total number: ", str(suggestion[0]))
        print("Days that earn money in prediction: ", str(suggestion[1]))
        print("Days that loss money in prediction: ", str(suggestion[2]))
        print("Rate: ", str(suggestion[3]), "%")
        print("should pick: ", suggestion[4])


x = stock_info('LYFT', ('2018-01-01', '2020-06-27'))
x.auto_run_output()
