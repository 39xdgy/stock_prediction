import tkinter as tk
import tkinter.font as font
from tkinter import messagebox as msg
import pandas_datareader as web
from datetime import date
from stock_model_latest import stock_model_latest as sml

class GUI:

    def __init__(self):
        self.wn_width = 480
        self.wn_height = 360
        self.Add_width = 360
        self.Add_height = 60

        self.today = str(date.today())
        self.finish = False
        stock_list_file = open("..\\txt_file\stock_list.txt", "r")
        self.stock_list = stock_list_file.read().split("\n")
        self.stock_list.remove('')
        stock_list_file.close()
        self.dict_stock = {}
        self.wn = tk.Tk()
        self.wn.withdraw()
        self.Add_wn = tk.Tk()
        self.Add_wn.withdraw()
        self.debug_wn = tk.Tk()
        self.debug_wn.withdraw()
        self.loading_wn = tk.Tk()
        self.loading_wn.withdraw()
        self.select_all_var = tk.IntVar()
        self.clear_var = tk.IntVar()
        self.report_data = {}
        self.debug_flag = False
        self.pred_day = ''
        self.loading_log_listbox = ''
        self.loading_log_line = 'Start Predicting\n'



        self.draw_wn()
        self.draw_add_wn()
        #self.draw_debug_wn()
        self.draw_loading_wn()
        #self.main_screen()


    def update_stock_list(self):
        stock_list_file = open("..\\txt_file\stock_list.txt", "w")
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

    def close_debug(self):
        self.wn.deiconify()
        self.debug_wn.withdraw()

    def close_all(self):
        self.wn.withdraw()
        self.Add_wn.destroy()
        self.wn.destroy()
        self.debug_wn.destroy()
        self.wn.quit()

    def draw_checkbox(self):
        checkbox_x = 1
        checkbox_y = 2
        for stock_name in self.stock_list:
            if stock_name not in self.dict_stock:
                temp_var = tk.IntVar()
                self.dict_stock[stock_name] = (tk.Checkbutton(self.wn, text = stock_name, variable = temp_var), temp_var)
                self.dict_stock[stock_name][0].grid(column = checkbox_x, row = checkbox_y, padx=10, pady=10)
            if(checkbox_x == 6):
                checkbox_x = 1
                checkbox_y += 1
            else:
                checkbox_x += 1


    def select_all_checked(self, auto = False):
        print(self.select_all_var.get())
        temp_auto = auto
        for box in self.dict_stock:
            if self.select_all_var.get() == 1 or temp_auto:
                self.dict_stock[box][0].select()
            else:
                self.dict_stock[box][0].deselect()


    def clear_checked(self):
        for box in self.dict_stock:
            self.dict_stock[box][0].deselect()

    def is_today_out(self):
        temp = web.DataReader("AAPL", data_source = 'yahoo', start = "2020-05-31", end = date.today())
        return (str(date.today()) == str(temp.index[-1])[:10])

    def draw_wn(self):
        self.wn.title('Stock Prodection')
        self.center(self.wn, self.wn_width, self.wn_height)
        buttom_font = font.Font(size = 20)


        self.draw_checkbox()


        select_all = tk.Checkbutton(self.wn, text = "select all", variable = self.select_all_var, onvalue = 1, offvalue = 0, command = self.select_all_checked)
        clear = tk.Checkbutton(self.wn, text = "clear", variable = self.clear_var, onvalue = 1, offvalue = 0, command = self.clear_checked)
        select_all.grid(sticky = "n", column = 1, row = 1)
        clear.grid(sticky = "n", column = 2, row = 1)

        today_update = ''
        if self.is_today_out(): today_update = tk.Label(self.wn, text = 'Can predict next day.', fg = 'Green')
        else: today_update = tk.Label(self.wn, text = 'Please keep waiting.', fg = 'Red')

        today_update.place(x = 350, y = 7)



        Add_buttom = tk.Button(self.wn, text = "Add Stock", height = 2, width = 10, command = self.Add_clicked)
        Add_buttom.place(x = 50, y = 280)

        Run_buttom = tk.Button(self.wn, text = "Run", height = 2, width = 10, command = self.run_clicked)
        Run_buttom.place(x = 150, y = 280)

        self.prodect_buttom = tk.Button(self.wn, text = "Prodect", height = 2, width = 10, command = self.prodect_clicked)
        self.prodect_buttom.place(x = 250, y = 280)

        setting_buttom = tk.Button(self.wn, text = 'debug', height = 2, width = 10, command = self.debug_clicked)#"Setting", height = 2, width = 10)
        setting_buttom.place(x = 350, y = 280)

        debug_buttom = tk.Button(self.wn, text = "model_data", height = 1, width = 10, command = self.debug_clicked)
        debug_buttom.place(x = 395, y = 330)



    def draw_add_wn(self):
        self.Add_wn.title('Add Stock')
        self.center(self.Add_wn, self.Add_width, self.Add_height)

        Add_txt = tk.Entry(self.Add_wn, width = 30)
        Add_txt.place(x = 30, y = 15)

        Add_confirm = tk.Button(self.Add_wn, text = "confirm", height = 1, width = 7, command = lambda: self.add_stock(Add_txt))
        Add_confirm.place(x = 260, y = 13)

        self.Add_wn.protocol("WM_DELETE_WINDOW", self.close_add)




    def draw_debug_wn(self):
        self.debug_wn.title('debug window')
        self.center(self.debug_wn, self.wn_width, self.wn_height)

        debug_on_label = tk.Label(self.debug_wn, text = "debug mode: ")
        debug_on_label.place(x = 30, y = 30)

        debug_on_button = tk.Button(self.debug_wn, text = "On", command = self.debug_on)
        debug_on_button.place(x = 250, y = 30)

        debug_off_button = tk.Button(self.debug_wn, text = "Off", command = self.debug_off)
        debug_off_button.place(x = 380, y = 30)

        debug_day_label = tk.Label(self.debug_wn, text = "final training day: ")
        debug_day_label.place(x = 30, y = 90)

        self.debug_day = tk.Entry(self.debug_wn, width = 30, state = tk.DISABLED)
        self.debug_day.place(x = 200, y = 90)

        debug_pred_label = tk.Label(self.debug_wn, text = "The day you want to predict: ")
        debug_pred_label.place(x = 30, y = 120)

        self.debug_pred_day = tk.Entry(self.debug_wn, width = 30, state = tk.DISABLED)
        self.debug_pred_day.place(x = 200, y = 120)


        debug_confirm = tk.Button(self.debug_wn, text = "confirm", height = 1, width = 7, command = self.debug_done)
        debug_confirm.place(x = 410, y = 320)



    def debug_checked(self, debug_var):
        print(debug_var.get())


    def draw_loading_wn(self):
        self.center(self.loading_wn, self.wn_width, self.wn_height)
        self.loading_wn.title("Running")

        self.loading_log_scroll = tk.Scrollbar(self.loading_wn)
        self.loading_log_scroll.pack(side = tk.RIGHT, fill = tk.Y)


        self.loading_log_listbox = tk.Listbox(self.loading_wn, bg = "White", yscrollcommand = self.loading_log_scroll.set, width = 75, height = 21)
        self.loading_log_listbox.place(x = 2, y = 5)


    def main_screen(self):
        self.wn.deiconify()

        self.wn.protocol("WM_DELETE_WINDOW", self.close_all)
        self.wn.update()
        self.wn.mainloop()


    def prodect_clicked(self):
        file_name = "..\\txt_file\\" + self.today + "_report.txt"
        report_file = open(file_name, 'w')
        for stock in self.report_data:
            predict_data = self.report_data[stock]
            stock, filter_area = stock.split('_')
            data_today = web.DataReader(stock, data_source = 'yahoo', start = "2020-07-01", end = self.today).filter([filter_area])
            today_data = str(data_today[filter_area][-1])
            avg = self.avg_output(predict_data)
            mid = self.mid_output(predict_data)
            diff = avg - mid
            line = stock + "_" + filter_area + ": " + today_data + "\n\tavg: " + str(avg) + "\n\tmid: " + str(mid) + "\n\tdiff: " + str(diff) + "\n" # "\n\tmax_avg: " + max_avg + "\n"
            report_file.write(line)
            report_file.write("\n")
        report_file.close()
        self.prodect_buttom['state'] = tk.DISABLED



    def avg_output(self, predict_data):
        predict_data.sort()
        return (sum(predict_data[2:-2])/6)

    def mid_output(self, predict_data):
        predict_data.sort()
        return predict_data[4]

    def run_clicked(self):
        self.wn.withdraw()

        msg.showinfo("Program start", "开始预测")
        self.loading_wn.deiconify()

        self.loading_wn.after(500, self.main_logic_brain_create)
        self.loading_wn.update()
        self.loading_wn.mainloop()
        #msg.showinfo('Success', 'Your are going to be rich. ')


        #self.wn.deiconify()

    def main_logic_brain_create(self):
        start_date = "2018-01-01"
        file_name = "..\\txt_file\\" + self.today + "_log.txt"
        log_file = open(file_name, "w")
        self.loading_log_listbox.insert(tk.END, "Start Predicting")
        self.loading_log_scroll.config(command = self.loading_log_listbox.yview)
        self.loading_wn.update()
        for stock_name in self.stock_list:
            if(self.dict_stock[stock_name][1].get() == 1):
                temp = "now running: " + stock_name
                self.loading_log_listbox.insert(tk.END, temp)
                self.loading_log_scroll.config(command = self.loading_log_listbox.yview)
                self.loading_wn.update()
                temp_report_data = []
                for i in range(0, 10):
                    Brain = sml(stock_name, (start_date, self.today), (1, 20, 60), 'Low')#, 'Close')
                    Brain.create_brain()
                    Brain.use_brain()
                    report_line = Brain.create_report()
                    log_file.write(report_line)
                    log_file.write("\n")
                    temp_report_data.append(Brain.pred_price[0, 0])
                log_file.write('\n')
                save_name = stock_name + "_Low"
                self.report_data[save_name] = temp_report_data
                temp_report_data = []
                for i in range(0, 10):
                    Brain = sml(stock_name, (start_date, self.today), (1, 20, 60), 'Close')#, 'Close')
                    Brain.create_brain()
                    Brain.use_brain()
                    report_line = Brain.create_report()
                    log_file.write(report_line)
                    log_file.write("\n")
                    temp_report_data.append(Brain.pred_price[0, 0])
                log_file.write('\n')
                save_name = stock_name + "_Close"
                self.report_data[save_name] = temp_report_data
        log_file.close()
        self.loading_wn.withdraw()
        self.loading_wn.destroy()
        self.wn.deiconify()


    def Add_clicked(self):
        self.wn.withdraw()
        self.Add_wn.deiconify()

        self.Add_wn.protocol("WM_DELETE_WINDOW", self.close_add)
        self.Add_wn.mainloop()


    def debug_clicked(self):
        self.wn.withdraw()
        self.debug_wn.deiconify()

        self.debug_wn.protocol("WM_DELETE_WINDOW", self.close_debug)
        self.debug_wn.update()
        self.debug_wn.mainloop()


    def debug_on(self):
        #print("debug on")
        self.debug_flag = True
        self.debug_day['state'] = tk.NORMAL
        self.debug_pred_day['state'] = tk.NORMAL


    def debug_off(self):
        self.debug_flag = False
        self.debug_day['state'] = tk.DISABLED
        self.debug_pred_day['state'] = tk.DISABLED


    def debug_done(self):#, debug_day):
        if self.debug_flag:
            self.today = self.debug_day.get()
            self.pred_day = self.debug_pred_day.get()
            msg.showinfo("debug info", "Enter debug mode")
            self.debug_wn.withdraw()
            self.wn.title('Stock Prodection(debug mode)')
        else:
            msg.showinfo("debug info", "Exit debug mode")
            self.wn.title('Stock Prodection')
        self.wn.deiconify()

    def add_stock(self, Add_txt):
        stock_name = str(Add_txt.get()).upper()
        try:
            df = web.DataReader(stock_name, data_source = 'yahoo')
            self.Add_wn.withdraw()
            if stock_name not in self.stock_list:
                self.stock_list.append(stock_name)
                msg.showinfo('Success', 'Successfully add stock into the list.')
                self.update_stock_list()
            else:
                msg.showinfo('Already exist', 'This stock already exist in the list.')
        except Exception as e:
            #print(e)
            msg.showinfo('Error', 'The name does not exist. ')

        self.draw_checkbox()

        self.wn.deiconify()


if __name__ == "__main__":
    x = GUI()
    x.main_screen()
