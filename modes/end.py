from cmu_112_graphics import *

class EndGameMode(Mode):
    def redrawAll(mode, canvas):
        endGame = mode.app.assets["endGame"]
        cx, cy = mode.app.width / 2, mode.app.height / 2
        canvas.create_image(cx, cy, image=endGame)

    def keyPressed(mode, event):
        mode.app.changeMode("splash")
        