from cmu_graphics import *
from PIL import Image

def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

class CannonBall:
    def __init__(self):
        self.ball_radius = 20
        self.cannonSize = 40
        self.cannonBalls = []
        self.directions = []
        self.image = CMUImage(Image.open('images/cannonball.png'))
        self.image2 = CMUImage(Image.open('images/cannonball.png').transpose(Image.FLIP_LEFT_RIGHT))

    def add_cannonball(self, x, y, dir): # summon a cannonball
        self.cannonBalls.append((x, y))
        self.directions.append(dir)

    def move(self, shift): # moving cannonballs
        for cannonBallIdx in range(len(self.cannonBalls)):
            x, y = self.cannonBalls[cannonBallIdx]
            self.cannonBalls[cannonBallIdx] = (x + self.directions[cannonBallIdx], y)
    
    def disappear(self, shift, grid, colorgrid): # cannonballs disappear when contacting mario / a block
        for cannonBallIdx in range(len(self.cannonBalls)): 
            x, y = self.cannonBalls[cannonBallIdx]
            x = x + self.cannonSize / 2
            y = y + self.cannonSize / 2
            grid_x, grid_y = int(x // self.cannonSize), int(y // self.cannonSize)
            if grid[grid_y][grid_x] and not colorgrid[grid_y][grid_x]:
                self.cannonBalls.pop(cannonBallIdx)
                self.directions.pop(cannonBallIdx)
                break

    def damage(self, mariox, marioy, shift): # inflict damage if touching mario
        for cannonBallIdx in range(len(self.cannonBalls)):
            x, y = self.cannonBalls[cannonBallIdx]
            if distance(mariox, marioy, x - shift + self.cannonSize / 2, y + self.cannonSize / 2) <= self.ball_radius:
                self.cannonBalls.pop(cannonBallIdx)
                self.directions.pop(cannonBallIdx)
                return True
        return False

    def draw(self, shift): # draw cannonball
        for cannonBallIdx in range(len(self.cannonBalls)): 
            x, y = self.cannonBalls[cannonBallIdx]
            if self.directions[cannonBallIdx] == 1: 
                drawImage(self.image, x - shift + self.cannonSize / 2, y + self.cannonSize / 2, 
                          width = self.ball_radius, height = self.ball_radius, align='center')
            else:
                drawImage(self.image2, x - shift + self.cannonSize / 2, y + self.cannonSize / 2, 
                          width = self.ball_radius, height = self.ball_radius, align='center')
