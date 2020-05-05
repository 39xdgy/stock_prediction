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

        self.wn = tk.Tk()
        self.Add_wn = tk.Tk()
        self.Add_wn.withdraw()
        self.main_screen()


    def update_stock_list(self):
        stock_list_file = open("stock_list.txt", "w")
        for stock in self.stock_list:
            line = stock + "\n"
            stock_list_file.write(line)
        stock_list_file.close()


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

    def main_screen(self):
        self.wn.title('Stock Prodection')
        self.center(self.wn, self.wn_width, self.wn_height)
        buttom_font = font.Font(size = 20)


        temp_x = 1
        temp_y = 1
        dict_stock = {}
        for stock_name in self.stock_list:

            dict_stock[stock_name] = temp_var = tk.IntVar()
            temp_checkbox = tk.Checkbutton(self.wn, text = stock_name, variable = temp_var, onvalue = 1, offvalue = 0)
            #pos = str(temp_x)+"x"+str(temp_y)

            temp_checkbox.grid(column = temp_x, row = temp_y, padx=10, pady=10)
            if(temp_x == 6):
                temp_x = 1
                temp_y += 1
            else:
                temp_x += 1


        Add_buttom = tk.Button(self.wn, text = "Add Stock", height = 2, width = 10, command = self.Add_clicked)
        Add_buttom.place(x = 100, y = 280)

        Run_buttom = tk.Button(self.wn, text = "Run", height = 2, width = 10, command = lambda: self.run_clicked(dict_stock))
        Run_buttom.place(x = 200, y = 280)

        setting_buttom = tk.Button(self.wn, text = "Setting", height = 2, width = 10)
        setting_buttom.place(x = 300, y = 280)

        self.wn.protocol("WM_DELETE_WINDOW", self.close_all)
        self.wn.mainloop()


    def run_clicked(self, dict_stock):
        start_date = "2012-01-01"
        today = str(date.today())
        report_file = open("report.txt", "w")
        self.wn.withdraw()
        msg.showinfo("Program start", "开始预测")
        for stock_name in self.stock_list:
            if(dict_stock[stock_name].get() == 1):
                print("now running: " + stock_name)
                for i in range(0, 5):
                    Brain = stock_model(stock_name, (start_date, today))
                    #print(Brain.data)
                    report_line = Brain.create_report()
                    report_file.write(report_line)
                    report_file.write("\n")
                report_file.write('\n')

        msg.showinfo('Success', '恭喜你，你要发了！')

        report_file.close()
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
