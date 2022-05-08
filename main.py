# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


from tkinter import *

main = Tk()
# Code to add widgets will go here...
main.geometry("400x400")
frame = Frame(main)
frame.pack()

controlButtonList = []

canvas = Canvas(main, width=200, height=200)
canvas.pack()

table = [[-1,0,0],[-1,-1,0],[0,0,0],[-1,0,-1],[0,0,-1]]

def createField(canvas, table):
    x_size = eval(canvas.cget("height"))//len(table)
    y_size = eval(canvas.cget("width"))//len(table[0])
    for i in range(0, len(table)):
        for j in range(0, len(table[0])):
            if (table[i][j]==-1):
                temp = canvas.create_rectangle(0, 0, x_size, y_size, fill="red")
            else:
                temp = canvas.create_rectangle(0, 0, x_size, y_size, fill="green")
            canvas.move(temp, i * x_size, j * y_size)


createField(canvas, table)


def buttonClick(index):
    print(index)


for i in range(0, 9):
    temp = Button(frame, text=str(i), name=str(i), width=2, height=2)
    temp.grid(row=i // 3, column=i % 3)
    controlButtonList.append(temp)

controlButtonList[0].config(command=lambda: buttonClick(1))
controlButtonList[1].config(command=lambda: buttonClick(2))
controlButtonList[2].config(command=lambda: buttonClick(3))
controlButtonList[3].config(command=lambda: buttonClick(4))
controlButtonList[4].config(command=lambda: buttonClick(5))
controlButtonList[5].config(command=lambda: buttonClick(6))
controlButtonList[6].config(command=lambda: buttonClick(7))
controlButtonList[7].config(command=lambda: buttonClick(8))
controlButtonList[8].config(command=lambda: buttonClick(9))



if __name__ == "__main__":
    main.mainloop()

"""
        
            
btn1 = Button(frame, text="", name="btn1", command=lambda: buttonClick(1))
btn1.grid(row=0, column=0)
controlButtonList.append(btn1)
btn2 = Button(frame, text="", name="btn2", command=lambda: buttonClick(2))
btn2.grid(row=0, column=1)
controlButtonList.append(btn2)
btn3 = Button(frame, text="", name="btn3", command=lambda: buttonClick(3))
btn3.grid(row=0, column=2)
controlButtonList.append(btn3)
btn4 = Button(frame, text="", name="btn4", command=lambda: buttonClick(4))
btn4.grid(row=1, column=0)
controlButtonList.append(btn4)
btn5 = Button(frame, text="", name="btn5", command=lambda: buttonClick(5))
btn5.grid(row=1, column=1)
controlButtonList.append(btn5)
btn6 = Button(frame, text="", name="btn6", command=lambda: buttonClick(6))
btn6.grid(row=1, column=2)
controlButtonList.append(btn6)
btn7 = Button(frame, text="", name="btn7", command=lambda: buttonClick(7))
btn7.grid(row=2, column=0)
controlButtonList.append(btn7)
btn8 = Button(frame, text="", name="btn8", command=lambda: buttonClick(8))
btn8.grid(row=2, column=1)
controlButtonList.append(btn8)
btn9 = Button(frame, text="", name="btn9", command=lambda: buttonClick(9))
btn9.grid(row=2, column=2)
controlButtonList.append(btn9)
"""
