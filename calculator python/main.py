import tkinter as tk
from tkinter import StringVar

def button_press(num):
    global equation_text
    equation_text = equation_text + str(num)
    equation_label.set(equation_text)

def equals():
    global equation_text
    try:
        total = str(eval(equation_text))
        equation_label.set(total)
        equation_text = total
    except SyntaxError:
        equation_label.set("syntax error")
        equation_text = ""
    except ZeroDivisionError:
        equation_label.set("arithmetic error")
        equation_text = ""

def clear_calc():
    global equation_text
    equation_label.set("")
    equation_text = ""

window = tk.Tk()
window.title("Calculator program")
window.geometry("500x500")

equation_text = ""
equation_label = StringVar()

label = tk.Label(window, textvariable=equation_label, font=('consolas',20), 
                 bg="white", width=24, height=2)
label.pack()

frame = tk.Frame(window)
frame.pack()

# Создаем кнопки цифр
buttons = []
for i in range(1, 10):
    button = tk.Button(frame, text=str(i), height=4, width=9, font=35,
                      command=lambda num=i: button_press(num))
    buttons.append(button)

# Располагаем кнопки в сетке 3x3
for i in range(3):
    for j in range(3):
        buttons[i*3 + j].grid(row=i, column=j)

button0 = tk.Button(frame, text='0', height=4, width=9, font=35,
                   command=lambda: button_press(0))
button0.grid(row=3, column=0)

# Кнопки операций
operations = ['+', '-', '*', '/']
for i, op in enumerate(operations):
    button = tk.Button(frame, text=op, height=4, width=9, font=35,
                      command=lambda o=op: button_press(o))
    button.grid(row=i, column=3)

equal = tk.Button(frame, text='=', height=4, width=9, font=35,
                 command=equals)
equal.grid(row=3, column=2)

decimal = tk.Button(frame, text='.', height=4, width=9, font=35,
                   command=lambda: button_press('.'))
decimal.grid(row=3, column=1)

clear_button = tk.Button(window, text='clear', height=4, width=12, font=35,
                        command=clear_calc)
clear_button.pack()

window.mainloop()