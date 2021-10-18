import pygame
import random
import math
from pygame import mixer

# Initialise the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))  # (width,height)

# Background
background = pygame.image.load("Background.png")

#Background Song

mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
iconUfo = pygame.image.load("Icon.png")
pygame.display.set_icon(iconUfo)

# Player
playerImg = pygame.image.load("Player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(10)

# Bullet
# Ready state - You can't see the bullet on the screen.
# Fire - The bullet is currently moving.
bulletImg = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Scoreboard

score_value = 0

font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf',70)

def show_score(x,y):
    score = font.render("Score : "+ str(score_value),True, (255,255,255))
    screen.blit(score,(x, y))

def game_over_text():
    Game_Over = over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(Game_Over,(200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    # RGB - Red, Green and Blue.... These values can range from 0-255
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Movement iteration
        if event.type == pygame.KEYDOWN:
            print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            print("A keystroke is released")
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds.
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movements
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 672:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        
        # Collision detection

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 672)
            enemyY[i] = random.randint(50, 200)
        
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()