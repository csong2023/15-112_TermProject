from cmu_graphics import *
from mario import Mario
from castle import Castle
from button import Button
from grid import Grid
from fire import Fire
from instructions import Instructions
from gumba import Gumba
from plant import Plant
from cannon import Cannon
from PIL import Image

'''
Image Sources:
Cannon & Cannonball: https://www.pixilart.com/art/bullet-bill-and-cannon-super-mario-bros-d28470dd1f9d0e8
Plant: https://tenor.com/view/piranha-plant-super-smash-bros-super-mario-piranha-piranhas-gif-13386962
Grid & Pipe & Gumba: https://www.deviantart.com/zedic0n/art/8-bit-Mario-Sprites-945075341
Fire: https://tenor.com/view/fire-bar-mario-mario-obsticle-get-real-real-gif-21175776
Heart(life): https://www.deviantart.com/joshuat1306/art/Super-Mario-Heart-2D-786384022
Background: https://www.freepik.com/free-photos-vectors/mario-background
Castle: https://www.youtube.com/watch?v=yOHaO-Bn90Q
Font: https://www.fontbolt.com/font/super-mario-maker-font/
Mario: https://www.pixilart.com/draw/mario-sprite-sheet-c8cb88f1ea7ee2d
'''

def onAppStart(app):
    app.stepsPerSecond = 30
    app.grid = Grid(20, 80, 40)
    app.fire = Fire(40)
    app.damageCooldown = 0
    app.mario = Mario()
    app.gumba = Gumba()
    app.plant = Plant()
    app.cannon = Cannon()
    app.castle = Castle(app.width + 800, app.height - 40)
    app.buttons = Button()
    app.selected = "block"
    app.event = 0
    # 0: Start, 1: Setup, 2: Play, 3: Win, 4: Lose
    app.shift = 0
    app.rotation = 0

    app.instructions = Instructions()
    app.show_instructions = -1

    app.titleImage = CMUImage(Image.open('images/title.png'))
    app.backgroundImage = CMUImage(Image.open('images/background.png'))
    app.heartImage = CMUImage(Image.open('images/heart.png'))
    app.winImage = CMUImage(Image.open('images/win.png'))
    app.loseImage = CMUImage(Image.open('images/lose.png'))

    app.titleImagesize = 300

def redrawAll(app):
    drawImage(app.backgroundImage, - app.shift, 0, width = app.width * 3, height = app.height)
    if app.event == 0:
        drawImage(app.titleImage, 0, 300, width = app.width, height = app.titleImagesize)
        app.instructions.drawInstructionButton()
        if app.show_instructions == 1:
            app.instructions.drawInstructions(app.height, app.width)
    if app.event == 1:
        app.buttons.draw()
        app.grid.draw(app.shift)
        app.fire.draw(app.shift, app.rotation)
        app.gumba.draw(app.shift, app.height, app.width)
        app.plant.draw(app.shift)
        app.cannon.draw(app.shift)
        app.castle.draw(app.shift, app.height, app.width)
        drawLabel(f'Currently Selected: {app.selected}', 400, 200, size=30, bold=True)
    elif app.event == 2:
        app.grid.draw(app.shift)
        app.fire.draw(app.shift, app.rotation)
        app.gumba.draw(app.shift, app.height, app.width)
        app.plant.draw(app.shift)
        app.cannon.draw(app.shift)
        drawImage(app.heartImage, 100, 100, width = 60, height = 60, align='center')
        drawLabel(f'X {app.mario.life}', 150, 100, size=20)
        if app.damageCooldown % 6 == 0:
            app.mario.draw()
        app.castle.draw(app.shift, app.height, app.width)
    elif app.event == 3:
        drawImage(app.winImage, 200, 300, width = 400, height = 200)
    elif app.event == 4:
        drawImage(app.loseImage, 200, 300, width = 400, height = 200)

def onStep(app):
    if app.damageCooldown > 0:
        app.damageCooldown -= 1
    app.shift += app.mario.scrollScreen()
    app.mario.update(app.grid, app.shift)
    app.gumba.update()
    if app.event == 2:
        app.gumba.move(app.shift, app.grid.grid)
        app.plant.update()
        app.cannon.update(app.shift, app.grid.grid, app.grid.colorgrid)
        app.rotation += 0.0005
        if app.fire.damage(app.mario.x, app.mario.y, app.rotation, app.shift) and app.damageCooldown <= 0:
            app.mario.life -= 1
            app.damageCooldown = 150
        elif app.gumba.damage(app.mario.x, app.mario.y, app.shift) and app.damageCooldown <= 0:
            app.mario.life -= 1
            app.damageCooldown = 150
        elif app.plant.damage(app.mario.x, app.mario.y, app.shift) and app.damageCooldown <= 0:
            app.mario.life -= 1
            app.damageCooldown = 150
        elif app.cannon.damage(app.mario.x, app.mario.y, app.shift) and app.damageCooldown <= 0:
            app.mario.life -= 1
            app.damageCooldown = 150

    if app.mario.checkwin(app.shift, app.castle.x, app.castle.y) and app.event == 2:
        app.event = 3
        app.shift = 0
    
    if app.mario.life == 0:
        app.event = 4
        app.shift = 0

def onKeyHold(app, keys):
    if app.event == 2:
        if 'right' in keys:
            app.mario.moveRight()
        if 'left' in keys and (app.shift > 0 or app.mario.x >= 130):
            app.mario.moveLeft()

def onMousePress(app, mouseX, mouseY):
    if app.event == 0:
        if app.instructions.buttonPress(mouseX, mouseY):
            app.show_instructions *= -1
    elif app.event == 1:
        if mouseY <= 400:
            if app.buttons.buttonPress(mouseX, mouseY) == 'PLAY':
                app.shift = 0
                app.event = 2
            else:
                app.selected = app.buttons.buttonPress(mouseX, mouseY)
        elif mouseY >= 400:
            if app.selected == 'BLOCK':
                app.grid.click(mouseX, mouseY, app.shift)
            elif app.selected == 'FIRE':
                app.grid.click(mouseX, mouseY, app.shift)
                app.fire.addfire(mouseX, mouseY, app.shift)
            elif app.selected == 'DELETE':
                app.grid.unclick(mouseX, mouseY, app.shift)
                app.fire.unclick(mouseX, mouseY, app.shift)
                app.gumba.unclick(mouseX, mouseY, app.shift)
                app.plant.unclick(mouseX, mouseY, app.shift)
                app.cannon.unclick(mouseX, mouseY, app.shift)
            elif app.selected == 'GUMBA':
                app.gumba.click(mouseX, mouseY, app.shift, app.grid.grid)
            elif app.selected == 'PLANT':
                app.plant.click(mouseX, mouseY, app.shift, app.grid.grid)
                app.grid.click(mouseX, mouseY, app.shift)
            elif app.selected == 'CANNON':
                app.cannon.click(mouseX, mouseY, app.shift, app.grid.grid)
                app.grid.click(mouseX, mouseY, app.shift)
                app.grid.colorclick(mouseX, mouseY, app.shift)

def onKeyPress(app, key):
    if app.event == 0 and key == 'space':
        app.event = 1 
    elif app.event == 1:
        if key == 'right':
            app.shift += 40
        if key == 'left':
            app.shift -= 40
    elif app.event == 2:
        if key == 'space':
            app.mario.jump()
    elif app.event == 3 or app.event == 4:
        if key == 'r':
            restartApp(app)
            app.event = 0
    
def restartApp(app):
    onAppStart(app)

def main():
    runApp(width=800, height=800)

main()
