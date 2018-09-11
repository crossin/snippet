import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter by Crossin")

window = ttk.Frame(root)
window.pack(ipadx=10, ipady=10)

label = ttk.Label(window, text="Hello, world!")
label.pack()
btn = ttk.Button(window, text="OK")
btn.pack()
w = ttk.Entry(window)
w.pack()

w = tk.Listbox(window, height=3)
w.insert(1, "Python")
w.insert(2, "C++")
w.insert(3, "JAVA")
w.pack()

v1 = tk.BooleanVar()
w = ttk.Checkbutton(window, text='Check 1', variable=v1)
w.invoke()
w.pack()
v2 = tk.BooleanVar()
w = ttk.Checkbutton(window, text='Check 2', variable=v2)
w.pack()

w = ttk.Radiobutton(window, text = "Option 1", value=1)
w.invoke()
w.pack()
w = ttk.Radiobutton(window, text = "Option 2", value=2)
w.pack()

w = tk.Text(window, height=5, width=25, highlightbackground='black', highlightthickness=1)
w.pack()

w = ttk.Combobox(window)
w['values'] = ('IDLE', 'PyCharm', 'VSCode', 'SublimeText')
w.current(1)
w.pack()

root.mainloop()
