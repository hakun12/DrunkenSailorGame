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
scoreMpx = 1

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

#SPRITES
bg = pygame.image.load('images/testbg.jpg')
kraken = pygame.image.load('images/monster.png')
chest = pygame.image.load('images/chest.png')
rum_bottle = pygame.image.load('images/rum.png')
player = objects.Player(75,360,155,155)
spawn_tracks = [objects.SpawnTrack(50),
                objects.SpawnTrack(205),
                objects.SpawnTrack(360),
                objects.SpawnTrack(515)]

monsters = []
treasures = []
bottles = []
for i in range(0,5):
    monsters.append(objects.Entity(kraken, 0, 50))
    spawn_tracks[randint(0,3)].sockets[randint(0,7)].attachEntity(monsters[i])

for i in range(0,3):
    treasures.append(objects.Entity(chest, randint(10,500), 75))
    spawn_tracks[randint(0, 3)].sockets[randint(0, 7)].attachEntity(treasures[i])

for i in range(0,2):
    bottles.append(objects.Entity(rum_bottle, randint(1000,2500), 60))
    spawn_tracks[randint(0, 3)].sockets[randint(0, 7)].attachEntity(bottles[i])

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

    #Count score
    hiddenscore += 1*scoreMpx
    print(hiddenscore)
    if hiddenscore > 100:
        hiddenscore = 0
        score += 1
    scoreDisplay = font.render(f"Score: {score} || Score multiplier: {scoreMpx}", 1, (255, 255, 255))

    GameWindow.blit(bg,(0,0))
    #Display and move all sockets within spawn tracks
    for st in spawn_tracks:
        st.draw(GameWindow)

    #Check for unattached monster, then try to attach it to random socket
    #also
    #Check for attached monster and check if it's colliding with player
    for monster in monsters:
        if not monster.attached:
            spawn_tracks[randint(0,3)].sockets[randint(0,7)].attachEntity(monster)
        if monster.attached and CollisionDetect(player.hitbox, monster.socket.hitbox):
            score = 0

    for treasure in treasures:
        if treasure.cooldown > 0:
            treasure.cooldown -= 1
        if not treasure.attached:
            spawn_tracks[randint(0,3)].sockets[randint(0,7)].attachEntity(treasure)
        if treasure.attached and CollisionDetect(player.hitbox, treasure.socket.hitbox):
            treasure.cooldown = randint(500,4000)
            treasure.socket.detachEntity()
            score += 5

    for bottle in bottles:
        if bottle.cooldown > 0:
            bottle.cooldown -= 1
        if not bottle.attached:
            spawn_tracks[randint(0,3)].sockets[randint(0,7)].attachEntity(bottle)
        if bottle.attached and CollisionDetect(player.hitbox, bottle.socket.hitbox):
            bottle.cooldown = randint(500,4000)
            bottle.socket.detachEntity()
            if scoreMpx == 1:
                scoreMpx = 2
            elif scoreMpx == 2:
                scoreMpx = 5
            elif scoreMpx == 5:
                scoreMpx = 10
            else:
                scoreMpx += 1
            player.moveDelay *= 0.75

    #Display score and player
    GameWindow.blit(scoreDisplay,(40, 15))
    player.draw(GameWindow)
    pygame.display.update()
    mainClock.tick(60)

pygame.quit()
