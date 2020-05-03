from stock_model import stock_model
from datetime import date

stock_list_file = open("stock_list.txt", "r")
stock_list = stock_list_file.read().split("\n")
#print(stock_list)
stock_list_file.close()

start_date = "2012-01-01"
today = str(date.today())
#yeasterday = today
#yeasterday = yeasterday[:-1] + str(int(yeasterday[-1])-1)
#print(yeasterday)

report_file = open("report.txt", "w")
for stock in stock_list:
    for i in range(0, 5):
        if(stock[0] != "#"):
            Brain = stock_model(stock, (start_date, today))
            #print(Brain.data)
            report_line = Brain.create_report()
            report_file.write(report_line)
            report_file.write("\n")

report_file.close()
