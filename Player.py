import pygame
from pygame.locals import *
from HealthBar import HealthBar

vec = pygame.math.Vector2



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Images/Player_Sprite_R.png")
        self.rect = pygame.Rect(x, y, 10, -16)

        # Player Info
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.healthbar = HealthBar(10, 10)

        # Player Constants
        self.ACC = 0.4
        self.FRIC = -0.1

        # Player Movements
        self.jumping = False
        self.running = False
        self.sleep =False 
        self.direction = "RIGHT"
        self.move_frame = 0

        # Player Attacking
        self.attacking = False
        self.attack_frame = 0
        self.attack_counter = 0
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.hit_cooldown = False

        # Player Events
        self.hit_cooldown_event = pygame.USEREVENT + 1

        
    def move(self):
        self.acc = vec(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.acc.x = -self.ACC
        if keys[K_RIGHT]:
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > 800:
            self.pos.x = -40
        elif self.pos.x < -40:
            self.pos.x = 800

        self.rect.topleft = self.pos
        self.rect.x += 32


    def walking(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return

        if self.jumping == False and self.running == True:
            if self.vel.x >= 0:
                self.image = self.animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = self.animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if self.running == False and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.animation_right[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.animation_left[self.move_frame]

    def attack(self):
        if self.attacking == True:
            if self.direction == "RIGHT":
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width,self.pos.y, 30, self.rect.height)
            elif self.direction == "LEFT":
                self.attack_range = pygame.Rect(self.pos.x, self.pos.y, 30, self.rect.height)
            
            if self.attack_frame > 38:
                self.attack_frame = 0
                self.attacking = False
                self.attack_range = pygame.Rect(0, 0, 0, 0)
                return

            if self.direction == "RIGHT":
                self.image = self.attack_animation_right[self.attack_frame]
            elif self.direction == "LEFT":
                self.image = self.attack_animation_left[self.attack_frame]

            self.attack_counter += 1
            if self.attack_counter >= 3:
                self.attack_frame += 1
                self.attack_counter = 0
        

    def update(self, group):
        self.walking()
        self.move()
        self.attack()
        self.collision(group)

    def player_hit(self, damage):
        if self.hit_cooldown == False:
            self.hit_cooldown = True
            self.healthbar.takeDamage(damage)
            pygame.time.set_timer(self.hit_cooldown_event, 1000)
            
        
        

    def collision(self, group):
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]

                if self.rect.bottom >= lowest.rect.top:
                    self.pos.y = lowest.rect.top - self.rect.height
                    self.rect.y = lowest.rect.top - self.rect.height 
                    self.vel.y = 0
                    self.jumping = False
                    
    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12
        
    def render(self, display):
        #pygame.draw.rect(display, (255, 0, 0), self.rect)
        #pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.pos)
        self.healthbar.render(display)

    def load_animations(self):
        self.animation_right = [pygame.image.load("Images/Player_Sprite_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite2_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite3_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite4_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite5_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite6_R.png").convert_alpha(),
                   pygame.image.load("Images/Player_Sprite_R.png").convert_alpha()]

        self.animation_left = [pygame.image.load("Images/Player_Sprite_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite2_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite3_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite4_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite5_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite6_L.png").convert_alpha(),
                          pygame.image.load("Images/Player_Sprite_L.png").convert_alpha()]


############################################obrdle###bordel*******************************************************
        self.attack_animation_right = [pygame.image.load("Images/Player_Sprite_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack1_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack1_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack2_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack2_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack3_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack3_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack3_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack3_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_R.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack5bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_R.png").convert_alpha(),                                  
                                  pygame.image.load("Images/Player_Attack5cis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack6_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack6_R.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack_R.png").convert_alpha()]

        self.attack_animation_left = [pygame.image.load("Images/Player_Sprite_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack1_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack1_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack2_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack2_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack3_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack3_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack3_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack3_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack4bis_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5_L.png").convert_alpha(),
                                  pygame.image.load("Images/Player_Attack5bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5bis_L.png").convert_alpha(),                                  
                                  pygame.image.load("Images/Player_Attack5cis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack5cis_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack6_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack6_L.png").convert_alpha(),
                                  pygame.image.load("Images\Player_Attack_L.png").convert_alpha()]