import pygame
import random
import math
from pygame import mixer

pygame.init()

# ----------------Create a screen-------------
screen = pygame.display.set_mode((800, 600))
running = True

# ----------------Create a surface for the blur effect-------------
surface = pygame.Surface((800, 600), pygame.SRCALPHA)  # Surface with alpha transparency

# ------------------Title and Icon--------------
pygame.display.set_caption("FEC Blasters")
icon = pygame.image.load("school.png")
pygame.display.set_icon(icon)

# -------------Background-----------
background = pygame.image.load("d32real.jpeg")

#---------- FPS ---------

clock = pygame.time.Clock()

FPS = 60

# ------------ BG music----------------
mixer.music.load("mujibdj.mp3")
mixer.music.play(-1)

#-------------Game Pause---------- -
game_pause = False

#---------------display menu---------
def game_pause_func():
    global game_pause

    game_pause = True

    while game_pause:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:   
                    game_pause = False  # Unpause the game


            if event.type == pygame.QUIT:
                game_pause = False
                global running
                running = False


# ------------------Player---------------
playerImg = pygame.image.load("dalim.png")
playerX = 370 
playerY = 480
playerX_change = 0
playerY_change = 0

# ------------------Multiple Enemy---------------
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("Mujib.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# ------------------Laser------------------
laserImg = pygame.image.load("mujib_bullet.png")
laserX = 0
laserY = 480
laserY_change = 5

# List to store lasers
lasers = []

# ----------------Score------------
score_value = 0
font = pygame.font.Font("font.ttf", 40)

textX = 10
textY = 10

endX = 275
endY = 350

# ----------------Game Over------------
Go_font = pygame.font.Font("font.ttf", 84)

# ---------------Definitions----------

def draw_pause():
    surface.fill((158, 158, 158, 180))  # Fill the surface with a semi-transparent color
    screen.blit(surface, (0, 0))  # Draw the surface on the screen
    pause_text = font.render("Game is Paused", True, (0, 255, 255))  # Text for the pause screen
    screen.blit(pause_text, (250, 250))  # Display the "Game Paused" text at the center

def Game_Over():
    GO_Text = Go_font.render("GAME OVER", True, (0, 255, 255))
    screen.blit(GO_Text, (255, 250))

def Max_Score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def laser(x, y):
    screen.blit(laserImg, (x, y))

def fire_laser(x, y):
    lasers.append([x + 16, y + 10])

def iscollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False

def player_collision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance < 30: 
        return True
    else:
        return False

# ------------Game continues -------------------
while running:

    #-------- fps --------

    clock.tick(FPS)

    # -------Background : Color and RGB-----------
    screen.fill((0, 0, 0))

    # ---------Background image----------
    screen.blit(background, (0, 0))

    if game_pause == True:

        pass  # Draw the pause screen with blur effect and text

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ------------- for keypad --------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    game_pause_func()

                if event.key == pygame.K_LEFT:
                    playerX_change = -5

                if event.key == pygame.K_RIGHT:
                    playerX_change = 5

                if event.key == pygame.K_UP:
                    playerY_change = -5

                if event.key == pygame.K_DOWN:
                    playerY_change = 5

                if event.key == pygame.K_SPACE:
                    if len(lasers) < 5:
                        laser_sound = mixer.Sound("laser1.mp3")
                        laser_sound.play()
                        laserX = playerX
                        laserY = playerY
                        fire_laser(laserX, laserY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        # -------------Player object Moving--------------
        playerX += playerX_change
        playerY += playerY_change

        # ----------Boundary-------------
        if playerX <= 0:
            playerX = 0
        elif playerX >= 746:
            playerX = 746
        if playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536

        # -------------Enemy object Moving--------------
        for i in range(num_of_enemy):
            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 746:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            #--------------player-enemy collision-------------
            if player_collision(playerX, playerY, enemyX[i], enemyY[i]):
                Game_Over()
                Max_Score(endX , endY)
                pygame.display.update()
                pygame.time.delay(3000) 
                running = False 

            enemy(enemyX[i], enemyY[i], i) 


        # -------------Laser Movement--------------
        for laser_pos in lasers[:]:
            laser_pos[1] -= laserY_change 

            if laser_pos[1] <= 0:  
                lasers.remove(laser_pos)

            laser(laser_pos[0], laser_pos[1])

            # ------------- Collision check for each laser-------------
            for i in range(num_of_enemy):
                collision = iscollision(enemyX[i], enemyY[i], laser_pos[0], laser_pos[1])
                if collision:
                    collision_sound = mixer.Sound("explosion.mp3")
                    collision_sound.play()
                    score_value += 1
                    lasers.remove(laser_pos)

                    enemyX[i] = random.randint(0, 800)
                    enemyY[i] = random.randint(50, 150)
                    print(f"Score: {score_value}")

        # ----------------Update the game screen--------------
        player(playerX, playerY)
        Max_Score(textX, textY)

    pygame.display.update()

