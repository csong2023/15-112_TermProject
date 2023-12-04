from cmu_graphics import *
from PIL import Image

class Mario:
    def __init__(self):
        self.radius = 40
        self.height = 800
        self.width = 800
        self.x = 150
        self.y = self.height - self.radius
        self.initialVelocity = 10
        self.gravity = 0.5
        self.isJumping = False
        self.life = 3
        self.speed = 5
        self.dir = 1

        self.marioImageIdx = 0
        self.marioImages = [CMUImage(Image.open('images/mario1.png')), CMUImage(Image.open('images/mario2.png')), CMUImage(Image.open('images/mario3.png'))]
        self.marioJumpingimage = CMUImage(Image.open('images/mariojumping.png'))
        self.marioImages2 = [CMUImage(Image.open('images/mario1.png').transpose(Image.FLIP_LEFT_RIGHT)), CMUImage(Image.open('images/mario2.png').transpose(Image.FLIP_LEFT_RIGHT)), CMUImage(Image.open('images/mario3.png').transpose(Image.FLIP_LEFT_RIGHT))]
        self.marioJumpingimage2 = CMUImage(Image.open('images/mariojumping.png').transpose(Image.FLIP_LEFT_RIGHT))
        self.imageSwitchSteps = 30

    def jump(self): # jump function for mario
        if not self.isJumping:
            self.isJumping = True
            self.initialVelocity = 10

    def checkCollision(self, grid, shift): # check mario's collision with grids
        gridX = int((self.x + shift) // grid.cellSize)
        gridY = int(self.y // grid.cellSize)

        if 0 <= gridX < grid.cols and 0 <= gridY + 1 < grid.rows:
            if grid.grid[gridY + 1][gridX]: # if there's a block below, adjust Mario's position and reset jumping
                if self.y + self.radius > (gridY + 1) * grid.cellSize:
                    self.isJumping = False
                    self.y = (gridY + 1) * grid.cellSize - self.radius
            else: # if there's no block below, allow Mario to fall
                self.isJumping = True
        

    def update(self, grid, shift): # update current mario state
        if self.isJumping:
            self.y -= self.initialVelocity
            self.initialVelocity -= self.gravity
        self.checkCollision(grid, shift)
        if self.y >= self.height - self.radius:
            self.isJumping = False
            self.y = self.height - self.radius

    def moveLeft(self): # mario moving left
        self.x -= self.speed
        self.dir = -1
        self.marioImageIdx += 1
        self.marioImageIdx %= self.imageSwitchSteps

    def moveRight(self): # mario moving right
        self.x += self.speed
        self.dir = 1
        self.marioImageIdx += 1
        self.marioImageIdx %= self.imageSwitchSteps

    def draw(self): # use different image depending on mario state
        if self.dir == 1:
            if self.isJumping:
                drawImage(self.marioJumpingimage, self.x, self.y, width = self.radius, height = self.radius, align='center')
            else:
                drawImage(self.marioImages[self.marioImageIdx // 10], self.x, self.y + 20, width = self.radius, height = self.radius, align='center')
        else:
            if self.isJumping:
                drawImage(self.marioJumpingimage2, self.x, self.y, width = self.radius, height = self.radius, align='center')
            else:
                drawImage(self.marioImages2[self.marioImageIdx // 10], self.x, self.y + 20, width = self.radius, height = self.radius, align='center')

    def scrollScreen(self): # if mario is near the edge of the screen, shift screen
        if self.x >= self.width - 200:
            self.x = self.width - 200
            return self.speed 
        elif self.x <= 100:
            self.x = 100
            return -1 * self.speed  
        return 0  # if mario not near edges, no shift required
    
    def checkwin(self, shift, castleX, castleY): # check any win status (reaching the end of the map)
        if castleX - shift <= self.x:
            return True
        return False
