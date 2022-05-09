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
from PIL import Image
import numpy as np

class Player:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.xOldPos = xPos
        self.yOldPos = yPos

    def move(self, x, y):
        xCenter = self.xPos+(self.xPos-self.xOldPos)
        yCenter = self.yPos + (self.yPos - self.yOldPos)
        self.xOldPos = self.xPos
        self.yOldPos = self.yPos
        self.xPos = xCenter + x
        self.yPos = yCenter + y

    def getPos(self):
        return [self.xPos, self.yPos]

    def penalty(self):
        self.xPos=self.xOldPos
        self.yPos=self.yOldPos

    def getOldPos(self):
        return [self.xOldPos, self.yOldPos]


main = Tk()
# Code to add widgets will go here...
main.geometry("600x600")
frame = Frame(main)
frame.pack()

controlButtonList = []

canvas = Canvas(main, width=500, height=500)
canvas.pack()


def loadTrack(imageName):
    """
    Create a 2D map matrix based on a given image
    :param imageName: image file name
    :return: 2D array of the track
    """
    img = Image.open(imageName)
    data = np.asarray(img).transpose(1,0,2)
    height = data.shape[0]
    width = data.shape[1]
    map = np.zeros((height, width))

    for i in range(0, height):
        for j in range(0, width):
            if (data[i][j] == [255, 0, 0]).all():
                map[i][j] = -1
            elif (data[i][j] == [255, 255, 255]).all():
                map[i][j] = 0
            elif (data[i][j] == [0, 255, 0]).all():
                map[i][j] = 1
            elif (data[i][j] == [0, 0, 255]).all():
                map[i][j] = 100
            else:
                map[i][j] = -2

    return map


mapTrack = loadTrack("large1.png")

x_size = eval(canvas.cget("height")) // mapTrack.shape[0]
y_size = eval(canvas.cget("width")) // mapTrack.shape[1]
rectange_size = min(x_size, y_size)

def createField(canvasName, mapTrack):
    """
    Draw the track based on the given map
    :param canvasName: Canvas, draw on it
    :param mapTrack: 2D array of the track
    """
    for i in range(0, mapTrack.shape[0]):
        for j in range(0, mapTrack.shape[1]):
            if mapTrack[i][j] == -1:
                temp = canvasName.create_rectangle(0, 0, rectange_size, rectange_size, fill="red")
            elif mapTrack[i][j] == 0:
                temp = canvasName.create_rectangle(0, 0, rectange_size, rectange_size, fill="green")
            elif mapTrack[i][j] == 100:
                temp = canvasName.create_rectangle(0, 0, rectange_size, rectange_size, fill="white")
            elif (mapTrack[i][j] == 1):
                temp = canvasName.create_rectangle(0, 0, rectange_size, rectange_size, fill="blue")
            canvasName.move(temp, i * rectange_size, j * rectange_size)


createField(canvas, mapTrack)

player1 = Player(5,5)

def create_circle(x, y, r, canvasName, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color)

def drawPlayer(canvasName, player):
    pos = player1.getPos()
    oldPos = player1.getOldPos()

    xCenter = pos[0] + (pos[0] - oldPos[0])
    yCenter = pos[1] + (pos[1] - oldPos[1])
    for i in range(-1,2):
        for j in range(-1,2):
            create_circle((xCenter+i) * rectange_size, (yCenter+j) * rectange_size, 3, canvasName, "blue")

    create_circle(pos[0] * rectange_size, pos[1] * rectange_size, 4, canvasName, "yellow")

def updateCanvas(canvasName, mapTrack, player):
    canvasName.delete("all")
    createField(canvasName, mapTrack)
    drawPlayer(canvasName, player)

updateCanvas(canvas,mapTrack,player1)

def validMovement(player, mapTrack):
    pos = player.getPos()
    if mapTrack[pos[0]][pos[1]] < 0:
        return False
    return True

def buttonClick(canvasName, index):
    x = index % 3 -1
    y = index // 3 -1
    print(x,y)
    player1.move(x, y)
    if not validMovement(player1, mapTrack):
       player1.penalty()
    updateCanvas(canvas,mapTrack,player1)
    print(index)
    print(player1.getPos())


for i in range(0, 9):
    temp = Button(frame, text=str(i), name=str(i), width=2, height=2)
    temp.grid(row=i // 3, column=i % 3)
    controlButtonList.append(temp)

controlButtonList[0].config(command=lambda: buttonClick(canvas,0))
controlButtonList[1].config(command=lambda: buttonClick(canvas,1))
controlButtonList[2].config(command=lambda: buttonClick(canvas,2))
controlButtonList[3].config(command=lambda: buttonClick(canvas,3))
controlButtonList[4].config(command=lambda: buttonClick(canvas,4))
controlButtonList[5].config(command=lambda: buttonClick(canvas,5))
controlButtonList[6].config(command=lambda: buttonClick(canvas,6))
controlButtonList[7].config(command=lambda: buttonClick(canvas,7))
controlButtonList[8].config(command=lambda: buttonClick(canvas,8))

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
