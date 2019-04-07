import pygame
from random import randint
from math import sqrt

cos45 = sqrt(2)/2
sin45 = cos45

class Hitbox(object):
    def __init__(self,radius, x,y):
        self.radius = radius
        self.x = x
        self.y = y
        self.getCollisionPoints()

    def getCollisionPoints(self):
        self.collisionPoints = [
            (self.x, self.y - self.radius),
            (int(self.x + cos45 * self.radius), int(self.y + sin45 * self.radius)),
            (self.x + self.radius, self.y),
            (int(self.x + cos45 * self.radius), int(self.y - sin45 * self.radius)),
            (self.x, self.y + self.radius),
            (int(self.x - cos45 * self.radius), int(self.y - sin45 * self.radius)),
            (self.x - self.radius, self.y),
            (int(self.x - cos45 * self.radius), int(self.y + sin45 * self.radius))
        ]

    def drawCollisionPoints(self,window):
        self.getCollisionPoints()
        for cp in self.collisionPoints:
            pygame.draw.circle(window, (0, 0, 255), cp, 2, 2)

    def draw(self, window):
        pygame.draw.circle(window, (255, 0, 0), (self.x,self.y), 50, 2)
        self.drawCollisionPoints(window)

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.updateHitbox()

    vel = 0
    moveBase = 2
    moveDelay = 0.05
    moveDirection = 0
    moveDirectionPrevious = 0
    isMoving = False
    hook = False
    sprite = pygame.image.load('images/ship.png')

    def updateHitbox(self):
        self.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
        self.hitbox = Hitbox(50, self.center[0], self.center[1])

    def draw(self,window):
        window.blit(self.sprite, (self.x, self.y))
        self.updateHitbox()
        self.hitbox.draw(window)

class SpawnTrack(object):
    def __init__(self, startY):
        self.startY = startY
        self.entities = []
        self.speed = randint(2,5)

    def add(self,entity):
        if entity not in self.entities:
            self.entities.append(entity)
    def delete(self,entity):
        if entity in self.entities:
            self.entities.remove(entity)

class Obstacle(object):
    def __init__(self, x, Track, width, height, speed, sprite, track):
        self.x = x
        self.y = Track.startY
        self.width = width
        self.height = height
        self.speed = speed
        self.sprite = sprite
        self.updateHitbox()
        self.track = track
        Track.add(self)


    def updateHitbox(self):
        self.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
        self.hitbox = Hitbox(50, self.center[0], self.center[1])

    def draw(self,window):
        window.blit(self.sprite,(self.x, self.y))
        self.updateHitbox()
        self.hitbox.draw(window)