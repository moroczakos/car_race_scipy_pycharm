class Player:
    def __init__(self, name, xPos, yPos, color):
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

    def getName(self):
        return self.name

    def move(self, x, y):
        xCenter = self.xPos + (self.xPos - self.xOldPos)
        yCenter = self.yPos + (self.yPos - self.yOldPos)
        self.xOldPos = self.xPos
        self.yOldPos = self.yPos
        self.xPos = xCenter + x
        self.yPos = yCenter + y
        self.visitedPositions.append([self.xPos, self.yPos])
        #print(validLine(self.getOldPos(), self.getPos()))

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