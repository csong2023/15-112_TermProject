from cmu_graphics import *
from PIL import Image

class Castle:
    def __init__(self, x, y): # Set where the castle would be
        self.x = x
        self.y = y
        self.mapSize = 1600 # Starting at the end of the map
        self.image = CMUImage(Image.open('images/castle.png'))
        
    def draw(self, shift, canvasHeight, canvasWidth): # Draw the castle
        drawImage(self.image, self.mapSize - shift, canvasHeight - canvasHeight // 4, height = canvasHeight // 4, width = canvasWidth // 4)
