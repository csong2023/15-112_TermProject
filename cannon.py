from cmu_graphics import *
from cannonball import CannonBall
import random
from PIL import Image

class Cannon:
    def __init__(self):
        self.cell_size = 40
        self.cannons = []
        self.cannonsCooldown = []
        # setting random cooldowns for the cannons (how frequently will a cannonball be released)
        self.cannonball = CannonBall()
        self.cooldownMin, self.cooldownMax = (200, 300)

        self.image = CMUImage(Image.open('images/cannon.png'))
    
    def click(self, x, y, shift, grid): # adding a cannon
        gridX = int((x + shift) // self.cell_size)
        gridY = int(y // self.cell_size)
        if (gridY, gridX) not in self.cannons and not grid[gridY][gridX]:
            self.cannons.append((gridY, gridX))
            self.cannonsCooldown.append(random.randint(self.cooldownMin, self.cooldownMax))

    def unclick(self, x, y, shift): # removing a cannon
        gridX = int((x + shift) // self.cell_size)
        gridY = int(y // self.cell_size)
        
        if (gridY, gridX) in self.cannons:
            self.cannonsCooldown.pop(self.cannons.index((gridY, gridX)))
            self.cannons.remove((gridY, gridX))

    def damage(self, mariox, marioy, shift): # detect damage of the cannonball
        if self.cannonball.damage(mariox, marioy, shift):
            return True
        return False

    def update(self, shift, grid, colorgrid): # update each cannonball 
        self.summon_cannonball(shift)
        self.cannonball.move(shift)
        self.cannonball.disappear(shift, grid, colorgrid)

    def summon_cannonball(self, shift): # for each cooldown, add cannonball and set cooldown to default
        for cannonIdx in range(len(self.cannons)):
            if self.cannonsCooldown[cannonIdx] == 0:
                self.cannonsCooldown[cannonIdx] = random.randint(self.cooldownMin, self.cooldownMax)
                y, x = self.cannons[cannonIdx]
                self.cannonball.add_cannonball(x * self.cell_size, y * self.cell_size, -1)
                self.cannonball.add_cannonball(x * self.cell_size, y * self.cell_size, 1)
            else:
                self.cannonsCooldown[cannonIdx] -= 1

    def draw(self, shift): # drawing cannons and cannonballs
        self.cannonball.draw(shift)
        for cannonIdx in range(len(self.cannons)):
            y, x = self.cannons[cannonIdx]
            drawRect(x * self.cell_size - shift, y * self.cell_size, 
                     self.cell_size, self.cell_size, fill='black')
            drawImage(self.image, x * self.cell_size - shift, y * self.cell_size, 
                      width = self.cell_size, height = self.cell_size)