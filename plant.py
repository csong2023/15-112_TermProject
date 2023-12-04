from cmu_graphics import *
import random
from PIL import Image

def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

class Plant:
    def __init__(self): # initializing plant images + pipe image
        self.imagePipe = CMUImage(Image.open('images/pipe.png'))
        self.imagePlant1 = CMUImage(Image.open('images/plant1.png'))
        self.imagePlant2 = CMUImage(Image.open('images/plant2.png'))
        self.cellSize = 40
        self.plants = []
        self.plantsCooldown = []
        self.pauseTime = 150
        self.damageMin = -5
        self.lift = [0] * self.pauseTime + list(range(0, -35, -1)) + [-35] * self.pauseTime + list(range(-35, 0))
        self.liftIdx = 0

    def click(self, x, y, shift, grid): # add plant
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        if (gridY, gridX) not in self.plants and not grid[gridY][gridX]:
            self.plants.append((gridY, gridX))
            self.plantsCooldown.append(self.pauseTime)

    def unclick(self, x, y, shift): # remove plant
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        
        if (gridY, gridX) in self.plants:
            self.plantsCooldown.pop(self.plants.index((gridY, gridX)))
            self.plants.remove((gridY, gridX))

    def damage(self, mariox, marioy, shift): # if the plant part is contacting mario, inflict damage (not the pipe part)
        for plantIdx in range(len(self.plants)):
            y, x = self.plants[plantIdx]
            x = (x * self.cellSize) - shift
            y = y * self.cellSize
            circleY = y + self.lift[self.liftIdx]
            circleX = x + self.cellSize // 2
            if self.lift[self.liftIdx] < self.damageMin and distance(mariox, marioy, circleX, circleY) < self.cellSize // 2:
                return True
        return False
        
    def update(self): # make sure that the plant part is moving
        self.liftIdx = (self.liftIdx + 1) % len(self.lift)

    def draw(self, shift): # draw plant
        for plantIdx in range(len(self.plants)):
            y, x = self.plants[plantIdx]
            x = (x * self.cellSize) - shift
            y = y * self.cellSize
            
            circleY = y + self.lift[self.liftIdx]
            circleX = x + self.cellSize // 2

            if self.liftIdx // 10 % 2 == 0:
                drawImage(self.imagePlant1, x, y + self.lift[self.liftIdx], width = self.cellSize, height = self.cellSize)
            else:
                drawImage(self.imagePlant2, x, y + self.lift[self.liftIdx], width = self.cellSize, height = self.cellSize)
            drawRect(x, y, self.cellSize, self.cellSize, fill='green')
            drawImage(self.imagePipe, x, y, width = self.cellSize, height = self.cellSize)
            
