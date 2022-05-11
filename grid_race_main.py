from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as st
from PIL import Image
import numpy as np
import random
import time
import player


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
                startPositions.append([i, j])
            elif (data[i][j] == [0, 0, 255]).all():
                map[i][j] = 100
                finishPositions.append([i, j])
            else:
                map[i][j] = -1
    return map


def createField(canvasName):
    """
    Draw the track based on the given map
    :param canvasName: Canvas, draw on it
    :param mapTrack: 2D array of the track
    """
    for i in range(0, mapTrack.shape[0]):
        for j in range(0, mapTrack.shape[1]):
            if mapTrack[i][j] == -1:
                temp = canvasName.create_rectangle(0, 0, rectangeSize, rectangeSize, fill="red")
            elif mapTrack[i][j] == 0:
                temp = canvasName.create_rectangle(0, 0, rectangeSize, rectangeSize, fill="green")
            elif mapTrack[i][j] == 100:
                temp = canvasName.create_rectangle(0, 0, rectangeSize, rectangeSize, fill="white")
            elif (mapTrack[i][j] == 1):
                temp = canvasName.create_rectangle(0, 0, rectangeSize, rectangeSize, fill="blue")
            canvasName.move(temp, int((i - 0.5) * rectangeSize), int((j - 0.5) * rectangeSize))


def getRandomStartPosition():
    """
    Return one of the starting positions randomly
    :return: starting position [x, y]
    """
    random.shuffle(startPositions)
    return startPositions.pop()


def isFinished(pos):
    """
    Is the position finished position
    :param pos: position [x, y]
    :return: True/False
    """
    if mapTrack[pos[0]][pos[1]] == 100:
        return True
    return False


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


def drawPlayer(canvasName, player, radius):
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
            create_circle((xCenter + i) * rectangeSize, (yCenter + j) * rectangeSize, radius - 1, canvasName, "",
                          player.getColor(), 1)

    create_circle(pos[0] * rectangeSize, pos[1] * rectangeSize, radius, canvasName, player.getColor(), "black", 1)


def drawPlayerPath(canvasName, player):
    """
    Draw the path of the player
    :param canvasName: name of the canvas
    :param player: player
    """
    path = player.getVisitedPositions()
    for i in range(0, len(path) - 1):
        create_circle(path[i][0] * rectangeSize, path[i][1] * rectangeSize, 3, canvasName, player.getColor(), "black",
                      1)
        canvasName.create_line(path[i][0] * rectangeSize, path[i][1] * rectangeSize, path[i + 1][0] * rectangeSize,
                               path[i + 1][1] * rectangeSize, fill=player.getColor(), width=2)
    create_circle(path[-1][0] * rectangeSize, path[-1][1] * rectangeSize, 3, canvasName, player.getColor(), "black",
                  1)


def updateCanvas(canvasName, playerList):
    """
    After each step update the canvas: player position, path and possible next positions
    :param canvasName:
    :param player:
    """
    canvasName.delete("all")
    createField(canvasName)
    for player in playerList:
        drawPlayer(canvasName, player, 4)
        drawPlayerPath(canvasName, player)
    time.sleep(0.4)


def validMovement(player):
    """
    Next position is valid or not (on the track, or on the other player)
    :param player: player
    :return: True/False
    """
    pos = player.getPos()
    if mapTrack[pos[0]][pos[1]] < 0:
        return False
    for i in range(0, len(playerList)):
        if (i != playerAt(pos)) & equalPoints(pos, playerList[i].getPos()):
            return False
    return True


def validLine(pos1, pos2):
    """
    The line between the two position (matrix: [x , y]) is on the track or not
    :param pos1: position 1
    :param pos2: position 2
    :return: True/False
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    if np.abs(dx) > 0:
        d = dy / dx
        for i in range(0, np.abs(dx) + 1):
            tx = pos1[0] + i * np.sign(dx)
            tyf = int(np.floor(pos1[1] + i * d * np.sign(dx)))
            tyc = int(np.ceil(pos1[1] + i * d * np.sign(dx)))
            if (mapTrack[tx][tyf] < 0) & (mapTrack[tx][tyc] < 0):
                return False
    if np.abs(dy) > 0:
        d = dx / dy
        for i in range(0, np.abs(dy) + 1):
            ty = pos1[1] + i * np.sign(dy)
            txf = int(np.floor(pos1[0] + i * d * np.sign(dy)))
            txc = int(np.ceil(pos1[0] + i * d * np.sign(dy)))
            if (mapTrack[txf][ty] < 0) & (mapTrack[txc][ty] < 0):
                return False
    return True


def playerAt(pos):
    """
    Return the index of that player at given position, otherwise -1
    :param pos: position [x, y]
    :return: index of player it exist or -1
    """
    for i in range(0, len(playerList)):
        if equalPoints(pos, playerList[i].getPos()):
            return i
    return -1


def equalPoints(pos1, pos2):
    """
    If two positions are the same
    :param pos1: position 1 [x, y]
    :param pos2: position 2 [x, y]
    :return: True/False
    """
    if (pos1[0] == pos2[0]) & (pos1[1] == pos2[1]):
        return True
    return False

def nextPlayerToMove(currentPlayerList):
    currentPlayer = currentPlayerList.pop()
    numOfPenalty = currentPlayer.getPenaltyRounds()
    while numOfPenalty > 0:
        currentPlayer.step()
        writeTextArea(currentPlayer.getName() + " is in penalty for " + str(numOfPenalty) + " more rounds.")
        currentPlayer.setPenaltyRounds(numOfPenalty - 1)
        currentPlayerList.insert(0, currentPlayer)
        currentPlayer = currentPlayerList.pop()
        numOfPenalty = currentPlayer.getPenaltyRounds()
    return currentPlayer

def buttonClick(canvasName, x, y):
    """
    Button click event: move the player
    :param canvasName: name of the canvas
    :param x: move direction x
    :param y: move direction y
    """
    # print(x, y)
    if len(currentPlayerList) > 0:
        currentPlayer = nextPlayerToMove(currentPlayerList)

        currentPlayer.move(x, y)
        currentPlayer.step()
        stepNum = str(currentPlayer.getStepNumber())
        if not validMovement(currentPlayer):
            currentPlayer.penalty()
            writeTextArea(currentPlayer.getName() + " is out of track or collided with other player. Penalty for 5 rounds. (step #" + stepNum + ")")

        if not isFinished(currentPlayer.getPos()):
            currentPlayerList.insert(0, currentPlayer)
        else:
            writeTextArea(currentPlayer.getName() + " has reached the finish position. (step #" + stepNum + ")")


        updateCanvas(canvasName, playerList)
        if len(currentPlayerList) > 0:
            nextPlayer = nextPlayerToMove(currentPlayerList)
            currentPlayerList.append(nextPlayer)
            writeTextArea(nextPlayer.getName() + " is to move (step #" + str(nextPlayer.getStepNumber()) + ")")
            drawPlayer(canvasName, nextPlayer, 6)
    # print(index)
    # print(isFinished(currentPlayer.getPos()))


def writeTextArea(string):
    textArea.configure(state='normal')
    textArea.insert(tk.INSERT, string + "\n")
    textArea.configure(state='disabled')
    textArea.yview(END)


def addButtonAction():
    if len(startPositions) > 0:
        startPos = getRandomStartPosition()
        s = text1.get('1.0', 'end')
        s = s.strip()
        if s == "":
            s = "Player" + len(startPositions)
        tempPlayer = player.Player(s, startPos[0], startPos[1], colors.pop())
        playerList.insert(0, tempPlayer)
        currentPlayerList.insert(0, tempPlayer)
        text1.delete('1.0', 'end')
    else:
        buttonAdd.pack_forget()
        text1.pack_forget()
        label1.config(text="No more player can be added!")

def moveFunction(mapTrack):
    return [0, 0]

def startButtonAction():
    if len(playerList) > 0:
        buttonAdd.pack_forget()
        text1.pack_forget()
        label1.pack_forget()
        startButton.pack_forget()
        codeArea.pack_forget()
        textArea.pack(side=LEFT)
        if not modeCoding:
            frameButton.pack(side=RIGHT, padx=10)
        else:
            codeToRun = codeArea.get('1.0', 'end') + "\n"
            eval(codeToRun)
            """
            for i in range(0, 5):
                nextMove = moveFunction(mapTrack)
                buttonClick(canvas, nextMove[0], nextMove[1])
            """

        updateCanvas(canvas, playerList)
        drawPlayer(canvas, currentPlayerList[-1], 6)
        writeTextArea(playerList[-1].getName() + " is to move (step #" + str(currentPlayerList[-1].getStepNumber()) + ")")
    else:
        label1.config(text="No player is added! Add a player!")

def selectMapButtonAction(mapName):
    canvas.pack(side=TOP, padx=50, pady=10)
    global mapTrack
    mapTrack = loadTrack(mapName)
    xSize = np.ceil(eval(canvas.cget("height")) / mapTrack.shape[0])
    ySize = np.ceil(eval(canvas.cget("width")) / mapTrack.shape[1])
    global rectangeSize
    rectangeSize = min(xSize, ySize)
    createField(canvas)
    updateCanvas(canvas, playerList)
    for i in mapButtonList:
        i.pack_forget()
    manualBtn.pack(side=LEFT)
    codeBtn.pack(side=LEFT, padx=10)

def manualMode():
    manualBtn.pack_forget()
    codeBtn.pack_forget()
    label1.pack()
    text1.pack(side=LEFT)
    buttonAdd.pack(side=LEFT, padx=10)
    startButton.pack(padx=10)

def codingMode():
    manualBtn.pack_forget()
    codeBtn.pack_forget()
    label1.pack()
    codeArea.pack(side=BOTTOM)
    text1.pack(side=LEFT)
    buttonAdd.pack(side=LEFT, padx=5)
    startButton.pack(side=LEFT, padx=5)
    global modeCoding
    modeCoding = True

root = Tk()
root.title("Grid race")
root.geometry("800x800")

controlButtonList = []
startPositions = []
finishPositions = []
playerList = []
currentPlayerList = []
mapButtonList = []
modeCoding = False
colors = ['#822A8A', '#A8A228', '#00FF00', '#C9FF00', '#6688CC', '#88CC66']

canvas = Canvas(root, width=800, height=550)


frameRoot = Frame(root)
frameRoot.pack(side=BOTTOM, pady=(0, 50))

#Select map
mapNames = ["straight.png", 'small1.png', 'small2.png', 'large1.png', 'large2.png']
labelMap = Label(frameRoot, text="Choose a map:")
labelMap.config(font=12)
labelMap.pack()
mapButtonList.append(labelMap)
photo = tk.PhotoImage(file=mapNames[0])
b1 = Button(frameRoot, image=photo, command=lambda: selectMapButtonAction(mapNames[0]))
b1.pack(side=LEFT, padx=5)
mapButtonList.append(b1)
photo2 = tk.PhotoImage(file=mapNames[1])
b2 = Button(frameRoot, image=photo2, command=lambda: selectMapButtonAction(mapNames[1]))
b2.pack(side=LEFT, padx=5)
mapButtonList.append(b2)
photo3 = tk.PhotoImage(file=mapNames[2])
b3=Button(frameRoot, image=photo3, command=lambda: selectMapButtonAction(mapNames[2]))
b3.pack(side=LEFT, padx=5)
mapButtonList.append(b3)
photo4 = tk.PhotoImage(file=mapNames[3])
b4 = Button(frameRoot, image=photo4, command=lambda: selectMapButtonAction(mapNames[3]))
b4.pack(side=LEFT, padx=5)
mapButtonList.append(b4)
photo5 = tk.PhotoImage(file=mapNames[4])
b5 = Button(frameRoot, image=photo5, command=lambda: selectMapButtonAction(mapNames[4]))
b5.pack(side=LEFT, padx=5)
mapButtonList.append(b5)

"""
for i in range(0, len(mapNames)):
    photo = tk.PhotoImage(file=mapNames[i])
    temp = Button(frameRoot, image=photo, command=lambda: selectMapButtonAction(mapNames[i]))
    temp.pack(side=LEFT, padx=5)
    mapButtonList.append(temp)
"""

#Select mode
manualBtn = Button(frameRoot, width=5, height=1, text="Manual", command=lambda: manualMode())
codeBtn = Button(frameRoot, width=5, height=1, text="Coding", command=lambda: codingMode())




label1 = Label(frameRoot, text="Add new player:")
label1.config(font=12)
text1 = Text(frameRoot, width=20, height=1)
buttonAdd = Button(frameRoot, width=3, height=1, text="Add", command=lambda: addButtonAction())
startButton = Button(frameRoot, width=5, height=1, text="Start", command=lambda: startButtonAction())

textArea = st.ScrolledText(frameRoot, width=60, height=10, font=12)
# text_area.pack(side=LEFT)
writeTextArea("Grid game")

codeArea = st.ScrolledText(frameRoot, width=60, height=10, font=12)
codeArea.insert(tk.INSERT, "Write your code here!")

# Manual mode
frameButton = Frame(frameRoot)
# frameButton.pack(side=RIGHT, padx=10)
for i in range(0, 9):
    temp = Button(frameButton, name=str(i), width=2, height=2)
    temp.grid(row=i // 3, column=i % 3)
    controlButtonList.append(temp)

controlButtonList[0].config(text="↖", command=lambda: buttonClick(canvas, -1, -1))
controlButtonList[1].config(text="↑", command=lambda: buttonClick(canvas, 0, -1))
controlButtonList[2].config(text="↗", command=lambda: buttonClick(canvas, 1, -1))
controlButtonList[3].config(text="←", command=lambda: buttonClick(canvas, -1, 0))
controlButtonList[4].config(text=".", command=lambda: buttonClick(canvas, 0, 0))
controlButtonList[5].config(text="→", command=lambda: buttonClick(canvas, 1, 0))
controlButtonList[6].config(text="↙", command=lambda: buttonClick(canvas, -1, 1))
controlButtonList[7].config(text="↓", command=lambda: buttonClick(canvas, 0, 1))
controlButtonList[8].config(text="↘", command=lambda: buttonClick(canvas, 1, 1))

if __name__ == "__main__":
    root.mainloop()
