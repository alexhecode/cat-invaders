# Import random module
import random

# Importing and initialising the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((800,600))

# Set up background
background = pygame.image.load("background.jpg")

# Customise window title and icon
pygame.display.set_caption("Commander Doge and the Cat Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("doge.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load("cat.gif")
enemyX = random.randint(0,800)
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# Projectile
# Ready - Ball is not on screen however is ready to be fired
# Fire - The ball is moving

bulletImg = pygame.image.load('ball.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "Ready"

# Define player
def player(x,y):
    screen.blit(playerImg, (x, y))
    
# Defnite enemy
def enemy(x,y):
    screen.blit(enemyImg, (x, y))

# Define projectile
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Run until the user asks to quit
running = True
while running:
    
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
            # Call fire_bullet function when space key is pressed
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
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
    
    # Allows enemy to move along x axis
    enemyX += enemyX_change

    # Introduce boundaries for enemy
    if enemyX <= 0:
        enemyX_change = 4
        # Allows enemy to move along y axis by 40px when it hits the boundary
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        # Allows enemy to move along y axis by 40px when it hits the boundary
        enemyY += enemyY_change
        
    # Projectile Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # Fill the screen with RGB - Red, Green, Blue
    screen.fill((0,0,0))
    
    # Background Image
    screen.blit(background, (0, 0))
    
    # Place player image and enemy on screen    
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
