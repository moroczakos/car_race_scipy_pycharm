import random

import functions

# Player class
class Player:
    def __init__(self, name, xPos, yPos, color, ai):
        """
        Constructor
        :param name: name of the player
        :param xPos: starting x positions, current positions
        :param yPos: starting y positions, current positions
        :param color: color the draw the player
        :param ai: is AI player or not
        """
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
        """
        Move to the next position based on the given direction
        :param x: given x direction
        :param y: given y direction
        """
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
        Movement of the AI
        :param mapTrack: map of the track
        :param playerList: list of players
        :return:
        """
        self.zombieArray = functions.createZombieMap(mapTrack)
        return functions.moveBestNStemDirection(mapTrack, playerList, self.getOldPos(), self.getPos(), self.zombieArray, 8)

        try:
            return functions.moveBestNStemDirection(mapTrack, playerList, self.getOldPos(), self.getPos(), self.zombieArray, 8)
        except Exception:
            return [0, 0]

    def setPenaltyRounds(self, numOfPenalty):
        """
        Set penalty in case of invalid movement
        :param numOfPenalty: number of penalty rounds
        """
        self.penaltyRounds = numOfPenalty

    def getPenaltyRounds(self):
        return self.penaltyRounds

    def getVisitedPositions(self):
        """
        Return the visited positions for drawing the path
        :return: list of visited positions
        """
        return self.visitedPositions

    def getStepNumber(self):
        return self.stepNumber

    def step(self):
        """
        Increase the number of steps by one
        """
        self.stepNumber = self.stepNumber + 1

    def getPos(self):
        return [self.xPos, self.yPos]

    def getColor(self):
        return self.color

    def penalty(self):
        """
        Put the player in penalty for invalid movement
        """
        self.xPos = self.xOldPos
        self.yPos = self.yOldPos
        self.visitedPositions.append([self.xPos, self.yPos])
        self.setPenaltyRounds(4)

    def getOldPos(self):
        return [self.xOldPos, self.yOldPos]