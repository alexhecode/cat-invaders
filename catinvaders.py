# Importing math and random modules
import math
import random

# Importing and initialising the pygame library
import pygame
pygame.init()

# Import sound mixer from pygame library
from pygame import mixer

# Set up the drawing window
screen = pygame.display.set_mode((800, 600))

# Set up the background
background = pygame.image.load('background.jpg')

# Load background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Customise window title and icon
pygame.display.set_caption("Commander Doge and the Cat Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Set player image and location
playerImg = pygame.image.load('doge.png')
playerX = 370
playerY = 480
playerX_change = 0

# Set enemy image and location
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('cat.gif'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Projectile
# Projectile states:
# Ready - Ball is not on screen however is ready to be fired
# Fire - The ball is moving
bulletImg = pygame.image.load('ball.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "Ready"

# Create scoreboard
score_value = 0
font = pygame.font.Font('GOODDP__.ttf', 32)

textX = 10
textY = 10

# Create "Game Over" text
over_font = pygame.font.Font('GOODDP__.ttf', 64)

# Define scoreboard
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Define "Game Over" text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Define Player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Define Enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Define Projectile
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Definte Collisions
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Run until the user asks to quit
running = True
while running:

    # Fill the screen with RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    
    # Background Image
    screen.blit(background, (0, 0))
    
    # Did the user click the windows close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is activated check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
        
        # Call fire_bullet function when space key is pressed and play sound effects
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bulletSound = mixer.Sound("yeet.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Check if keystroke has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Allows player to move along x axis
    playerX += playerX_change
    
    # Introduce boundaries for the player - takes player.png image size into account
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Set "Game Over" conditions
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            
            # Set "Game over" sound effect
            gameoverSound = mixer.Sound("gameover.wav")
            gameoverSound.play()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Set collisions for when projectiles hit enemy
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound("meow.wav")
            collisionSound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Place player image and score on screen
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
