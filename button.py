from cmu_graphics import *
from PIL import Image

class Button:
    def __init__(self):
        # Button dimensions setup
        self.buttons = [(i * 110 + 30, 25) for i in range(7)]
        self.buttonWidth = 75
        self.buttonHeight = 50
        self.imageSize = 15
        self.imageGap = 10
        # Images for buttons
        self.gridImage = CMUImage(Image.open('images/grid.png'))
        self.fireImage = CMUImage(Image.open('images/fire.png'))
        self.gumbaImage = CMUImage(Image.open('images/gumba.png'))
        self.pipeImage = CMUImage(Image.open('images/pipe.png'))
        self.cannonImage = CMUImage(Image.open('images/cannon.png'))
        self.images = [None, self.gridImage, self.fireImage, self.gumbaImage, self.pipeImage, self.cannonImage, None]
        # Button Labels Setup
        self.buttonLabels = ['DELETE', 'BLOCK', 'FIRE', 'GUMBA', 'PLANT', 'CANNON', 'PLAY']

    def buttonPress(self, mouseX, mouseY): # Detect any button press
        for buttonIdx in range(len(self.buttons)):
            buttonX, buttonY = self.buttons[buttonIdx]
            if 0 <= (mouseX - buttonX) <= self.buttonWidth and abs(buttonY - mouseY) <= self.buttonHeight:
                return self.buttonLabels[buttonIdx]
        return 'None Selected'

    def draw(self): # Draw Buttons
        for buttonIdx in range(len(self.buttons)):
            x, y = self.buttons[buttonIdx]
            drawRect(x, y, self.buttonWidth, self.buttonHeight, fill='black', border='red')
            if self.images[buttonIdx] == None:
                drawLabel(self.buttonLabels[buttonIdx], x + self.buttonWidth / 2, y + self.buttonHeight / 2, 
                          size = self.imageSize, bold=True, fill='white')
            else:
                drawImage(self.images[buttonIdx], x + self.buttonWidth / 2, y + self.buttonHeight / 2, 
                          width = self.buttonWidth - self.imageGap * 2, height = self.buttonHeight - self.imageGap, align='center')

