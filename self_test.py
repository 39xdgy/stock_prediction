x = [(0.0063, 328.41888),
     (0.0029, 322.0299),
     (0.0022, 319.01382),
     (0.0017, 308.27036),
     (0.0018, 316.27673),
     (0.0016, 306.4895),
     (0.0018, 323.9303),
     (0.0014, 318.3425),
     (0.0015,308.54874),
     (0.0014, 316.81277),
     (0.0014, 313.6903),
     (0.0013, 317.5966),
     (0.0012, 321.62064),
     (0.0012, 316.26123),
     (0.0012, 338.50992),
     (0.0012, 315.79642),
     (0.0011, 317.00595),
     (0.0011, 326.255),
     (0.0012, 319.47345),
     (0.0011, 308.03464)]

#print((321.62064+316.26123+315.79642+317.00595+326.255+319.47345)/6)

import pandas_datareader as web
from datetime import date
import tkinter as tk
import time
from stock_model import stock_model as sm
x = web.DataReader("F", data_source = 'yahoo', start = "2020-05-31", end = date.today())
#print(x)
#print(str(date.today()) == str(x.index[0])[:10])


class window:

    def __init__(self):
        self.wn1 = tk.Tk()
        self.wn2 = tk.Tk()
        self.wn3 = tk.Tk()
        self.wn1.withdraw()
        self.wn2.withdraw()
        self.wn3.withdraw()
        self.wn3.configure(bg='White')
        self.track = 0
        self.draw_wn()
        self.main()

    def next_to_2(self):
        self.wn1.withdraw()
        self.wn2.deiconify()
        self.wn2.mainloop()

    def next_to_3(self):
        self.wn2.withdraw()
        self.wn3.deiconify()
        self.draw_wn3()
        self.wn3.mainloop()
    def draw_wn(self):
        self.wn1.title("test 1")
        self.wn2.title("test 2")

        next_button = tk.Button(self.wn1, text = "next 1", command = self.next_to_2)
        next_button.grid()

        next_button_2 = tk.Button(self.wn2, text = "next 2", command = self.next_to_3)
        next_button_2.grid()



        self.wn1.protocol("WM_DELETE_WINDOW", self.close_all)
        self.wn2.protocol("WM_DELETE_WINDOW", self.close_all)

        '''
        start_time = time.time()
        for i in range(0, 10):
            for j in range(0, 10):
                time.sleep(10)
            now_time = time.time()
            self.track += (now_time - start_time)
            start_time = now_time
        '''

    def draw_wn3(self):
        self.wn3.title("test 3")
        self.test_label = tk.Label(self.wn3, text = "testing...", bg = "White")
        self.test_label.grid()
        self.wn3.protocol("WM_DELETE_WINDOW", self.close_all)
        self.wn3.after(10, self.test_fuc)


    def test_fuc(self):

        start_time = time.time()
        flag = "testing..."
        lis = ['AAPL', 'F', 'BABA']
        for name in lis :
            #for j in range(0, 10):
            x = sm(name, ("2018-05-01", "2020-05-31"))
            x.create_brain()
            flag += "\n" + name + "is finished"
            #now_time = time.time()
            #self.track += (now_time - start_time)
            #start_time = now_time
            self.test_label.configure(text = flag)
            self.wn3.update()



    def main(self):
        self.wn1.deiconify()
        self.wn1.mainloop()

    def close_all(self):
        self.wn1.destroy()
        self.wn2.destroy()
        self.wn3.destroy()

x = window()
