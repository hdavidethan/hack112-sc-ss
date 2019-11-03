##########################
#        HACK 112        #
#   _xXEl1t3_H4x0rzXx_   #
##########################

from cmu_112_graphics import *

from modes.splash_screen import SplashScreenMode
from modes.game import GameMode
from modes.pause import PauseMode
from utility.utility import AssetLoader

import random

class SurvivingCollege(ModalApp):
    MODE_GAME =  "game"
    MODE_SPLASH = "splash"
    MODE_PAUSE = "pause"

    def appStarted(app):
        app.isFullscreen = False
        app.cacheSize = (app.height, app.width)
        app.assets = AssetLoader.loadAssets(app, app.height, app.width)
        app.initializeModes()
        app.changeMode("splash")
        
    def initializeModes(app):
        app.modes = {
            "game": GameMode(),
            "splash": SplashScreenMode(),
            "pause": PauseMode()
        }

    def changeMode(app, mode):
        app.setActiveMode(app.modes[mode])

    def timerFired(app):
        super().timerFired()
        # detect if window size was changed
        if app.cacheSize != (app.height, app.width):
            app.cacheSize = app.height, app.width
            app.assets = AssetLoader.loadAssets(app, app.height, app.width)

if __name__ == "__main__":
    SurvivingCollege(width=960, height=780)