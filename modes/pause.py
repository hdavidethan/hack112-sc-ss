from cmu_112_graphics import *
from constants import Constants

class PauseMode(Mode):
    def appStarted(mode):
        pass
    
    def keyPressed(mode, event):
        mode.app.changeMode('game')
    
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height,
            fill=Constants.PAUSE_BG)
        canvas.create_text(mode.width/2, mode.height/2, text='Game Paused',
            fill='yellow')