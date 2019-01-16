#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math
import random

class Crossin(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        #Set the bot color in RGB
        self.setColor(250, 250, 20)
        self.setGunColor(0, 0, 0)
        self.setRadarColor(200, 100, 0)
        self.setBulletsColor(100, 150, 250)
        
        self.radarVisible(True) # if True the radar field is visible
        
        #get the map size
        size = self.getMapSize()
        self.mapWidth = size.width()
        self.mapHeight = size.height()
        
        self.lockRadar("gun")
        self.setRadarField("thin")
            
    def run(self): #main loop to command the bot
        targetX = random.randint(150, self.mapWidth - 150)
        targetY = random.randint(150, self.mapHeight - 150)
        pos = self.getPosition()
        targetAg = 180 + math.degrees(math.atan2(targetX - pos.x(), pos.y() - targetY))
        deltaAg = (targetAg - self.getHeading()) % 360
        if deltaAg > 180:
            deltaAg -= 360
        self.turn(deltaAg)
        self.move(100)
        self.gunTurn(90)

    def onHitWall(self):
        self.stop()
        self.turn(90)
        self.move(-100)

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        pass

    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        pass
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        pass
        
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        self.fire(9)
        self.gunTurn(3)
        self.fire(6)
        self.gunTurn(3)
        self.fire(3)
        self.gunTurn(6)
