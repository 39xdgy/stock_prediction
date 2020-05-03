import tkinter as tk
import tkinter.font as font
from tkinter import messagebox as msg
import pandas_datareader as web

wn_width = 480
wn_height = 360
wn_size = str(wn_width) + "x" + str(wn_height)

Add_width = 360
Add_height = 60
Add_size = str(Add_width) + "x" + str(Add_height)


def center(toplevel, width, height):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    #size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = (w - width) // 2
    y = (h - height) // 2
    '''format = width x height + left_top_width + left_top_height'''
    toplevel.geometry("{}x{}+{}+{}".format(width, height, x, y))#("%dx%d+%d+%d" % (size + (x, y)))


def add_stock(wn, Add_wn, Add_txt):
    try:
        df = web.DataReader(Add_txt.get(), data_source = 'yahoo')#, start = '2016-01-01', end = '2020-04-25')
        Add_wn.quit()
        Add_wn.destroy()
        msg.showinfo('Success', 'Successfully add stock into the list')
        wn.update()
        wn.deiconify()
    except:
        msg.showinfo('Error', 'The name does not exist. ')

def Add_clicked(wn):
    wn.withdraw()
    Add_wn = tk.Tk()
    Add_wn.title('Add Stock')
    center(Add_wn, Add_width, Add_height)

    Add_txt = tk.Entry(Add_wn, width = 30)
    Add_txt.place(x = 30, y = 15)

    Add_confirm = tk.Button(Add_wn, text = "confirm", height = 1, width = 7, command = lambda: add_stock(wn, Add_wn, Add_txt))
    Add_confirm.place(x = 260, y = 13)

    Add_wn.mainloop()



def main_screen():

    wn = tk.Tk()
    wn.title('Stock Prodection')
    center(wn, wn_width, wn_height)
    buttom_font = font.Font(size = 20)

    Add_buttom = tk.Button(wn, text = "Add Stock", height = 2, width = 10, command = lambda: Add_clicked(wn))
    Add_buttom.place(x = 100, y = 120)

    Run_buttom = tk.Button(wn, text = "Run", height = 2, width = 10)
    Run_buttom.place(x = 200, y = 120)

    setting_buttom = tk.Button(wn, text = "Setting", height = 2, width = 10)
    setting_buttom.place(x = 300, y = 120)

    wn.mainloop()


main_screen()
