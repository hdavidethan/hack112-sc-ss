from cmu_112_graphics import *
from constants import Constants
from utility.problem import Problem
from utility.player import Player
from PIL import Image, ImageTk
import random
import pygame

class GameMode(Mode):
    def appStarted(mode):
        mode.delay = 5

        mode.gridSize = 0.1 * mode.height
        mode.margin = 3 * mode.gridSize

        mode.player = Player(mode)
        mode.player.sex = mode.app.playerSex
        mode.levelStarted()

    def levelStarted(mode, repeat=False):
        mode.scrollX = 0
        mode.scrollY = 0

        mode.player.x = 0
        mode.player.y = 0

        mode.tickCounter = 0
        mode.initProblems()
        mode.showWelcome = True
        mode.repeat = repeat

    def initProblems(mode):
        mode.problems = set()
        for i in range(16):
            if (i % 2 == 0):
                x = random.randint(0, Constants.gridWidth-2)
                y = random.randint(Constants.gridHeight//2, Constants.gridHeight-1)
                mode.problems.add(Problem(x, y, 'y', Problem.randomProblem(mode.player.currentYear)))
            else:
                x = random.randint(Constants.gridWidth//2, Constants.gridWidth-1)
                y = random.randint(0, Constants.gridHeight-2)
                mode.problems.add(Problem(x, y, 'x', Problem.randomProblem(mode.player.currentYear)))

    def getBounds(mode, col, row):
        return (mode.margin+(col+0.5)*mode.gridSize,
            mode.margin+(row+0.5)*mode.gridSize)

    def direction(mode, dir):
        if mode.showWelcome:
            mode.showWelcome = False
            return
        player = mode.player
        oldX, oldY = player.x, player.y
        if (dir == 'Right'):
            player.movePlayer(+1, 0) 
        elif (dir == 'Left'):
            player.movePlayer(-1, 0)
        elif (dir == 'Up'):
            player.movePlayer(0, -1)
        elif (dir == 'Down'):
            player.movePlayer(0, +1)

        x, y = player.x, player.y
        if x != oldX and y != oldY:
            mode.collidePlayer()

    def collidePlayer(mode):
        px, py = mode.player.x, mode.player.y
        for problem in mode.problems:
            x, y = problem.x, problem.y
            if x == px and y == py:
                mode.levelStarted(repeat=True)
                pygame.mixer.Channel(1).play(mode.app.assets["mario"])
                return


    def timerFired(mode):
        if mode.showWelcome:
            return
        if (mode.player.x == Constants.gridWidth-1 and mode.player.y == Constants.gridHeight-1):
            mode.levelUp()
        moveTiles = mode.tickCounter % mode.delay == 0
        px, py = mode.player.x, mode.player.y
        for problem in mode.problems:
            if moveTiles:
                mode.tickCounter = 0
                if (problem.direction == 'x'):
                    problem.x -= 1
                    if (problem.x < 0):
                        problem.x = Constants.gridWidth - 1
                elif (problem.direction == 'y'):
                    problem.y -= 1
                    if (problem.y < 0):
                        problem.y = Constants.gridHeight - 1
        mode.collidePlayer()
        mode.tickCounter += 1
    
    def levelUp(mode):
        mode.player.currentYear += 1
        if mode.player.currentYear == 5:
            mode.app.changeMode("endGame")
            return
        mode.levelStarted()

    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawGrid(canvas)
        mode.drawProblems(canvas)
        mode.drawPlayer(canvas)
        mode.drawGUI(canvas)
        if mode.showWelcome:
            mode.drawWelcome(canvas)

    def drawWelcome(mode, canvas):
        year = mode.player.currentYear
        width, height = mode.app.width, mode.app.height
        cx, cy = width / 2, height / 2

        rect = mode.createTransparentRectangle(0, 0, width, height)
        canvas.create_image(0, 0, image=rect, anchor="nw")

        if mode.repeat:
            canvas.create_rectangle(cx-width/4, cy-height/8, cx+width/4, cy+height/8, fill="white", outline="white")
            canvas.create_text(width/2,height/2-30,text=f"You got held back!",
                font="courier 20 bold",fill="black", width=width/2)
            canvas.create_text(width/2,height/2,text=f"Welcome back to year {year}!",
                font="courier 20 bold",fill="black", width=width/2)
            canvas.create_text(width/2,height/2+30,text=f"Press any key to start.",
                font="courier 14 bold",fill="black", width=width/2)
        else:
            canvas.create_rectangle(cx-width/4, cy-height/16, cx+width/4, cy+height/16, fill="white", outline="white")
            canvas.create_text(width/2,height/2,text=f"Welcome to year {year}!",
                font="courier 20 bold",fill="black", width=width/2)
            canvas.create_text(width/2,height/2+30,text=f"Press any key to start.",
                font="courier 14 bold",fill="black", width=width/2)

    def createTransparentRectangle(mode, x1, y1, x2, y2):
        rgba = (255, 255, 255, 100)
        image = Image.new("RGBA", (x2-x1, y2-y1), rgba)
        return ImageTk.PhotoImage(image)
    
    def drawBackground(mode,canvas):
        level = mode.player.getLevel()
        background = mode.app.assets[f"background{level}"]
        canvas.create_image(0, 0, anchor="nw", image=background)

    def drawPlayer(mode, canvas):
        mode.player.draw(mode, canvas)

    def drawGrid(mode, canvas):
        sx = mode.scrollX
        sy = mode.scrollY

        tx = mode.margin - sx
        ty = mode.margin - sy
        bx = mode.margin + mode.gridSize*Constants.gridWidth - sx
        by = mode.margin + mode.gridSize*Constants.gridHeight - sy

        canvas.create_rectangle(tx, ty, bx, by)
        
        for i in range(Constants.gridWidth):
            for j in range(Constants.gridHeight):
                x0 = mode.margin + i * mode.gridSize - sx
                y0 = mode.margin + j * mode.gridSize - sy
                x1 = mode.margin + (i + 1) * mode.gridSize - sx
                y1 = mode.margin + (j + 1) * mode.gridSize - sy
                canvas.create_rectangle(x0, y0, x1, y1)
                if i == Constants.gridWidth - 1 and j == Constants.gridHeight - 1:
                    level = mode.player.getLevel()
                    img = mode.app.assets[f"goal{level}"]
                    canvas.create_image(x0, y0, anchor="nw", image=img)
    
    def drawProblems(mode, canvas):
        for problem in mode.problems:
            problem.draw(mode, canvas)

    def drawGUI(mode, canvas):
        GUI1 = 0.5 * mode.gridSize
        canvas.create_text(mode.width/2, 20, anchor='n', 
            text=f'Year {mode.player.currentYear} of {mode.player.graduationYear}',font="courier 25 bold")
        canvas.create_text(mode.width/2,70, text="Avoid all the things that can set you back",font="courier 20 bold")
        canvas.create_text(mode.width/2,90, text="by moving up, down, left and right",font="courier 20 bold")