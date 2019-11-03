from cmu_112_graphics import *

class SplashScreenMode(Mode):
    def mousePressed(mode,event):
        if event.y > 2*(mode.height/3) and event.y < 6*(mode.height/7):
            if event.x > mode.width/4 and event.x < mode.width/2:
                mode.app.playerSex = "girl"
                mode.app.changeMode("game")
            if event.x > mode.width/2 and event.x < 3*(mode.width/4):
                mode.app.playerSex = "boy"
                mode.app.changeMode("game")
    def redrawAll(mode, canvas):
        splashScreen = mode.app.assets["splashScreen"]
        canvas.create_image(0,0, image=splashScreen, anchor="nw") #need to draw splash screen
        