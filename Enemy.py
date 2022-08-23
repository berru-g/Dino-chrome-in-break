import pygame
import random

vec = pygame.math.Vector2


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/CLOUD.png")
        self.rect = self.image.get_rect()
        

        self.pos = vec(random.randint(0, 800), 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.FRIC = -0.1
        self.ACC = round(random.uniform(0.1, 0.2), 2)

        self.direction = random.randint(0, 1) # 0 -> Means Right | 1 -> Means Left


    def move(self):
        self.acc = vec(0, 0.5)

        if self.direction == 0:
            self.acc.x = self.ACC
        elif self.direction == 1:
            self.acc.x = -self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > 780:
            self.direction = 1
        elif self.pos.x < 0:
            self.direction = 0

        self.rect.topleft = self.pos


    def collision(self, group):
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]

                if self.rect.bottom >= lowest.rect.top:
                    self.pos.y = lowest.rect.top - self.rect.height
                    self.rect.y = lowest.rect.top - self.rect.height 
                    self.vel.y = 0

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            # Hit the Player 
            player.player_hit(1)
        elif self.rect.colliderect(player.attack_range):
            # Hit by the Player
            self.kill()


    def update(self, group, player):
        self.move()
        self.collision(group)
        self.player_collision(player)
                    

    def render(self, display):
        display.blit(self.image, self.pos)
        #pygame.draw.rect(display, (0, 0, 255), self.rect)


        
        
