# Start of the program
import pygame
from pygame import mixer
import random
import math

# Intialize The Game
pygame.init()

# Create The Screen
screen = pygame.display.set_mode((800, 600))

# Background image setting
background = icon = pygame.image.load('background.png')

# bckground sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption And Title of the game
pygame.display.set_caption("Udta Patola")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player icon
plimg = pygame.image.load("player.png")
plx = 370
ply = 480
plychange = 0

# enemy icon
enimg = []
enx = []
eny = []
enchangeX = []
encchangeY = []

numofenemies = 6

for i in range(numofenemies):
    enimg.append(pygame.image.load("enemy.png"))
    enx.append(random.randint(0, 735))
    eny.append(random.randint(50, 150))
    enchangeX.append(2)
    encchangeY.append(40)

# Bullet Icon
bimg = pygame.image.load("bullet.png")
bx = 0
by = 480
bchangeX = 0
bchangeY = 10

# you cant see the bullet on the screem
bstate = "ready"

# Fire - The bullet is currently moving

# score value
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textx = 10
texty = 10

# gameover
gameoveerr = pygame.font.Font("freesansbold.ttf", 64)


def game():
    over = gameoveerr.render("GAME OVER  :", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def showscore(x, y):
    fontt = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(fontt, (x, y))


def player(x, y):
    screen.blit(plimg, (x, y))


def enemy(x, y, i):
    screen.blit(enimg[i], (x, y))


def fire_bullet(x, y):
    global bstate
    bstate = "fire"
    screen.blit(bimg, (x + 16, y + 10))


def isCollision(enx, eny, bx, by):
    distance = math.sqrt(math.pow(enx - by, 2) + (math.pow(eny - by, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # rgb color
    screen.fill((20, 150, 70))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # if any keystroke is pressed example for right and left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plychange = -10
            if event.key == pygame.K_RIGHT:
                plychange = 10
            if event.key == pygame.K_SPACE:
                if bstate == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bx = plx
                    fire_bullet(bx, by)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                plychange = 0

    # Here we are checking the boundaries of the characters so they cannot go outside of the boundaries
    plx += plychange

    if plx <= 2:
        plx = 2
    elif plx >= 734:
        plx = 734

    # Enemy movement
    for i in range(numofenemies):
        # Game over
        if eny[i] > 440:
            for j in range(numofenemies):
                eny[j] = 2000
            game()
            break

        enx[i] += enchangeX[i]
        if enx[i] <= 2:
            enchangeX[i] = 2
            eny[i] += encchangeY[i]
        elif enx[i] >= 734:
            enchangeX[i] = -2
            eny[i] += encchangeY[i]

        # Collision
        collision = isCollision(enx[i], eny[i], bx, by)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            by = 480
            bstate = "ready"
            score += 1
            enx[i] = random.randint(0, 735)
            eny[i] = random.randint(50, 150)

        enemy(enx[i], eny[i], i)

    # bullet movement
    if by <= 0:
        by = 480
        bstate = "ready"

    if bstate is "fire":
        fire_bullet(bx, by)
        by -= bchangeY

    player(plx, ply)
    showscore(textx, texty)
    pygame.display.update()
# END OF THE PROGRAM
