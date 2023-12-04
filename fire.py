from cmu_graphics import *
import math
from PIL import Image

#https://www.geeksforgeeks.org/check-line-touches-intersects-circle/
#Used equation for finding shortest distance from line to circle (perpendicular distance)
def shortest_distance(x1, y1, a, b, c): 
    shortestDistance = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
    return shortestDistance

class Fire:
    def __init__(self, cellSize):
        self.fires = []
        self.cellSize = cellSize
        self.fireRadius = 20
        self.length = 160
        self.fire_image = CMUImage(Image.open('images/fire.png'))
        self.fireInterval = 5
        self.imageSize = 30

    def addfire(self, x, y, shift): # add fire block
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        if (gridX * self.cellSize + self.cellSize / 2, gridY * self.cellSize + self.cellSize / 2) not in self.fires:
            self.fires.append((gridX * self.cellSize + self.cellSize / 2, gridY * self.cellSize + self.cellSize / 2))
    
    def unclick(self, x, y, shift): # remove fire block
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        if (gridX * self.cellSize + self.cellSize / 2, gridY * self.cellSize + self.cellSize / 2) in self.fires:
            self.fires.remove((gridX * self.cellSize + self.cellSize / 2, gridY * self.cellSize + self.cellSize / 2))

    def damage(self, mariox, marioy, rotation, shift): # inflict damage
        for fireIdx in range(len(self.fires)):
            x, y = self.fires[fireIdx]
            x -= shift
            newx, newy = x + self.length * math.sin(math.degrees(rotation)), y + self.length * math.cos(math.degrees(rotation))
            a = newy - y
            b = x - newx
            c = (a * x + b * y) * -1
            if shortest_distance(mariox, marioy, a, b, c) <= self.fireRadius and (x <= mariox <= newx or newx <= mariox < x):
                return True
        return False


    def draw(self, shift, rotation): # draw fire blocks
        for fireIdx in range(len(self.fires)):
            x, y = self.fires[fireIdx]
            newx, newy = x + self.length * math.sin(math.degrees(rotation)), y + self.length * math.cos(math.degrees(rotation))
            for j in range(self.fireInterval + 1):
                drawImage(self.fire_image, x + self.length * math.sin(math.degrees(rotation)) * (1 / self.fireInterval) * j - shift, 
                          y + self.length * math.cos(math.degrees(rotation)) * (1 / self.fireInterval) * j, width = self.imageSize, height = self.imageSize, align = 'center', rotateAngle = math.degrees(rotation))