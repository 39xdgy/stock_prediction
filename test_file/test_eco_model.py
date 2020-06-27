from stock_model_latest import stock_model_latest as sml
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

x = sml('AAPL', ('2018-01-01', '2020-06-20'), (1, 28, 120))


dataset = x.all_data
#print(dataset.index)
#print(dataset.loc['2020-06-18']['High'])
'''
for name in dataset.columns:
    print(name)
#print(dataset.columns)
'''


for date in dataset.index:
    high= dataset.loc[date]
    #print(high)


#print(x.all_data)
#print(x.all_data.loc['2019-04-18'])
#print(x.dataset)
h_i = 0
l_i = 1
o_i = 2
c_i = 3
# MACD calculation
DI_list = []
EMA12_list = []
EMA26_list = []
DIF_list = []  #快线
MACD_list = []  #慢线
OSC_list = []  #BAR
OSC_slope = []
for day_data in x.dataset:
    high, low, open, close = day_data
    DI = (high + low + (2*close))/4
    DI_list.append(DI)

day_count = 0

for DI in DI_list:
    if day_count == 11:
        EMA12 = sum(DI_list[0:12])/12
        EMA12_list.append(EMA12)
    elif day_count > 11:
        EMA12 = (EMA12_list[-1] * (11/13)) + (DI_list[day_count] * (2/13))
        EMA12_list.append(EMA12)

    if day_count == 25:
        EMA26 = sum(DI_list[0:26])/26
        EMA26_list.append(EMA26)
    elif day_count > 25:
        EMA26 = (EMA26_list[-1]*(25/27)) + (DI_list[day_count] * (2/27))
        EMA26_list.append(EMA26)

    day_count += 1

#print(len(EMA12_list))
#print(len(EMA26_list))
EMA12_list = EMA12_list[14:]

for index in range(0, len(EMA12_list)):
    DIF = EMA12_list[index] - EMA26_list[index]
    DIF_list.append(DIF)
    if index == 8:
        MACD = sum(DIF_list[0:9])/9
        MACD_list.append(MACD)
    elif index > 8:
        MACD = (MACD_list[-1]*(8/10)) + (DIF_list[index]*(2/10))
        MACD_list.append(MACD)

#print(DIF_list)
#print(MACD_list)
DIF_list = DIF_list[9:]

for i in range(0, len(DIF_list)): OSC_list.append(DIF_list[i] - MACD_list[i])
#print(OSC_list)

for i in range(1, len(OSC_list)): OSC_slope.append(OSC_list[i] - OSC_list[i-1])

#print(OSC_list)
#print(MACD_list)
#print(DIF_list)
'''
plt.title("MACD")
plt.plot(DIF_list)
plt.plot(MACD_list)
plt.show()

plt.title("OSC chart")
plt.plot(OSC_list)
plt.show()

plt.title("Slope Chart")
plt.plot(OSC_slope)
plt.show()
'''

#MACD calculation finished

#RSI calculation

RSI6_list = []
for i in range(5, len(x.dataset)):
    gain_total = 0
    loss_total = 0
    gain_count = 0
    loss_count = 0
    gain_radio = 0
    loss_radio = 0
    for j in range(0, 6):
        day_data = x.dataset[i-j]
        temp_gl = day_data[c_i] - day_data[o_i]
        if temp_gl > 0:
            gain_total += temp_gl
            gain_count += 1
        if temp_gl < 0:
            loss_total += temp_gl
            loss_count += 1

    if gain_count != 0: gain_radio = gain_total / gain_count
    if loss_count != 0:
        loss_radio = loss_total / loss_count
        loss_radio = -loss_radio

    RSI = (gain_radio / (gain_radio + loss_radio)) * 100
    RSI6_list.append(RSI)



RSI12_list = []
for i in range(11, len(x.dataset)):
    gain_total = 0
    loss_total = 0
    gain_count = 0
    loss_count = 0
    gain_radio = 0
    loss_radio = 0
    for j in range(0, 12):
        high, low, open, close = x.dataset[i-j]
        temp_gl = close - open
        if temp_gl > 0:
            gain_total += temp_gl
            gain_count += 1
        if temp_gl < 0:
            loss_total += temp_gl
            loss_count += 1

    if gain_count != 0: gain_radio = gain_total / gain_count
    if loss_count != 0:
        loss_radio = loss_total / loss_count
        loss_radio = -loss_radio

    RSI = (gain_radio / (gain_radio + loss_radio)) * 100
    RSI12_list.append(RSI)

#print(RSI12_list)


#print(len(RSI6_list), len(RSI12_list))
RSI6_list = RSI6_list[6:]

#print(len(RSI6_list) == len(RSI12_list))

RSI_diff_list = []

for i in range(0, len(RSI6_list)): RSI_diff_list.append(RSI6_list[i] - RSI12_list[i])


#RSI calculation finish

#KDJ calculation

RSV_list = []
for i in range(8, len(x.dataset)):
    low_list = []
    high_list = []
    final_close = 0
    for j in range(0, 9):
        index  = i - j
        high, low, open, close = x.dataset[index]
        low_list.append(low)
        high_list.append(high)
        if j == 8: final_close = close
    low_list.sort()
    high_list.sort()
    RSV = ((final_close - low_list[0])/(high_list[-1] - low_list[0]))*100
    RSV_list.append(RSV)

K_list = []
D_list = []
J_list = []

for i in range(0, len(RSV_list)):
    K = 0
    D = 0
    J = 0
    if i == 0:
        K = (100/3) + (1/3)*RSV_list[i]
        K_list.append(K)
        D = (100/3) + (1/3)*K_list[i]
        D_list.append(D)
    else:
        K = (2/3)*K_list[-1] + (1/3)*RSV_list[i]
        K_list.append(K)
        D = (2/3)*D_list[-1] + (1/3)*K_list[i]
        D_list.append(D)

    J = 3*D - 2*K
    J_list.append(J)



#KDJ calculation finished


'''
print("All length")
print("Total data length", len(x.dataset))
print("RSI6_list", len(RSI6_list))
print("RSI12_list", len(RSI12_list))
print("OSC_list", len(OSC_list))
print("OSC_slope", len(OSC_slope))
print("K", len(K_list))
print("D", len(D_list))
print("J", len(J_list))
'''
diff = len(RSI6_list) - len(OSC_slope)

#print(OSC_list)

diff_final_data = len(x.dataset) - len(OSC_slope)


# testing how accurate the data is
test_gain = 0
test_loss = 0

in_gain = False
for index in range(0, len(OSC_slope)):
    slope = OSC_slope[index]
    OSC = OSC_list[index+1]
    RSI6 = RSI6_list[index+35-12]
    RSI12 = RSI12_list[index+35-12]
    RSI_diff = RSI_diff_list[index+35-12]
    J = J_list[index+35-9]
    #if OSC < 0: OSC = -OSC
    if RSI6 < 50 and RSI12 < 50 and slope > 0:# and OSC > 0:     #正确率2/3
    #if OSC < 0: in_gain = False;
    #if OSC > 0:
    #if slope > 0:
    #if RSI < 50:
    #if slope > 0 and RSI_diff > 0:# and RSI6 < 50:
        in_gain = True
        index = OSC_slope.index(slope)
        temp_data = x.dataset[index + 35]
        diff_day = temp_data[c_i] - temp_data[o_i]
        if diff_day > 0: test_gain += 1
        elif diff_day < 0: test_loss += 1



'''
for day_data in x.dataset:
    diff_day = day_data[c_i] - day_data[o_i]
    if diff_day > 0: test_gain += 1
    if diff_day < 0: test_loss += 1
'''


print("Total number: ", str(test_gain+test_loss))
print("Days that earn money in prediction: ", str(test_gain))
print("Days that loss money in prediction: ", str(test_loss))
print("Rate: ", str(test_gain*100/(test_gain+test_loss)), "%")
