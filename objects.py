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

class Entity(object):
    def __init__(self, sprite, cooldown, radius):
        self.sprite = sprite
        self.attached = False
        self.socket = None
        self.cooldown = cooldown
        self.hitboxRadius = radius

class Socket(object):
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.height = 155
        self.width = 155
        self.aligned = False
        self.updateHitbox()
        self.entity = None
        self.cooldown = 0

    def attachEntity(self, entity):
        if self.aligned == False and self.x > 1280 and self.cooldown <= 0 and entity.cooldown <= 0:
            self.aligned = True
            entity.attached = True
            self.entity = entity
            self.entity.socket = self

    def detachEntity(self):
        self.aligned = False
        self.entity.attached = False
        self.entity.socket = None
        self.entity = None
        self.cooldown = randint(10,60)

    def updateHitbox(self):
        if self.aligned:
            self.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
            self.hitbox = Hitbox(self.entity.hitboxRadius, self.center[0], self.center[1])
        else:
            self.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
            self.hitbox = Hitbox(50, self.center[0], self.center[1])

    def draw(self, window):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.aligned:
            window.blit(self.entity.sprite, (self.x, self.y))
            self.updateHitbox()
            self.hitbox.draw(window)

class SpawnTrack(object):
    def __init__(self, startY):
        self.startY = startY
        self.entities = []
        self.speed = randint(2,5)
        self.start = 1300
        self.sockets = []
        for i in range(0,8):
            self.sockets.append(Socket(self.start,self.startY))
            self.start += 175

    def draw(self, window):
        for socket in self.sockets:
            socket.x -= self.speed
            if socket.x < -100:
                if socket.aligned:
                    socket.detachEntity()
                socket.x = 1300
            socket.draw(window)

