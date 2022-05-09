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
    def __init__(self, xPos, yPos, color):
        self.xPos = xPos
        self.yPos = yPos
        self.xOldPos = xPos
        self.yOldPos = yPos
        self.visitedPositions = []
        self.visitedPositions.append([self.xPos, self.yPos])
        self.color = color

    def move(self, x, y):
        xCenter = self.xPos + (self.xPos - self.xOldPos)
        yCenter = self.yPos + (self.yPos - self.yOldPos)
        self.xOldPos = self.xPos
        self.yOldPos = self.yPos
        self.xPos = xCenter + x
        self.yPos = yCenter + y
        self.visitedPositions.append([self.xPos, self.yPos])
        print(validLine(self.getOldPos(), self.getPos()))

    def getVisitedPositions(self):
        return self.visitedPositions

    def getPos(self):
        return [self.xPos, self.yPos]

    def getColor(self):
        return self.color

    def penalty(self):
        self.xPos = self.xOldPos
        self.yPos = self.yOldPos
        self.visitedPositions.append([self.xPos, self.yPos])

    def getOldPos(self):
        return [self.xOldPos, self.yOldPos]


main = Tk()
# Code to add widgets will go here...
main.geometry("900x900")
frame = Frame(main)
frame.pack()

controlButtonList = []

canvas = Canvas(main, width=700, height=700)
canvas.pack()


def loadTrack(imageName):
    """
    Create a 2D map matrix based on a given image
    :param imageName: image file name
    :return: 2D array of the track
    """
    img = Image.open(imageName)
    data = np.asarray(img).transpose(1, 0, 2)
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
                map[i][j] = -1
    return map


mapTrack = loadTrack("large1.png")

x_size = eval(canvas.cget("height")) // mapTrack.shape[0]
y_size = eval(canvas.cget("width")) // mapTrack.shape[1]
rectange_size = min(x_size, y_size)


def createField(canvasName):
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


createField(canvas)

player1 = Player(5, 5, "yellow")


def create_circle(x, y, r, canvasName, fillColor, outlineColor, width):  # center coordinates, radius
    """
    Creates a circle
    :param x: center x position
    :param y: center y position
    :param r: radius
    :param canvasName: name of canvas
    :param fillColor: color of filling
    :param outlineColor: color of border line
    :param width: width of border line
    :return: creates circle
    """
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=fillColor, outline=outlineColor, width=width)


def drawPlayer(canvasName, player):
    """
    Draw the position of the player and the possible positions to move
    :param canvasName: name of the canvas
    :param player: player
    """
    pos = player.getPos()
    oldPos = player.getOldPos()

    xCenter = pos[0] + (pos[0] - oldPos[0])
    yCenter = pos[1] + (pos[1] - oldPos[1])
    for i in range(-1, 2):
        for j in range(-1, 2):
            create_circle((xCenter + i) * rectange_size, (yCenter + j) * rectange_size, 3, canvasName, "",
                          player.getColor(), 1)

    create_circle(pos[0] * rectange_size, pos[1] * rectange_size, 4, canvasName, player.getColor(), "black", 1)


def drawPlayerPath(canvasName, player):
    """
    Draw the path of the player
    :param canvasName: name of the canvas
    :param player: player
    """
    path = player.getVisitedPositions()
    for i in range(0, len(path) - 1):
        create_circle(path[i][0] * rectange_size, path[i][1] * rectange_size, 3, canvasName, player.getColor(), "black",
                      1)
        canvasName.create_line(path[i][0] * rectange_size, path[i][1] * rectange_size, path[i + 1][0] * rectange_size,
                               path[i + 1][1] * rectange_size, fill=player.getColor(), width=2)
    create_circle(path[-1][0] * rectange_size, path[-1][1] * rectange_size, 3, canvasName, player.getColor(), "black",
                  1)


def updateCanvas(canvasName, player):
    """
    After each step update the canvas: player position, path and possible next positions
    :param canvasName:
    :param player:
    """
    canvasName.delete("all")
    createField(canvasName)
    drawPlayer(canvasName, player)
    drawPlayerPath(canvasName, player)


updateCanvas(canvas, player1)


def validMovement(player):
    """
    Next position is valid or not (on the track)
    :param player: player
    :return: True/False
    """
    pos = player.getPos()
    if mapTrack[pos[0]][pos[1]] < 0:
        return False
    return True

def validLine(pos1, pos2):
    """
    The line between the two position (matrix: [x , y]) is on the track or not
    :param pos1: position 1
    :param pos2: position 2
    :return: True/False
    """
    dx = pos2[0]- pos1[0]
    dy = pos2[1] - pos1[1]

    if np.abs(dx) > 0:
        d = dy/dx
        for i in range(0, np.abs(dx)+1):
            ty = pos1[0]+i*np.sign(dx)
            txf = np.floor(pos1[1]+i*np.sign(dx))
            txc = np.ceil(pos1[1] + i * np.sign(dx))
            if mapTrack[txf][ty]<0 & mapTrack[txc][ty]<0:
                return False
    if np.abs(dy) > 0:
        d = dx/dy
        for i in range(0, np.abs(dy)+1):
            ty = pos1[1]+i*np.sign(dy)
            txf = np.floor(pos1[0]+i*np.sign(dy))
            txc = np.ceil(pos1[0] + i * np.sign(dy))
            if mapTrack[txf][ty]<0 & mapTrack[txc][ty]<0:
                return False
    return True


def buttonClick(canvasName, index):
    x = index % 3 - 1
    y = index // 3 - 1
    #print(x, y)
    player1.move(x, y)
    if not validMovement(player1):
        player1.penalty()
    updateCanvas(canvas, player1)
    #print(index)
    #print(player1.getPos())


for i in range(0, 9):
    temp = Button(frame, text=str(i), name=str(i), width=2, height=2)
    temp.grid(row=i // 3, column=i % 3)
    controlButtonList.append(temp)

controlButtonList[0].config(command=lambda: buttonClick(canvas, 0))
controlButtonList[1].config(command=lambda: buttonClick(canvas, 1))
controlButtonList[2].config(command=lambda: buttonClick(canvas, 2))
controlButtonList[3].config(command=lambda: buttonClick(canvas, 3))
controlButtonList[4].config(command=lambda: buttonClick(canvas, 4))
controlButtonList[5].config(command=lambda: buttonClick(canvas, 5))
controlButtonList[6].config(command=lambda: buttonClick(canvas, 6))
controlButtonList[7].config(command=lambda: buttonClick(canvas, 7))
controlButtonList[8].config(command=lambda: buttonClick(canvas, 8))

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
