#ORIGIN by https://coderslegacy.com/pygame-rpg-game-code-download/
# pimpé par github.com/berru-g
#DINO CHROME BREAK
#MAIS QUE FAIT LE DINO QUAND INTERNET FONCTIONNE ?
#WHAT DOES THE DINO DO WHEN THE INTERNET IS WORKING?

import pygame
from pygame.locals import *
import sys


from Ground import Ground
from Player import Player
from Enemy import Enemy
from UserInterface import UserInterface


# Begin Pygame
pygame.init()


WIDTH = 800
HEIGHT = 400
FPS = 60
CLOCK = pygame.time.Clock()


display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Chrome break")
#icon=pygame.image.load('icon.png')
#pygame.display.set_icon(icon)

background = pygame.image.load("Images/Background.png")
#H W G H
ground = Ground(901, 260, 0, 250, "Images/Ground.png")
player = Player(20, 200)
player.load_animations()
E1 = Enemy()
UI = UserInterface()

ground2 = Ground(100, 30, 300, 200, "Images/CLOUD.png")
ground3 = Ground(120, 30, 100, 150, "Images/CLOUD.png")
ground4 = Ground(80, 30, 500, 100, "Images/CLOUD.png")


EnemyGroup = pygame.sprite.Group()
EnemyGroup.add(E1)

GroundGroup = pygame.sprite.Group()
GroundGroup.add(ground)
GroundGroup.add(ground2)
GroundGroup.add(ground3)
GroundGroup.add(ground4)


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == player.hit_cooldown_event:
            player.hit_cooldown = False
            pygame.time.set_timer(player.hit_cooldown_event, 0)


        if event.type == MOUSEBUTTONDOWN:
            pass

        if event.type == KEYDOWN:
#            player.sleep()
            if event.key == K_UP:
                player.jump()
            if event.key == K_SPACE:
                player.attacking = True
                player.attack()


    # Update Functions
    for enemy in EnemyGroup:
        enemy.update(GroundGroup, player)
        
    player.update(GroundGroup)
    UI.update(CLOCK.get_fps())


    # Render Functions
    display.blit(background, (0, 0))
    player.render(display)
    UI.render(display)

    for enemy in EnemyGroup:
        enemy.render(display)

    for grounds in GroundGroup:
        grounds.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)
            











    
    
