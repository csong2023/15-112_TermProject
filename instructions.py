from cmu_graphics import *
from PIL import Image

def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

class Instructions:
    def __init__(self): # import instructions image
        self.image = CMUImage(Image.open('images/instructions.png'))
        self.buttonText = "?"
        self.buttonTextSize = 40
        self.buttonRadius = 30
        self.buttonX = 750
        self.buttonY = 750
    
    def buttonPress(self, mouseX, mouseY): # detect button press for instructions
        if distance(mouseX, mouseY, self.buttonX, self.buttonY) <= self.buttonRadius:
            return True
        return False

    def drawInstructionButton(self): # create button for instruction
        drawCircle(self.buttonX, self.buttonY, self.buttonRadius, fill = 'white', border = 'black')
        drawLabel(self.buttonText, self.buttonX, self.buttonY, size = self.buttonTextSize, bold = True)

    def drawInstructions(self, canvasHeight, canvasWidth): # draw instructions
        drawImage(self.image, app.height // 4, app.width // 4, 
                  width = app.width // 2, height = app.height // 2)
        