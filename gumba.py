from cmu_graphics import *
import math
from PIL import Image


class Gumba:
    def __init__(self):
        self.cellSize = 40
        self.gumbas = []
        self.dir = []
        self.dist = []
        self.drawMessage = 0
        self.errorMessage = "Gumba CANNOT be placed there!"
        self.opacity = 100
        self.textSize = 20

        self.image = CMUImage(Image.open('images/gumba.png'))

        
    def click(self, x, y, shift, grid): # add gumba
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        
        if gridY == len(grid) - 1 or grid[gridY + 1][gridX]:
            if (gridY, gridX) not in self.gumbas and not grid[gridY][gridX]:
                self.gumbas.append((gridY, gridX))
                self.dir.append(-1)
                self.dist.append(0)
                print(gridX)
        else: # error message if gumba can not be placed
            self.opacity = 100 
            self.drawMessage = 1

    def damage(self, mariox, marioy, shift): # inflict damage if contacting mario
        for i in range(len(self.gumbas)):
            y, x = self.gumbas[i]
            x = (x * self.cellSize) - shift + self.dist[i]
            y = y * self.cellSize
            if (x - self.cellSize / 2 <= mariox <= x + self.cellSize + self.cellSize / 2 
                and y - self.cellSize / 2 <= marioy <= y + self.cellSize + self.cellSize / 2):
                return True
        return False
    
    def update(self): 
        if self.opacity > 0:
            self.opacity -= 1
        else:
            self.drawMessage = 0

    def move(self, shift, grid): # gumba movement
        for i in range(len(self.gumbas)):
            gridY, x = self.gumbas[i]
            gridX = (x * self.cellSize + self.dist[i]) // self.cellSize
            direction = self.dir[i]
            if direction == -1:
                if grid[gridY][gridX]:
                    self.dir[i] *= -1
                    continue
                if gridY == 19 or grid[gridY + 1][gridX]:
                    self.dist[i] += self.dir[i]
                else:
                    self.dir[i] *= -1
            else:
                if grid[gridY][gridX + 1]:
                    self.dir[i] *= -1
                    continue
                if gridY == 19 or grid[gridY + 1][gridX + 1]:
                    self.dist[i] += self.dir[i]
                else:
                    self.dir[i] *= -1

    def unclick(self, x, y, shift): # remove gumba
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        
        if (gridY, gridX) in self.gumbas:
            self.dir.pop(self.gumbas.index((gridY, gridX)))
            self.dist.pop(self.gumbas.index((gridY, gridX)))
            self.gumbas.remove((gridY, gridX))
    
    def draw(self, shift, height, width): # draw gumba
        if self.drawMessage:
            drawLabel(self.errorMessage, height / 2, width / 2, 
                      size = self.textSize, opacity = self.opacity, fill='red')
        for i in range(len(self.gumbas)):
            y, x = self.gumbas[i]
            x = (x * self.cellSize) - shift + self.dist[i]
            y = y * self.cellSize
            drawRect(x, y, self.cellSize, self.cellSize, fill=None)
            drawImage(self.image, x, y, width = self.cellSize, height = self.cellSize)