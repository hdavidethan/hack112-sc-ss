from tkinter import *
from PIL import Image, ImageTk

class AssetLoader:
    @staticmethod
    def loadAssets(app, height, width):
        gridSize = 0.1 * height

        assets = {}
        assets["girl"] = AssetLoader.loadImage(app, "assets/images/girl.png", gridSize)
        assets["boy"] = AssetLoader.loadImage(app, "assets/images/boy.png", gridSize)

        assets["background1"] = AssetLoader.loadImage(app, "assets/images/background1.jpg")
        assets["background2"] = AssetLoader.loadImage(app, "assets/images/background2.jpg")
        assets["background3"] = AssetLoader.loadImage(app, "assets/images/background3.jpg")
        assets["background4"] = AssetLoader.loadImage(app, "assets/images/background4.jpg")
        assets["background5"] = AssetLoader.loadImage(app, "assets/images/background5.jpg")
        assets["splashScreen"]=AssetLoader.loadImage(app,"assets/images/splash_screen.png")

        assets["alcohol"] = AssetLoader.loadImage(app, "assets/images/alcohol.png", gridSize)
        assets["badGrades"]=AssetLoader.loadImage(app, "assets/images/badGrades.png", gridSize)
        assets["fratParties"]=AssetLoader.loadImage(app, "assets/images/fratParties.png", gridSize)
        assets["noParents"]=AssetLoader.loadImage(app, "assets/images/noParents.jpeg", gridSize)
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

        assets["goal1"]=AssetLoader.loadImage(app, "assets/images/goal1.png")
        assets["goal2"]=AssetLoader.loadImage(app, "assets/images/goal2.png")
        assets["goal3"]=AssetLoader.loadImage(app, "assets/images/goal3.png")
        assets["goal4"]=AssetLoader.loadImage(app, "assets/images/goal4.png")
        
        assets["gradCap"]=AssetLoader.loadImage(app, "assets/images/gradCap.png")
        
    @staticmethod
    def loadImage(app, url, size=None):
        if size is not None:
            height, width = size
            img = app.loadImage(url)
            img.resize(width, height)
            return ImageTk.PhotoImage(img)
        else:
            img = app.loadImage(url)
            return ImageTk.PhotoImage(img)