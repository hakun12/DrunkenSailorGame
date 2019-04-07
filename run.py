import pygame
import objects
from random import randint

#INITIAL SETUP
pygame.init()
Resolution = (1280,720)
GameWindow = pygame.display.set_mode(Resolution)
pygame.display.set_caption("Drunken Sailor")
mainClock = pygame.time.Clock()
font = pygame.font.SysFont('arial',18)
hiddenscore = 0
score = 0

def CollisionDetect(hitbox1, hitbox2):
    cp1 = hitbox2.collisionPoints[0]
    cp2 = hitbox2.collisionPoints[1]
    cp3 = hitbox2.collisionPoints[2]
    cp4 = hitbox2.collisionPoints[3]
    cp5 = hitbox2.collisionPoints[4]
    cp6 = hitbox2.collisionPoints[5]
    cp7 = hitbox2.collisionPoints[6]
    cp8 = hitbox2.collisionPoints[7]
    for cp in hitbox1.collisionPoints:
        if cp[0] > cp7[0] and cp[0] < cp3[0] and cp[1] < cp5[1] and cp[1] > cp1[1]:
            if cp[0] > cp6[0] and cp[0] < cp2[0] and cp[1] > cp6[1] and cp[1] < cp2[1]:
                return True
            elif cp[0] > cp8[0] and cp[0] < cp4[0] and cp[1] > cp8[1] and cp[0] < cp4[1]:
                return True

def CheckCollision2(entity1, entity2):
    if entity1.x <= entity2.x + 150:
        return True

#SPRITES
bg = pygame.image.load('images/testbg.jpg')
kraken = pygame.image.load('images/monster.png')
chest = pygame.image.load('images/chest.png')
player = objects.Player(75,360,155,155)
#spawn_tracks = [50,205,360,515]
spawn_tracks = [objects.SpawnTrack(50),
                objects.SpawnTrack(205),
                objects.SpawnTrack(360),
                objects.SpawnTrack(515)]
last_spawn_track = 0
monsters = []
treasures = []
for i in range(5):
    track = randint(0,3)
    monsters.append(objects.Obstacle(Resolution[0] + 200, spawn_tracks[track], 155, 155, spawn_tracks[track].speed, kraken, track))
    spawn_tracks[track].add(monsters[i])
    i += 1

for i in range(3):
    track = randint(0,3)
    treasures.append(objects.Obstacle(Resolution[0] + 1000, spawn_tracks[track], 155, 155, spawn_tracks[track].speed, chest, track))
    spawn_tracks[track].add(treasures[i])
    i += 1

run = True
while run:
    #HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and player.moveDirection != 1:
                if player.moveDirectionPrevious == 2:
                    player.moveDirectionPrevious = player.moveDirection
                player.moveDirection = 1
                player.hook = False
            elif event.key == pygame.K_s and player.moveDirection != 2:
                if player.moveDirectionPrevious == 1:
                    player.moveDirectionPrevious = player.moveDirection
                player.moveDirection = 2
                player.hook = False
            elif event.key == pygame.K_SPACE:
                player.hook = True
    if player.hook == True:
        player.isMoving = False
    else:
        if player.moveDirectionPrevious != 0 and player.moveDirectionPrevious != player.moveDirection:
            if player.vel > 0:
                player.isMoving = False
            else:
                player.isMoving = True
                player.moveDirectionPrevious = 0
        elif player.moveDirectionPrevious == 0 and player.moveDirectionPrevious != player.moveDirection:
            player.moveDirectionPrevious = player.moveDirection
            player.isMoving = True
        elif player.moveDirectionPrevious != 0 and player.moveDirection == player.moveDirectionPrevious:
            player.isMoving = True

    #print(f"X: {player.x} Y: {player.y} hook: {player.hook} | previous: {player.moveDirectionPrevious} | current: {player.moveDirection}")

    #BOUNDARIES
    if player.y < 25:
        player.vel = 0
        player.y = 25
    elif player.y > Resolution[1] - 150 - player.vel:
        player.vel = 0
        player.y = Resolution[1] - 150

    #HANDLE MOVEMENT
    if player.isMoving == True:
        if player.vel <= 5.2:
            player.vel += player.moveBase * player.moveDelay
        if player.moveDirection == 1:
            player.y -= player.vel
        else:
            player.y += player.vel
    else:
        if player.vel > 0:
            player.vel -= player.moveBase * player.moveDelay
            if player.moveDirectionPrevious == 1:
                player.y -= player.vel
            elif player.moveDirectionPrevious == 2:
                player.y += player.vel
            else:
                if player.moveDirection == 1:
                    player.y -= player.vel
                elif player.moveDirection == 2:
                    player.y += player.vel
        elif player.vel <= 0:
            player.vel = 0

    hiddenscore += 1
    if hiddenscore % 100 == 0:
        hiddenscore = 0
        score += 1
    #GameWindow.fill((0,0,0))
    scoreDisplay = font.render(f"Score: {score}", 1, (255, 255, 255))
    GameWindow.blit(bg,(0,0))
    GameWindow.blit(scoreDisplay,(40, 15))
    #pygame.draw.rect(GameWindow,(125,63,255),(150,150,200,200))
    for monster in monsters:
        previoustrack = monster.track
        track = randint(0,3)
        monster.x -= monster.speed
        if (monster.x < -100):
            monster.x = Resolution[0] + 150
            if previoustrack != track:
                monster.y = spawn_tracks[track].startY
                spawn_tracks[previoustrack].delete(monster)
                spawn_tracks[track].add(monster)
                monster.track = track
                monster.speed = spawn_tracks[track].speed
                for e in spawn_tracks[track].entities:
                    if CheckCollision2(monster, e) and e is not monster:
                        monster.x += 150
                for e in spawn_tracks[track].entities:
                    if CheckCollision2(monster, e) and e is not monster:
                        monster.x += 150
            else:
                monster.y = spawn_tracks[track].startY
                monster.speed = spawn_tracks[track].speed
        monster.draw(GameWindow)
        if CollisionDetect(player.hitbox, monster.hitbox):
            score = 0
    for t in treasures:
        previoustrack = t.track
        track = randint(0,3)
        t.x -= t.speed
        if (t.x < -100):
            t.x = Resolution[0] + randint(150,2400)
            if previoustrack != track:
                t.y = spawn_tracks[track].startY
                spawn_tracks[previoustrack].delete(t)
                spawn_tracks[track].add(t)
                t.track = track
                t.speed = spawn_tracks[track].speed
                for e in spawn_tracks[track].entities:
                    if CheckCollision2(t, e) and e is not t:
                        t.x += 1000
                for e in spawn_tracks[track].entities:
                    if CheckCollision2(t, e) and e is not t:
                        t.x += 1500
            else:
                t.y = spawn_tracks[track].startY
                t.speed = spawn_tracks[track].speed
        t.draw(GameWindow)
        if CollisionDetect(player.hitbox, t.hitbox) == True:
            score += 10
            t.x = -99
    for t in spawn_tracks:
        if len(t.entities) == 0:
            t.speed = randint(2,5)

    player.draw(GameWindow)
    pygame.display.update()
    mainClock.tick(60)

pygame.quit()
