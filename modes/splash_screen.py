from cmu_112_graphics import *

class SplashScreenMode(Mode):
    def appStarted(mode):
        pass

    def keyPressed(mode, event):
        mode.app.changeMode("game")

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        canvas.create_text(mode.width/2, mode.height/3, fill='white',
            text='Surviving College', font='Arial 18 bold')
        canvas.create_text(mode.width/2, 1.5*mode.height/3, fill='white',
            text='Press any key to start', font='Arial 18 bold')