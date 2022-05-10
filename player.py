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