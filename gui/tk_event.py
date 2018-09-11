# coding: utf8
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import random

num = random.randint(1, 100)

root = tk.Tk()
root.title("Tkinter by Crossin")
window_left = ttk.Frame(root)
window_left.pack(ipadx=10, ipady=10, fill='y', side=tk.LEFT)

label = ttk.Label(window_left, text="猜猜我想数字是多少（1~100）")
label.pack(padx=20, pady=20)
answer = tk.IntVar()
entry = ttk.Entry(window_left, width=20, textvariable=answer)
entry.pack()

window_right = ttk.Frame(root)
window_right.pack(ipadx=10, ipady=10, fill='y', side=tk.RIGHT)
output = scrolledtext.ScrolledText(window_right, height=10, width=25, highlightbackground='black', highlightthickness=1)
output.pack(pady=10)

def guess():
    a = answer.get()
    if a < num:
        output.insert(tk.INSERT, '%d 小了\n' % a)
    elif a > num:
        output.insert(tk.INSERT, '%d 大了\n' % a)
    else:
        output.insert(tk.INSERT, '猜中啦！就是 %d\n' % a)

btn = ttk.Button(window_left, text="确定", command=guess)
btn.pack()

root.mainloop()
