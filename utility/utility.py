from tkinter import *
from PIL import Image, ImageTk
import pygame

class AssetLoader:
    @staticmethod
    def loadAssets(app, height, width):
        gridSize = 0.1 * height
        assets = {}
        assets["girl"] = AssetLoader.loadImage(app, "assets/images/girl.png", gridSize)
        assets["boy"] = AssetLoader.loadImage(app, "assets/images/boy.png", gridSize)

        assets["background1"] = AssetLoader.loadBackground(app, "assets/images/background1.jpg", height, width)
        assets["background2"] = AssetLoader.loadBackground(app, "assets/images/background2.jpg", height, width)
        assets["background3"] = AssetLoader.loadBackground(app, "assets/images/background3.jpg", height, width)
        assets["background4"] = AssetLoader.loadBackground(app, "assets/images/background4.jpg", height, width)
        assets["background5"] = AssetLoader.loadBackground(app, "assets/images/background5.jpg", height, width)
        
        assets["splashScreen"]=AssetLoader.loadImage(app,"assets/images/splash_screen.png")
        assets["endGame"]=AssetLoader.loadImage(app,"assets/images/endScreen.png")

        assets["alcohol"] = AssetLoader.loadImage(app, "assets/images/alcohol.png", gridSize)
        assets["badGrades"]=AssetLoader.loadImage(app, "assets/images/badGrades.png", gridSize)
        assets["fratParties"]=AssetLoader.loadImage(app, "assets/images/fratParties.png", gridSize)
        assets["noParents"]=AssetLoader.loadImage(app, "assets/images/noParents.png", gridSize)
        assets["freshman15"]=AssetLoader.loadImage(app, "assets/images/freshman15.png", gridSize)
        assets["noCar"]=AssetLoader.loadImage(app, "assets/images/noCar.png", gridSize)
        
        assets["breakUps"]=AssetLoader.loadImage(app, "assets/images/breakUps.png", gridSize)
        assets["time"]= AssetLoader.loadImage(app, "assets/images/time.png", gridSize)
        assets["stress"]= AssetLoader.loadImage(app, "assets/images/stress.png", gridSize)
        assets["badTime"]=AssetLoader.loadImage(app, "assets/images/badTime.png", gridSize)
        
        assets["depression"]=AssetLoader.loadImage(app, "assets/images/depression.png", gridSize)
        assets["stackHw"]=AssetLoader.loadImage(app, "assets/images/stackHw.png", gridSize)
        assets["meanProfessor"]=AssetLoader.loadImage(app, "assets/images/meanProfessor.png", gridSize)
        assets["drugs"]=AssetLoader.loadImage(app, "assets/images/drugs.png", gridSize)
        assets["noMoney"]=AssetLoader.loadImage(app, "assets/images/noMoney.png", gridSize)
        assets["parentsLeaving"]=AssetLoader.loadImage(app, "assets/images/parentsLeaving.png", gridSize)
        
        assets["sadness"]=AssetLoader.loadImage(app, "assets/images/sadness.png", gridSize)
        assets["noFriends"]=AssetLoader.loadImage(app, "assets/images/noFriends.png", gridSize)

        assets["goal1"]=AssetLoader.loadImage(app, "assets/images/goal1.png", gridSize)
        assets["goal2"]=AssetLoader.loadImage(app, "assets/images/goal2.png", gridSize)
        assets["goal3"]=AssetLoader.loadImage(app, "assets/images/goal3.png", gridSize)
        assets["goal4"]=AssetLoader.loadImage(app, "assets/images/gradCap.png", gridSize)

        assets["theme"] = pygame.mixer.Sound("assets/sounds/theme.wav")
        assets["mario"] = pygame.mixer.Sound("assets/sounds/mario.wav")
        
        return assets
        
    @staticmethod
    def loadImage(app, url, size=None):
        img = app.loadImage(url)
        if size is not None:
            height, width = img.size
            hRatio = size / height
            wRatio = size / width
            ratio = min(hRatio, wRatio)
            img = app.scaleImage(img, ratio, antialias=True)
        return ImageTk.PhotoImage(img)

    @staticmethod
    def loadBackground(app, url, height, width):
        img = app.loadImage(url)
        iHeight, iWidth = img.size

        hRatio = height / iHeight
        wRatio = width / iWidth
        ratio = max(hRatio, wRatio)

        img = app.scaleImage(img, ratio, antialias=True)

        return ImageTk.PhotoImage(img)