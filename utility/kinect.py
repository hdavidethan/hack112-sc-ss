from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random
import time

from constants import Constants
from modes.game import *

class GameRuntime(object):
    def __init__(self, app):
        pygame.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("assets/sounds/theme.wav"))

        self.screenWidth = Constants.SCREEN_WIDTH
        self.screenHeight = Constants.SCREEN_HEIGHT
        self.app = app

        self.prevSpineBaseX = 0
        self.prevSpineBaseY = 0
        self.curSpineBaseX = 0
        self.curSpineBaseY = 0
        self.differenceSpineBaseX=0
        self.differenceSpineBaseY=0

        self.samePositionCounter=0
        self.samePositionAmount=10
        
        self.originalSpineBaseY=None

        self.currentSpineBaseX=0
        self.currentSpineBaseY=0

        self.resetYRange=self.screenHeight/36
        self.significantYChange=self.screenHeight/20


        self.moveLeft=False
        self.moveRight=False
        self.moveUp=False
        self.moveDown=False

        self.gameover = False
        self.calibration=False
        
        self.resetPos=False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Set the width and height of the window [width/2, height/2]
        self.screen = pygame.display.set_mode((960,540), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)

        # Loop until the user clicks the close button.
        self.done = False

        # Kinect runtime object, we want color and body frames 
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self.bodies = None

    def changeDirection(self):
        self.changeYPosition=self.differenceSpineBaseY*80
        self.changeXPosition=self.differenceSpineBaseX*80

        if(self.changeXPosition<-1): #left
            if(self.moveRight!=True and (self.currentSpineBaseX<self.originalHipLeft or self.currentSpineBaseX>self.originalHipRight)):
                self.moveLeft=True
                app.modes['game'].direction('Left')
        elif(self.changeXPosition>1): #right
            if(self.moveLeft!=True and (self.currentSpineBaseX<self.originalHipLeft or self.currentSpineBaseX>self.originalHipRight)):
                self.moveRight=True
                app.modes['game'].direction('Right')
        elif(self.changeYPosition<-1): #down
            if(self.moveUp!=True and (self.resetPos==True or self.currentSpineBaseY>self.originalSpineBaseY+self.resetYRange or self.currentSpineBaseY<self.originalSpineBaseY-self.resetYRange)):
                self.moveDown=True
                app.modes['game'].direction('Down')
        elif(self.changeYPosition>1): #up
            if(self.moveDown!=True and (self.resetPos==True or self.currentSpineBaseY>self.originalSpineBaseY+self.resetYRange or self.currentSpineBaseY<self.originalSpineBaseY-self.resetYRange)):
                self.moveUp=True
                app.modes['game'].direction('Up')

    def reset(self):
        self.currentSpineBaseX=(self.curSpineBaseX+1)*self.screenWidth/2
        self.currentSpineBaseY=(1-self.curSpineBaseY)*self.screenHeight/2
        if(self.currentSpineBaseX>self.originalHipLeft and self.currentSpineBaseX<self.originalHipRight and self.currentSpineBaseY<self.originalSpineBaseY+self.resetYRange and self.currentSpineBaseY>self.originalSpineBaseY-self.resetYRange):
            self.moveRight=False
            self.moveLeft=False
            self.moveUp=False
            self.moveDown=False

    def drawColorFrame(self, frame, targetSurface):
        targetSurface.lock()
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        # replacing old frame with new one
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        targetSurface.unlock()

    def calibrate(self):
        while not self.calibration:
            if self.gameover:
                font = pygame.font.Font(None, 36)
                text = font.render("Game over!", 1, (0, 0, 0))
                self.frameSurface.blit(text, (100,100))
                break
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                    self.calibration=True

            # We have a color frame. Fill out back buffer surface with frame's data 
            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.drawColorFrame(frame, self.frameSurface)
                frame = None

            # We have a body frame, so can get skeletons
            if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        
                        joints = body.joints 
                        if (joints[PyKinectV2.JointType_HandLeft].Position.y > joints[PyKinectV2.JointType_Head].Position.y and 
                            joints[PyKinectV2.JointType_HandRight].Position.y > joints[PyKinectV2.JointType_Head].Position.y):                
                            self.originalSpineBaseX=int((joints[PyKinectV2.JointType_SpineBase].Position.x+1)*self.screenWidth/2)
                            self.originalHipLeft=int((joints[PyKinectV2.JointType_HipLeft].Position.x+1)*self.screenWidth/2)
                            self.originalHipRight=int((joints[PyKinectV2.JointType_HipRight].Position.x+1)*self.screenWidth/2)
                            self.originalHipY=int((((1-joints[PyKinectV2.JointType_HipLeft].Position.y)*self.screenHeight/2 + (1-joints[PyKinectV2.JointType_HipRight].Position.y)*self.screenHeight/2))/2)
                            self.calibration=True

                 # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
                # --- (screen size may be different from Kinect's color frame size) 
                hToW = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
                targetHeight = int(hToW * self.screen.get_width())
                surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), targetHeight));
                self.screen.blit(surfaceToDraw, (0,0))
                surfaceToDraw = None
                pygame.display.update()

                # --- Limit to 60 frames per second
                self.clock.tick(60)

        if(self.done==True):
            self.kinect.close()
            pygame.quit()

    def run(self):
        # -------- Main Program Loop -----------
        while not self.done:
            # --- Main event loop
            if self.gameover:
                font = pygame.font.Font(None, 36)
                text = font.render("Game over!", 1, (0, 0, 0))
                self.frameSurface.blit(text, (100,100))
                break
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop

            # We have a color frame. Fill out back buffer surface with frame's data 
            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.drawColorFrame(frame, self.frameSurface)
                frame = None

            # We have a body frame, so can get skeletons
            if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        joints = body.joints 

                        # save the hand positions
                        if joints[PyKinectV2.JointType_SpineBase].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curSpineBaseX = joints[PyKinectV2.JointType_SpineBase].Position.x
                            self.curSpineBaseY = joints[PyKinectV2.JointType_SpineBase].Position.y
                            if(self.originalSpineBaseY==None):
                                self.originalSpineBaseY=(1-self.curSpineBaseY)*self.screenHeight/2
                            self.reset()
                        self.differenceSpineBaseX=self.curSpineBaseX-self.prevSpineBaseX
                        self.differenceSpineBaseY=self.curSpineBaseY-self.prevSpineBaseY

                        if((1-self.differenceSpineBaseY)*self.screenHeight/2<1):
                            self.samePositionCounter+=1
                            if(self.samePositionCounter>=self.samePositionAmount):
                                self.reset=True
                        else:
                            self.samePositionCounter=0

                        # cycle previous and current heights for next time
                        self.prevSpineBaseX = self.curSpineBaseX
                        self.prevSpineBaseY = self.curSpineBaseY
                        
            self.changeDirection()

            # Optional debugging text
            #font = pygame.font.Font(None, 36)
            #text = font.render(str(self.flap), 1, (0, 0, 0))
            #self.frameSurface.blit(text, (100,100))

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            hToW = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
            targetHeight = int(hToW * self.screen.get_width())
            surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), targetHeight));
            self.screen.blit(surfaceToDraw, (0,0))
            surfaceToDraw = None
            pygame.display.update()

            # --- Limit to 60 frames per second
            self.clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self.kinect.close()
        pygame.quit()

# game = GameRuntime();
# game.calibrate()
# game.run();