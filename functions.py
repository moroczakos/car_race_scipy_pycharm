import numpy as np

def validMovement(mapTrack, playerList, fromPos, toPos):
    """
    Next position is valid or not (on the track, or on the other player)
    :param toPos:
    :param mapTrack:
    :param playerList:
    :param fromPos: player
    :return: True/False
    """
    if mapTrack[toPos[0]][toPos[1]] < 0 \
            | validLine(mapTrack, fromPos, toPos) == False:
        return False
    for i in range(0, len(playerList)):
        if (i != playerAt(playerList, toPos)) & equalPoints(toPos, playerList[i].getPos()):
            return False
    return True


def validLine(mapTrack, pos1, pos2):
    """
    The line between the two position (matrix: [x , y]) is on the track or not
    :param mapTrack:
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


def playerAt(playerList, pos):
    """
    Return the index of that player at given position, otherwise -1
    :param playerList:
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

def createZombieMap(mapTrack):
    """
    Generate a zombie array based on the given map
    :param mapTrack: map of the track
    :return: generated zombieArray
    """
    lx = mapTrack.shape[0]
    ly = mapTrack.shape[1]

    num_of_fields = lx * ly

    penalty = 10 * num_of_fields

    zombieArray = [[penalty] * ly] * lx
    zombieArray = np.asarray(zombieArray)

    #set zombieArray value 0 if it is a finish position
    for i in range(0, lx):
        for j in range(0, ly):
            if mapTrack[i][j] == 100:
                zombieArray[i][j] = 0

    #generate the distance matrix: neighbouring postions get larger and larger value
    for k in range(1, num_of_fields):
        for i in range(0, lx):
            for j in range(0, ly):
                if zombieArray[i][j] == k-1:
                    for x in range(max(i-1, 0), min(i+2, lx)):
                        for y in range(max(j-1, 0), min(j+2, ly)):
                            if (mapTrack[x][y] != -1) & (zombieArray[x][y] == penalty):
                                zombieArray[x][y] = k

    return zombieArray

def validMoves(mapTrack, playerList, oldPos, pos):
    """
    Give back the valid directions and positions of the next movement from the current position
    :param mapTrack: map of the track
    :param playerList: list of players
    :param oldPos: previous position of the player
    :param pos: current position of the player
    :return: [valid directions, valid positions]
    """
    xCenter = pos[0] + (pos[0] - oldPos[0])
    yCenter = pos[1] + (pos[1] - oldPos[1])

    validmoves = []
    validpositions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            nextmove = [xCenter+i, yCenter+j]
            if validMovement(mapTrack, playerList, pos, nextmove):
                validmoves.append([i, j])
                validpositions.append(nextmove)

    return [validmoves, validpositions]


def moveBestNStemDirection(mapTrack, playerList, oldPos, pos, zombieArray, numOfStep):
    """
    Return the best possible direction of the next movement
     :param mapTrack: map of the track
    :param playerList: list of players
    :param oldPos: previous position of the player
    :param pos: current position of the player
    :param zombieArray: predetermined zombie array
    :param numOfStep: steps to look ahead
    :return: the best possible direction of the next movement
    """
    stepArray = []                  #store the steps
    nextPos = pos
    nextDir = [0, 0]                #direction to move
    prevPos = oldPos
    posValue = zombieArray[prevPos[0]][prevPos[1]]
    level = 0
    prexIndex = None
    # a step stores: next position, direction to move, previous position, previous position value, level (steps), index
    # of the previous step in the stepArray (for backtracking)
    step = [nextPos, nextDir, prevPos, posValue, level, prexIndex]

    stepArray.insert(0, step)
    stepArrayIndex = 0              # store the index in the stepArray of the previous step

    while step[4] < numOfStep:
        moves = validMoves(mapTrack, playerList, step[2], step[0])      # find next valid movements

        # search valid steps from a given position
        if len(moves[1])>0:
            for i in range(0, len(moves[1])):
                nextPos = moves[1][i]
                nextDir = moves[0][i]
                prevPos = step[2]
                level = step[4] + 1
                tempStep = [nextPos, nextDir, prevPos, posValue, level, stepArrayIndex]
                stepArray.insert(0, tempStep)

        # if there is no more valid step, continue the search in the next step
        if len(stepArray)>0:
            stepArrayIndex = stepArrayIndex + 1
            step = stepArray[stepArrayIndex]
        else:
            break           # if there is no next valid step, stop the loop

    # search the best Nth step result
    minIndex = 0
    minValue = stepArray[0][3]
    for i in range(0, len(stepArray)):
        if stepArray[i][3] < minValue:
            minValue = stepArray[i][3]
            minIndex = i

    # based on the best N-th step result, find the way how we get there (backtracking by previous indexes)
    prevIdx = minIndex
    while stepArray[prevIdx][5] > 0:
        prevIdx = stepArray[prevIdx][5]

    # return the next direction (based on the Nth best step)
    return stepArray[prevIdx][1]



