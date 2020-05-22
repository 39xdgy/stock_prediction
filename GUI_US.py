import tkinter as tk
import tkinter.font as font
from tkinter import messagebox as msg
import pandas_datareader as web
from datetime import date
from stock_model import stock_model

class GUI_US:

    def __init__(self):
        self.wn_width = 480
        self.wn_height = 360
        self.Add_width = 360
        self.Add_height = 60

        self.finish = False
        stock_list_file = open("stock_list.txt", "r")
        self.stock_list = stock_list_file.read().split("\n")
        self.stock_list.remove('')
        stock_list_file.close()
        self.dict_stock = {}
        self.wn = tk.Tk()
        self.Add_wn = tk.Tk()
        self.Add_wn.withdraw()

        self.select_all_var = tk.IntVar()
        self.clear_var = tk.IntVar()
        #self.draw_checkbox()
        self.report_data = {}
        self.main_screen()


    def update_stock_list(self):
        stock_list_file = open("stock_list.txt", "w")
        for stock in self.stock_list:
            line = stock + "\n"
            stock_list_file.write(line)
        stock_list_file.close()
        self.draw_checkbox()


    def center(self, toplevel, width, height):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        x = (w - width) // 2
        y = (h - height) // 2
        '''format = width x height + left_top_width + left_top_height'''
        toplevel.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def close_add(self):
        self.wn.deiconify()
        self.Add_wn.withdraw()


    def close_all(self):
        self.wn.withdraw()
        self.Add_wn.destroy()
        self.wn.destroy()
        self.wn.quit()

    def draw_checkbox(self):
        checkbox_x = 1
        checkbox_y = 2
        for stock_name in self.stock_list:
            if stock_name not in self.dict_stock:
                temp_var = tk.IntVar()
                self.dict_stock[stock_name] = (tk.Checkbutton(self.wn, text = stock_name, variable = temp_var), temp_var)
                #temp_checkbox = tk.Checkbutton(self.wn, text = stock_name, variable = self.dict_stock[stock_name])
            #pos = str(temp_x)+"x"+str(temp_y)

                self.dict_stock[stock_name][0].grid(column = checkbox_x, row = checkbox_y, padx=10, pady=10)
                if(checkbox_x == 6):
                    checkbox_x = 1
                    checkbox_y += 1
                else:
                    checkbox_x += 1
            #elif self.select_all.variable == 1:


    def select_all_checked(self):
        for box in self.dict_stock:
            if self.select_all_var.get() == 1:
                self.dict_stock[box][0].select()
            else:
                self.dict_stock[box][0].deselect()

    def clear_checked(self):
        for box in self.dict_stock:
            self.dict_stock[box][0].deselect()

    def main_screen(self):
        self.wn.title('Stock Prodection')
        self.center(self.wn, self.wn_width, self.wn_height)
        buttom_font = font.Font(size = 20)


        self.draw_checkbox()


        select_all = tk.Checkbutton(self.wn, text = "select all", variable = self.select_all_var, onvalue = 1, offvalue = 0, command = self.select_all_checked)
        clear = tk.Checkbutton(self.wn, text = "clear", variable = self.clear_var, onvalue = 1, offvalue = 0, command = self.clear_checked)
        select_all.grid(sticky = "n", column = 1, row = 1)
        clear.grid(sticky = "n", column = 2, row = 1)


        Add_buttom = tk.Button(self.wn, text = "Add Stock", height = 2, width = 10, command = self.Add_clicked)
        Add_buttom.place(x = 50, y = 280)

        Run_buttom = tk.Button(self.wn, text = "Run", height = 2, width = 10, command = self.run_clicked)
        Run_buttom.place(x = 150, y = 280)

        prodect_buttom = tk.Button(self.wn, text = "Prodect", height = 2, width = 10, command = self.prodect_clicked)
        prodect_buttom.place(x = 250, y = 280)

        setting_buttom = tk.Button(self.wn, text = "Setting", height = 2, width = 10)
        setting_buttom.place(x = 350, y = 280)


        self.wn.protocol("WM_DELETE_WINDOW", self.close_all)
        self.wn.mainloop()


    def prodect_clicked(self):
        today = str(date.today())
        file_name = today + "_report.txt"
        report_file = open(file_name, 'w')
        for stock in self.report_data:
            #print(stock)
            predict_data = self.report_data[stock]
            data_today = web.DataReader(stock, data_source = 'yahoo', start = today, end = today).filter(['Close'])
            today_close = str(data_today['Close'][0])
            avg = 0
            rng_avg = 0
            lease_avg = 0
            max_avg = 0
            for i in predict_data:
                avg += i[0]
                rng_avg += i[1]
                lease_avg += (i[0]-i[1])
                max_avg += (i[0]+i[1])
            avg = str(avg/5)
            rng_avg = str(rng_avg/5)
            lease_avg = str(lease_avg/5)
            max_avg = str(max_avg/5)
            line = stock + ": " + today_close + "\n\tavg: " + avg + "\n\tRange_avg: " + rng_avg + "\n\tlease_avg: " + lease_avg + "\n\tmax_avg: " + max_avg + "\n"
            report_file.write(line)
            report_file.write("\n")
        report_file.close()





    def run_clicked(self):
        start_date = "2012-01-01"
        today = str(date.today())
        file_name = today + "_log.txt"
        log_file = open(file_name, "w")
        self.wn.withdraw()
        msg.showinfo("Program start", "开始预测")
        for stock_name in self.stock_list:
            if(self.dict_stock[stock_name][1].get() == 1):
                print("now running: " + stock_name)
                temp_report_data = []
                for i in range(0, 5):
                    Brain = stock_model(stock_name, (start_date, today))
                    #print(Brain.data)
                    Brain.create_brain()
                    while Brain.rmse >= 5:
                        print("rmse大于5， 重新训练:", Brain.rmse)
                        Brain = stock_model(stock_name, (start_date, today))
                        Brain.create_brain()
                    Brain.use_brain()
                    report_line = Brain.create_report()
                    log_file.write(report_line)
                    log_file.write("\n")
                    temp_report_data.append((Brain.pred_price, Brain.rmse))
                log_file.write('\n')
                self.report_data[stock_name] = tuple(temp_report_data)

        msg.showinfo('Success', 'Your are going to be rich. ')

        log_file.close()
        #print(self.report_data)
        self.wn.deiconify()


    def Add_clicked(self):
        self.wn.withdraw()
        self.Add_wn.deiconify()
        self.Add_wn.title('Add Stock')
        self.center(self.Add_wn, self.Add_width, self.Add_height)

        Add_txt = tk.Entry(self.Add_wn, width = 30)
        Add_txt.place(x = 30, y = 15)

        Add_confirm = tk.Button(self.Add_wn, text = "confirm", height = 1, width = 7, command = lambda: self.add_stock(Add_txt))
        Add_confirm.place(x = 260, y = 13)

        self.Add_wn.protocol("WM_DELETE_WINDOW", self.close_add)
        self.Add_wn.mainloop()


    def add_stock(self, Add_txt):
        stock_name = str(Add_txt.get()).upper()
        try:
            df = web.DataReader(stock_name, data_source = 'yahoo')
            self.Add_wn.withdraw()
            #self.Add_wn.destroy()
            if stock_name not in self.stock_list:
                self.stock_list.append(stock_name)
                msg.showinfo('Success', 'Successfully add stock into the list.')
                self.update_stock_list()
            else:
                msg.showinfo('Already exist', 'This stock already exist in the list.')
        except Exception as e:
            #print(e)
            msg.showinfo('Error', 'The name does not exist. ')

        self.wn.update()
        self.wn.deiconify()


x = GUI_US()
