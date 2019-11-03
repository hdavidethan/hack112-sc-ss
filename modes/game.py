from cmu_112_graphics import *
from constants import Constants
from utility.problem import Problem
from utility.player import Player
import random

class GameMode(Mode):
    def appStarted(mode):
        mode.delay = 5

        mode.gridSize = 0.1 * mode.height
        mode.margin = 3 * mode.gridSize

        mode.player = Player(mode)
        mode.levelStarted()

    def levelStarted(mode):
        mode.scrollX = 0
        mode.scrollY = 0

        mode.player.x = 0
        mode.player.y = 0

        mode.tickCounter = 0
        mode.initProblems()

    def initProblems(mode):
        mode.problems = []
        for i in range(16):
            if (i % 2 == 0):
                x = random.randint(0, Constants.gridWidth-2)
                y = random.randint(Constants.gridHeight//2, Constants.gridHeight-1)
                mode.problems.append(Problem(x, y, 'y', Problem.randomProblem(mode.player.currentYear)))
            else:
                x = random.randint(Constants.gridWidth//2, Constants.gridWidth-1)
                y = random.randint(0, Constants.gridHeight-2)
                mode.problems.append(Problem(x, y, 'x', Problem.randomProblem(mode.player.currentYear)))
        print(mode.problems)

    def getBounds(mode, col, row):
        return (mode.margin+(col+0.5)*mode.gridSize,
            mode.margin+(row+0.5)*mode.gridSize)

    def keyPressed(mode, event):
        player = mode.player
        if (event.key == 'Right'):
            player.movePlayer(+1, 0) 
        elif (event.key == 'Left'):
            player.movePlayer(-1, 0)
        elif (event.key == 'Up'):
            player.movePlayer(0, -1)
        elif (event.key == 'Down'):
            player.movePlayer(0, +1)
        elif (event.key == 'p'):
            mode.app.changeMode('pause')

    def timerFired(mode):
        if (mode.player.x == Constants.gridWidth-1 and mode.player.y == Constants.gridHeight-1):
            mode.levelUp()
        if (mode.tickCounter % mode.delay == 0):
            mode.tickCounter = 0
            for problem in mode.problems:
                if (problem.direction == 'x'):
                    problem.x -= 1
                    if (problem.x < 0):
                        problem.x = Constants.gridWidth - 1
                elif (problem.direction == 'y'):
                    problem.y -= 1
                    if (problem.y < 0):
                        problem.y = Constants.gridHeight - 1
        mode.tickCounter += 1
    
    def levelUp(mode, delay=False):
        mode.player.currentYear += 1
        mode.delay = max(mode.delay - 1, 1)
        if delay:
            mode.player.graduationYear += 1
        mode.levelStarted()

    def redrawAll(mode, canvas):
        mode.drawGrid(canvas)
        mode.drawProblems(canvas)
        mode.drawPlayer(canvas)
        mode.drawGUI(canvas)

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
    
    def drawProblems(mode, canvas):
        sx = mode.scrollX
        sy = mode.scrollY
        for problem in mode.problems:
            r = mode.player.radius
            cx, cy = mode.getBounds(problem.x, problem.y)
            canvas.create_rectangle(cx-r-sx, cy-r-sy, cx+r-sx, cy+r-sy,
                fill=Constants.FILL)

    def drawGUI(mode, canvas):
        GUI1 = 0.5 * mode.gridSize
        canvas.create_rectangle(0, 0, mode.width, GUI1, fill='white', width=0)
        canvas.create_text(mode.width/2, 0, anchor='n', 
            text=f'Year {mode.player.currentYear} of {mode.player.graduationYear}')