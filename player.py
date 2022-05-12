import random

import functions


class Player:
    def __init__(self, name, xPos, yPos, color, ai):
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.xOldPos = xPos
        self.yOldPos = yPos
        self.visitedPositions = []
        self.visitedPositions.append([self.xPos, self.yPos])
        self.color = color
        self.penaltyRounds = 0
        self.stepNumber = 1
        self.moveFunction = None
        self.ai = ai

    def getName(self):
        return self.name

    def nextPosition(self, x, y):
        xCenter = self.xPos + (self.xPos - self.xOldPos)
        yCenter = self.yPos + (self.yPos - self.yOldPos)
        return [xCenter + x, yCenter + y]

    def move(self, x, y):
        xCenter = self.xPos + (self.xPos - self.xOldPos)
        yCenter = self.yPos + (self.yPos - self.yOldPos)
        self.xOldPos = self.xPos
        self.yOldPos = self.yPos
        self.xPos = xCenter + x
        self.yPos = yCenter + y
        self.visitedPositions.append([self.xPos, self.yPos])
        #print(validLine(self.getOldPos(), self.getPos()))

    def isAi(self):
        return self.ai

    def aiMove(self, mapTrack, playerList):
        """
        i = random.randint(-1, 1)
        j = random.randint(-1, 1)
        print(i,j)

        if functions.validMovement(mapTrack, playerList, self.getPos(), self.nextPosition(i,j)):
            print("true")
            #return [i, j]
        else:
            print("false")

        return [1, 0]
        """
        self.zombieArray = functions.createZombieMap(mapTrack)
        return functions.moveBestNStemDirection(mapTrack, playerList, self.getOldPos(), self.getPos(), self.zombieArray, 8)

        try:
            return functions.moveBestNStemDirection(mapTrack, playerList, self.getOldPos(), self.getPos(), self.zombieArray, 8)
        except Exception:
            return [0, 0]



    """
    def movePlayer(self):
        result = self.moveFunction
        self.move(result[0], result[1])

    def setMoveFunction(self, moveFunction):
        self.moveFunction = moveFunction
    """

    def setPenaltyRounds(self, numOfPenalty):
        self.penaltyRounds = numOfPenalty

    def getPenaltyRounds(self):
        return self.penaltyRounds

    def getVisitedPositions(self):
        return self.visitedPositions

    def getStepNumber(self):
        return self.stepNumber

    def step(self):
        self.stepNumber = self.stepNumber + 1

    def getPos(self):
        return [self.xPos, self.yPos]

    def getColor(self):
        return self.color

    def penalty(self):
        self.xPos = self.xOldPos
        self.yPos = self.yOldPos
        self.visitedPositions.append([self.xPos, self.yPos])
        self.setPenaltyRounds(4)

    def getOldPos(self):
        return [self.xOldPos, self.yOldPos]