##########################
#        HACK 112        #
#   _xXEl1t3_H4x0rzXx_   #
##########################

from cmu_112_graphics import *

from modes.splash_screen import SplashScreenMode
from modes.game import GameMode
from modes.end import EndGameMode
from utility.utility import AssetLoader
from utility.kinect import *
import pygame.mixer

import random

class SurvivingCollege(ModalApp):
    MODE_GAME =  "game"
    MODE_SPLASH = "splash"

    def appStarted(app):
        app.assets = AssetLoader.loadAssets(app, app.height, app.width)
        app.initializeModes()
        app.changeMode("splash")
        app.playerSex = None

        app.kinectGame = GameRuntime(app)
        app.kinectGame.calibrate()
        app.kinectGame.run()

        pygame.mixer.Channel(0).play(app.assets["theme"], loops=-1)
        
    def initializeModes(app):
        app.modes = {
            "game": GameMode(),
            "splash": SplashScreenMode(),
            "endGame": EndGameMode()
        }

    def changeMode(app, mode):
        app.setActiveMode(app.modes[mode])

if __name__ == "__main__":
    SurvivingCollege(width=Constants.SCREEN_WIDTH, height=Constants.SCREEN_HEIGHT)