import tkinter as tk


def val_print(c_var):
    print(c_var.get())




b = tk.Tk()

c_var = tk.IntVar()

c_check = tk.Checkbutton(b, variable = c_var, onvalue = 1, offvalue = 0, command = lambda: val_print(c_var))
c_check.grid(sticky = "n", column = 1, row = 1)

b.mainloop()


'''
a = tk.Tk()

a_b = tk.Button(a, text = "next", command = next)
a_b.place(x = 10, y = 10)

a.mainloop()
'''
