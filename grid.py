from cmu_graphics import *
from PIL import Image

class Grid:
    def __init__(self, rows, cols, cellSize):
        self.image = CMUImage(Image.open('images/grid.png'))
        self.rows = rows
        self.cols = cols
        self.cellSize = cellSize
        self.grid = [[False for _ in range(cols)] for _ in range(rows)]
        self.colorgrid = [[False for _ in range(cols)] for _ in range(rows)]

    def click(self, x, y, shift): # add grid
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        if 0 <= gridX < self.cols and 0 <= gridY < self.rows:
            self.grid[gridY][gridX] = True

    def colorclick(self, x, y, shift): # for other objects using the grid (ex. plant), add color
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        if 0 <= gridX < self.cols and 0 <= gridY < self.rows:
            self.colorgrid[gridY][gridX] = True

    def unclick(self, x, y, shift): # remove block
        gridX = int((x + shift) // self.cellSize)
        gridY = int(y // self.cellSize)
        
        if 0 <= gridX < self.cols and 0 <= gridY < self.rows:
            self.grid[gridY][gridX] = False

    def draw(self, shift): # draw grid
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x]:
                    drawRect((x * self.cellSize) - shift, y * self.cellSize, self.cellSize, self.cellSize)
                    drawImage(self.image, (x * self.cellSize) - shift, y * self.cellSize, 
                              width = self.cellSize, height = self.cellSize)
