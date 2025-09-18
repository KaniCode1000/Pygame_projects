# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 10:19:29 2021

@author: Kanishk
"""
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney
# Boss art from Wisedawn
import pygame
from math import atan2
import random
import codecs
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
new_wave = False
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
Speed_ship_count = 50
speedshipblitted = 0
forward_drive_online = False
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
bosscolour = (94,63,107)
LIGHTSKYBLUE = (135,206,250)
DODGERBLUE = (30,144,255)
POWDERBLUE = (176,224,230)
ORANGE = (255,140,0)
GOLD = (255,215,0)
LEMON_CHIFFON = (255,250,205)
# Lasers
RED_LASER = pygame.image.load(path.join(img_dir, "laserred.png"))
GREEN_LASER = pygame.image.load(path.join(img_dir,"lasergreen.png"))
BLUE_LASER = pygame.image.load(path.join(img_dir,"laserblue.png"))
BLACK_LASER = pygame.image.load(path.join(img_dir,"laserblack.png"))
#Enemy ships
RED_SHIP = pygame.image.load(path.join(img_dir, "enemyRed.png"))
GREEN_SHIP = pygame.image.load(path.join(img_dir,"enemyGreen.png"))
BLUE_SHIP = pygame.image.load(path.join(img_dir,"enemyBlue.png"))
BLACK_SHIP = pygame.image.load(path.join(img_dir,"enemyBlack.png"))
cursor = pygame.image.load(path.join(img_dir,'cursor.png'))
#Unchangeable variables
MAX_UFO = 50
# iterable variables
ufocount = 0
vec = pygame.math.Vector2 
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skirmish in Space")
clock = pygame.time.Clock()
enemycoordinates = []
font_name = pygame.font.match_font('arial')
pygame.display.set_icon(cursor)

def draw_text(surf, text, size, x, y,color,font_n):
    font = pygame.font.Font(font_n, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
def enemymob():
    e = Enemy(random.choice(['red','green','black','blue']))
    all_sprites.add(e)
    enemies.add(e)
    
def speedshipmob(count,bool1):
    global speedshipblitted, Speed_ship_count
    if Speed_ship_count >= speedshipblitted:
        for i in range(count):
            sp = Speed_ship()
            
            all_sprites.add(sp)
            
            speed_ship_group.add(sp)
            speedshipblitted += 1
            if bool1 == True:
                Speed_ship_count += 1

def ufomob(xpos,ypos):
    global ufocount
    for i in range(10):
        ufo = ufoattack(xpos - (50*(i-1)),ypos)
        all_sprites.add(ufo)
        ufogroup.add(ufo)
        ufocount += 1
        
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Enemy(pygame.sprite.Sprite):
    COLOR_MAP = {
                "red": (RED_SHIP, RED_LASER),
                "green": (GREEN_SHIP, GREEN_LASER),
                "blue": (BLUE_SHIP, BLUE_LASER),
                "black": (BLACK_SHIP, BLACK_LASER)
                }
    SHOOT = random.randrange(700,800)
    def __init__(self,color):
       
        
        pygame.sprite.Sprite.__init__(self)        
        self.image,self.colorlaser = pygame.transform.scale(self.COLOR_MAP[color][0], (45, 38)),self.COLOR_MAP[color][1]                   
        self.rect = self.image.get_rect()
        self.radius = 21
        self.image.set_colorkey(BLACK)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.checked = False
        while self.checked == False:
            self.rect.centerx = random.randrange(60,WIDTH - 60)
            self.rect.bottom = random.randrange(-1500,-60)
            self.hits = pygame.sprite.spritecollide(self, enemies, True )
            if len(self.hits) != 0:
                continue
            else:
                self.checked = True
            
        self.color = color
        self.speedy = 2
        self.shoot_delay = self.SHOOT
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.check = False
        
 


    def update(self):
        if not self.rect.bottom > 0 + self.image.get_height():
            self.power = 2
        else:
            self.power = 1
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + self.image.get_height():
            while self.check == False:
                self.rect.centerx = random.randrange(60,WIDTH - 60)
                self.rect.bottom = random.randrange(-300,-60)
                self.hits2 = pygame.sprite.spritecollide(self, enemies, True )
                if len(self.hits2) != 0:
                    continue
                else:
                    self.check = True
        
        self.shoot()
        
    

        


    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                ebullet = enemyBullet(self.rect.centerx, self.rect.bottom,self.colorlaser)
                all_sprites.add(ebullet)
                enemybullets.add(ebullet)
                shoot_sound.play()
class ufoattack(pygame.sprite.Sprite):
    
                
    def __init__(self,x,y):
        super().__init__()
        COLOR_MAP = {
                "red": (UFO[0], RED_LASER),
                "green": (UFO[1], GREEN_LASER),
                "yellow": (UFO[2], BLACK_LASER),
                "blue": (UFO[3], BLUE_LASER)}
        color = random.choice(['red','green','yellow','blue'])
        self.image_orig,self.colorlaser = pygame.transform.scale(COLOR_MAP[color][0], (40, 40)),COLOR_MAP[color][1]
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.colorlaser.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedx = 4
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.radius = self.image.get_height()//2
        self.rot = 0
        self.rot_speed = 8
        self.last_update = pygame.time.get_ticks()
        self.rect.center = (x,y)
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        
        
        if self.rect.left >= WIDTH:
            self.rect.y += 50
            self.rect.x = -50
        
        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            ebullet = enemyBullet(self.rect.centerx, self.rect.bottom,self.colorlaser)
            all_sprites.add(ebullet)
            enemybullets.add(ebullet)
            shoot_sound.play()
                
class MiniBoss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = miniboss
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = vec(0,2)
        self.rect.center = (WIDTH//2,-500)
        self.shoot_t = True
        self.plunge_t = False
        self.mine_t = False
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.l_upd = pygame.time.get_ticks()
        self.once = 0
        self.minecount = random.randrange(5,8)
        self.minedone = 0
        self.reached = False
        self.mineonce= 0 
        self.shield = 100
        self.minebulletlist = []
        
    def update(self):
        if not self.mine_t:
            self.speed.x = 0
        
            if player.rect.left < self.rect.centerx:
                self.speed.x = -2
            else:
                self.speed.x = 2
        if not self.reached:
            if self.rect.top > HEIGHT//3:
                self.reached = True
                self.speed.y = 0
                
        self.rect.centerx += self.speed.x
        self.rect.centery += self.speed.y
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < HEIGHT//3 - 80 and self.reached:
            self.rect.top = HEIGHT//3 - 80
            self.speed.y = 0
        
        self.attack()
        if self.shoot_t and self.rect.top > 0:
            self.shoot()
        if self.plunge_t:
            self.plunge()
        if self.mine_t:
            self.mine()
        if not self.alive():
            self.rect.center = (WIDTH + 400,HEIGHT + 400)
            
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_t:
            self.shoot_delay = 500
        else:
            self.shoot_delay = 700
        if now - self.last_shot > self.shoot_delay and self.shoot_t:
            self.last_shot = now
            bullet1 = enemyBullet(self.rect.left + 15 , self.rect.centery,bullet_img)
            bullet2 = enemyBullet(self.rect.right - 15, self.rect.centery,bullet_img)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            enemybullets.add(bullet1)
            enemybullets.add(bullet2)
            shoot_sound.play()
        elif now - self.last_shot > self.shoot_delay and self.mine_t:
            self.last_shot = now
            bullet1 = minebullets(self.rect.left + 15 , self.rect.centery)
            bullet2 = minebullets(self.rect.right - 15, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            shoot_sound.play()
            self.minebulletlist.append(bullet1)
            self.minebulletlist.append(bullet2)
            if len(self.minebulletlist) != 0:
                for i in self.minebulletlist:
                    if not i.alive():
                        self.minedone += 1
                        self.minebulletlist.remove(i)
            
            
            
    def attack(self):
        if self.once == 0:
            self.once += 1
            self.l_upd = pygame.time.get_ticks()
        if self.shoot_t and self.rect.top > 0:
            self.mineonce = 0
            if pygame.time.get_ticks() - self.l_upd > 4000:
                self.l_upd = pygame.time.get_ticks()
                self.shoot_t = False
                self.plunge_t = True
        if self.mine_t and self.minecount <= self.minedone:
            self.mine_t = False
            self.shoot_t  = True
            self.minedone = 0
            self.minecount = random.randrange(5,8)
            self.l_upd = pygame.time.get_ticks()
            
    def plunge(self):
        self.speed.y = 9
        if self.rect.bottom > HEIGHT - 20:
            self.speed.y = -9
            self.plunge_t = False
            self.mine_t = True
    
    def mine(self):
        if self.mineonce == 0:
            self.speed.x = 9
            self.mineonce += 1
        if self.rect.right > WIDTH - 50:
            self.speed.x = - 9
        if self.rect.left < 50:
            self.speed.x = 9
        self.shoot()
        
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(BOSS,(BOSS.get_width()//3,BOSS.get_height()//3))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = vec(0,2)
        self.rect.center = (WIDTH//2,-500)
        self.shoot_t = True
        self.plunge_t = False
        self.mine_t = False
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.l_upd = pygame.time.get_ticks()
        self.once = 0
        self.minecount = random.randrange(5,8)
        self.minedone = 0
        self.reached = False
        self.mineonce= 0 
        self.shield = 100
        self.starspread = False
        self.staraim = False
        self.minebulletlist = []
        self.aimcount = 0
        self.maxaimcount = 5
        self.fiveshot = 0
        self.maxfiveshot = 4
        self.staraimonce = 0
        
    def update(self):
        if not self.mine_t and not self.starspread:
            self.speed.x = 0
        
            if player.rect.left < self.rect.centerx:
                self.speed.x = -2
            else:
                self.speed.x = 2
        if not self.reached:
            if self.rect.top > HEIGHT//3:
                self.reached = True
                self.speed.y = 0
                
        self.rect.centerx += self.speed.x
        self.rect.centery += self.speed.y
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < HEIGHT//3 - 80 and self.reached:
            self.rect.top = HEIGHT//3 - 80
            self.speed.y = 0
        
        self.attack()
        if self.shoot_t and self.rect.top > 0:
            self.shoot()
        if self.plunge_t:
            self.plunge()
        if self.mine_t:
            self.mine()
        if self.staraim:
            if len(aimstar_g) == 0  and self.aimcount <= self.maxaimcount:
                self.aimstar()
                self.aimcount += 1
        if self.starspread:
            self.insane()
            if len(aimstar_g) == 0:
                self.aimspread()
                self.fiveshot += 1
            
        if not self.alive():
            self.rect.center = (WIDTH + 400,HEIGHT + 400)
            
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_t:
            self.shoot_delay = 450
        else:
            self.shoot_delay = 700
        if now - self.last_shot > self.shoot_delay and self.shoot_t:
            self.last_shot = now
            bullet1 = enemyBullet(self.rect.left + 15 , self.rect.centery,bullet_img)
            bullet2 = enemyBullet(self.rect.right - 15, self.rect.centery,bullet_img)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            enemybullets.add(bullet1)
            enemybullets.add(bullet2)
            shoot_sound.play()
        elif now - self.last_shot > self.shoot_delay and self.mine_t:
            self.last_shot = now
            bullet1 = minebullets(self.rect.left + 15 , self.rect.centery)
            bullet2 = minebullets(self.rect.right - 15, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            shoot_sound.play()
            self.minebulletlist.append(bullet1)
            self.minebulletlist.append(bullet2)
            if len(self.minebulletlist) != 0:
                for i in self.minebulletlist:
                    if not i.alive():
                        self.minedone += 1
                        self.minebulletlist.remove(i)
            
            
            
    def attack(self):
        if self.once == 0:
            self.once += 1
            self.l_upd = pygame.time.get_ticks()
        if self.shoot_t and self.rect.top > 0:
            self.mineonce = 0
            if pygame.time.get_ticks() - self.l_upd > 4000:
                self.l_upd = pygame.time.get_ticks()
                self.shoot_t = False
                self.plunge_t = True
        if self.mine_t and self.minecount <= self.minedone:
            self.mine_t = False
            self.staraim = True
            self.minedone = 0
            self.minecount = random.randrange(5,8)
            
        if self.staraim  and self.aimcount > self.maxaimcount:
            self.staraim = False
            self.starspread = True
            self.aimcount = 0
        if self.starspread and self.fiveshot > self.maxfiveshot:
            self.starspread = False
            self.shoot_t = True
            self.fiveshot = 0
            self.staraimonce = 0
            self.l_upd = pygame.time.get_ticks()
        
    def plunge(self):
        self.speed.y = 9
        if self.rect.bottom > HEIGHT - 20:
            self.speed.y = -9
            self.plunge_t = False
            self.mine_t = True
    
    def mine(self):
        if self.mineonce == 0:
            self.speed.x = 9
            self.mineonce += 1
        if self.rect.right > WIDTH - 50:
            self.speed.x = - 9
        if self.rect.left < 50:
            self.speed.x = 9
        self.shoot()
    def aimstar(self):
        a = Aimstar(10,self.rect.midbottom)
        a.set_target(random.choice([player.rect.center,player.rect.midleft,player.rect.midright]))
        all_sprites.add(a)
        aimstar_g.add(a)
    def aimspread(self):
        a0 = 0
        a1 = 0
        a2= 0
        a3 = 0
        a4 =0
        listy = [a0,a1,a2,a3,a4]
        for i in range(5):
            listy[i] = Aimstar(6,self.rect.center)
            listy[i].set_target((self.rect.centerx + ((i-2)*104),HEIGHT))
            all_sprites.add(listy[i])
            aimstar_g.add(listy[i])
    def insane(self):
        if self.staraimonce == 0:
            self.staraimonce += 1
            self.speed.x = 9
        if self.rect.right > WIDTH - 50:
            self.speed.x = - 9
        if self.rect.left < 50:
            self.speed.x = 9
        
class DrawText(pygame.sprite.Sprite):
    def __init__(self,text,size,x,y,timer):
        super().__init__()
        self.doonce =0 
        self.last_u = pygame.time.get_ticks()
        self.timer = timer
        self.txt = text
        self.s = size
        self.x = x
        self.y = y
        self.timedone = False
        self.color = random.choice([WHITE,YELLOW,BLUE,GREEN,RED,GOLD,LEMON_CHIFFON,DODGERBLUE,LIGHTSKYBLUE,POWDERBLUE,ORANGE])
    def update(self):
        if self.doonce == 0:
            self.doonce += 1
            self.last_u = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_u <= self.timer:
            draw_text(screen,self.txt,self.s,self.x,self.y,self.color,font_name)
        else:
            self.timedone = True
            
        
class Aimstar(pygame.sprite.Sprite):
    def __init__(self,speed,pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/laserRed09.png"),(37,36)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.rect.midbottom = pos
        self.mask = pygame.mask.from_surface(self.image)
    def set_target(self, pos):
        self.target = pygame.Vector2(pos)
        self.angle = atan2(self.target.y - (self.rect.centery + self.image.get_height()), 
                            self.target.x - (self.rect.centerx + self.image.get_width()))
        self.image = pygame.transform.rotate(self.image,360 - self.angle*57.29)
        self.rect = self.image.get_rect()
    def update(self):
        dead = False
        if not dead:
            hit = pygame.sprite.collide_rect(self, player)
            if hit and not player.hidden:
                hit = pygame.sprite.collide_mask(self,player)
                if hit:
                    dead = True
                    player.shield -= random.randrange(40,60)
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100 
                    self.kill()
            if not dead:
                move = self.target - self.pos
                move_length = move.length()
        
                if move_length < self.speed or self.rect.top > HEIGHT:
                    self.kill()
                elif move_length != 0:
                    move.normalize_ip()
                    move = move * self.speed
                    self.pos += move
                
                self.rect.midtop = list(int(v) for v in self.pos)        
        
class Speed_ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(speed_ship, (45, 38))
        self.rect = self.image.get_rect()
        
        self.radius = 21
        
        self.image.set_colorkey(WHITE)
        self.speedy = 2
        self.speedtime = pygame.time.get_ticks()
        self.checkcol = False
        self.speedmargin = 700
        self.shieldhit = random.randrange(1,4) 
        self.shield = 0
        while self.checkcol == False:
                self.rect.centerx = random.randrange(60,WIDTH - 60)
                self.rect.bottom = random.randrange(-300,-60)
                self.hits = pygame.sprite.spritecollide(self, speed_ship_group, True )
                if len(self.hits) != 0:
                    continue
                else:
                    self.checkcol = True
        self.checkagain = False
    def update(self):
        
        
        self.rect.y += self.speedy
        
        if pygame.time.get_ticks() - self.speedmargin > self.speedtime:
            self.speedy = 8
        if self.rect.top > HEIGHT:
            self.kill()
            
            speedshipmob(1,True)
        hitbybullet = pygame.sprite.spritecollide(self, bullets, True)
        for hit in hitbybullet:
            self.shield += 1
            
            
            if self.shield == self.shieldhit:
                expl_sounds[random.randrange(0,2)].play()
                death_explosion_speed = Explosion(self.rect.center, 'lg')
                all_sprites.add(death_explosion_speed)
                self.kill()
                speedshipmob(random.randrange(1,3),False)
                
            else:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                shipblitprob = random.randrange(0,4)
                if shipblitprob == 1:
                    speedshipmob(1,False)
            
class minebullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = minelaser
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.image.get_height()//2
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 6
        self.boom = False
        self.low_rad = 26
        self.high_rad = 56
        self.hlim = random.randrange(HEIGHT-60,HEIGHT - 20)
        
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        hits = pygame.sprite.spritecollide(self,bullets,False)
        if hits:
            self.boomtime()
        hits = pygame.sprite.collide_circle(player, self)
        if hits:
            self.BOOM(100)
            self.kill()
        if self.rect.bottom > self.hlim:
            self.boomtime()
    
    def BOOM(self,power):
        global death_explosion
        death_explosion_boom = Explosion(self.rect.center, 'player')
        all_sprites.add(death_explosion_boom)
        if not player.hidden:
            player.shield -= power
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100 
            
    def boomtime(self):
        distpos = (abs(self.rect.centerx - player.rect.centerx),abs(self.rect.centery - player.rect.centery))
        
        power = (distpos[0] + distpos[1])//2
        if distpos[0] <= self.low_rad and distpos[1] <= self.low_rad:
            self.BOOM(100 - power)
            self.kill()
        elif distpos[0] <= self.high_rad and distpos[1] <= self.high_rad:
            self.BOOM(100 - power)
            self.kill()
        else:
            self.BOOM(0)
            self.kill()
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 23
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speed_y = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.speed = 1
        self.speed_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.speed >= 2 and pygame.time.get_ticks() - self.speed_time > POWERUP_TIME:
            self.speed -= 1
            self.speed_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT
            
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.hidden == False:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] and self.hidden == False:
            self.speedx = 8
        if keystate[pygame.K_SPACE] and self.hidden == False:
            self.shoot()
        if keystate[pygame.K_UP] and forward_drive_online and self.hidden == False:
            self.speedy = -5
        if keystate[pygame.K_DOWN] and forward_drive_online and self.hidden == False:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 2*HEIGHT//3:
            self.rect.top = 2*HEIGHT//3
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def speedup(self):
        self.speed += 1
        self.speed_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.speed >=2:
            self.shoot_delay = 150
        else:
            self.shoot_delay = 250
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top,bullet_img)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery,bullet_img)
                bullet2 = Bullet(self.rect.right, self.rect.centery,bullet_img)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class enemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun','score+','speed','life','shield', 'gun','score+','speed','shield', 'gun','score+','speed'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen(hiscore):
    screen.blit(background, background_rect)
    font = pygame.font.match_font('Calibri')
    draw_text(screen,'CoderKani presents', 30,WIDTH/2 ,20, WHITE,pygame.font.match_font('HP simplified'))
    draw_text(screen, 'Skirmish in Space!', 50, WIDTH / 2, 70,WHITE,pygame.font.match_font('algerian'))
    draw_text(screen, "Special thanks to Kenney.nl for all the art", 22,WIDTH / 2, HEIGHT / 4,WHITE,font)
    draw_text(screen, "Thanks to tgfcoder <https://twitter.com/tgfcoder> for the background music", 15,WIDTH / 2, HEIGHT / 4 + 35,WHITE,font)
    draw_text(screen, "Thanks to Wisedawn for the boss art", 18,WIDTH / 2, HEIGHT / 4 + 70,WHITE,font)
    draw_text(screen, "Arrow keys move, Space to fire and P to pause", 22,WIDTH / 2, HEIGHT / 2,WHITE,font_name)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4,WHITE,font_name)
    draw_text(screen, f"Highscore:{hiscore}", 16, WIDTH / 2, HEIGHT * 3 / 4 + 60,WHITE,font_name)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def YouWin(hiscore):
    screen.blit(background, background_rect)
    draw_text(screen, 'Skirmish in Space!', 50, WIDTH / 2, HEIGHT / 4,WHITE,pygame.font.match_font('algerian'))
    draw_text(screen, "Congratulation You Won!!", 22,WIDTH / 2, HEIGHT / 2,WHITE,font_name)
    if not newhiscore:
        draw_text(screen, "Press a key to play again and beat the hiscore", 18, WIDTH / 2, HEIGHT * 3 / 4 - 50,WHITE,font_name)
    else:
        draw_text(screen, "NEW HIGHSCORE!!", 18, WIDTH / 2, HEIGHT * 3 / 4 - 60,WHITE,font_name)
        draw_text(screen, "Press a key to play again and become better", 18, WIDTH / 2, HEIGHT * 3 / 4,WHITE,font_name)
    draw_text(screen, f"Current Highscore:{hiscore}", 16, WIDTH / 2, HEIGHT * 3 / 4 + 60,WHITE,font_name)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def YouLose(hiscore):
    screen.blit(background, background_rect)
    if newhiscore:
        draw_text(screen, "Congrats you made the new highscore", 25,WIDTH / 2, HEIGHT / 2 + 60,WHITE,font_name)
    draw_text(screen, 'Skirmish in Space!', 50, WIDTH / 2, HEIGHT / 4,WHITE,pygame.font.match_font('algerian'))
    draw_text(screen, "GAME OVER", 35,WIDTH / 2, HEIGHT / 2,WHITE,font_name)
    draw_text(screen, "Press a key to play again", 18, WIDTH / 2, HEIGHT * 3 / 4,WHITE,font_name)
    draw_text(screen, f"Current Highscore:{hiscore}", 16, WIDTH / 2, HEIGHT * 3 / 4 + 60,WHITE,font_name)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
                
if __name__ == '__main__':
    
    # Load all game graphics
   
    background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
    background_rect = background.get_rect()
    player_img = pygame.image.load(path.join(img_dir, "player1.png")).convert()
    player_img2 = pygame.image.load(path.join(img_dir, "player2.png")).convert()
    player_img3 = pygame.image.load(path.join(img_dir, "player3.png")).convert()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(BLACK)
    player_mini_img2 = pygame.transform.scale(player_img2, (25, 19))
    player_mini_img2.set_colorkey(BLACK)
    player_mini_img3 = pygame.transform.scale(player_img3, (25, 19))
    player_mini_img3.set_colorkey(BLACK)
    bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    meteor_images = []
    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
                   'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
                   'meteorBrown_tiny1.png']
    UFO = []
    UFO_LIST = ['ufoRed.png','ufoGreen.png','ufoYellow.png','ufoBlue.png']
    speed_ship = pygame.image.load(path.join(img_dir, 'speed_ship.png'))
    BOSS = pygame.image.load(path.join(img_dir, 'boss9.png'))
    miniboss = pygame.transform.scale(pygame.image.load(path.join(img_dir,'miniboss.png')), (120,120)).convert()
    minelaser = pygame.image.load(path.join(img_dir,'laserRed10.png')).convert()
    for img in UFO_LIST:
        UFO.append(pygame.image.load(path.join(img_dir,img)).convert())
    
    
    
    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    explosion_anim['player'] = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)
        filename = 'sonicExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        explosion_anim['player'].append(img)
    powerup_images = {}
    powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
    powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
    powerup_images['life'] = pygame.image.load(path.join(img_dir, 'life.png')).convert()
    powerup_images['speed'] = pygame.image.load(path.join(img_dir, 'pill_blue.png')).convert() 
    powerup_images['score+'] = pygame.image.load(path.join(img_dir, 'star_gold.png')).convert()
    # Load all game sounds
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    shoot_sound.set_volume(0.05)
    shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
    shield_sound.set_volume(0.05)
    power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
    power_sound.set_volume(0.05)
    expl_sounds = []
    for snd in ['expl3.wav', 'expl6.wav']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    expl_sounds[0].set_volume(0.05)
    expl_sounds[1].set_volume(0.05)
    player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
    player_die_sound.set_volume(0.05)
    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.07)
    
    pygame.mixer.music.play(loops=-1)
    # Game loop
    game_over = True
    youwinI = False
    youloseI = False
    newhiscore = False
    running = True
    oncedoing = 0
    paused = False
    run = True
    if(not path.exists("hiscore.txt")):
        with open("hiscore.txt", "wb") as f:
            f.write(codecs.encode(b'52006','base64','strict'))
            
    try:
        with open("hiscore.txt", "rb") as f:
            hiscor = f.read()
            hiscore = codecs.decode(hiscor,'base64','strict')
            int(hiscore)
            
    except Exception as e:
        with open("hiscore.txt", "wb") as f:
            f.write(codecs.encode(b'52006','base64','strict'))
        with open("hiscore.txt", "rb") as f:
            hiscor = f.read()
            hiscore = codecs.decode(hiscor,'base64','strict')
    while running:
        if paused:
            while run:
                screen.blit(background, background_rect)
                draw_text(screen, 'PAUSED', 50, WIDTH//2, HEIGHT//2, WHITE, pygame.font.match_font('algerian'))
                pygame.display.update()
                clock.tick(FPS)
                
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        run = False
                        running = False
                    #pausing
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = not paused
                            run = False
        else:
            if game_over:
                if oncedoing == 0:
                    show_go_screen(int(hiscore))
                    
                    oncedoing += 1
                else:
                    if youwinI:
                        YouWin(int(hiscore))
                    if youloseI:
                        YouLose(int(hiscore))
                game_over = False
                all_sprites = pygame.sprite.Group()
                mobs = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                powerups = pygame.sprite.Group()
                aimstar_g = pygame.sprite.Group()
                txt_g = pygame.sprite.Group()
                player = Player()
                death_explosion = Explosion(player.rect.center, 'player')
                enemies = pygame.sprite.Group()
                enemybullets = pygame.sprite.Group()
                all_sprites.add(player)
                speed_ship_group = pygame.sprite.Group()
                ufogroup = pygame.sprite.Group()
                mini = MiniBoss()
                bossy = Boss()
                speedshipblitted = 0
                ufocount = 0
                level = 0
                wave_l = 5
                level6once = 0
                level8once = 0
                enemytime = pygame.time.get_ticks()
                speed_shiptime = False
                youwinI = False
                youloseI = False
                newhiscore = False
                WAVE_CHANGE = 7000
                for i in range(8):
                    newmob()
                
                
                score = 0
            run = True
            if enemytime+ WAVE_CHANGE < pygame.time.get_ticks() and level < 4:
                enemytime = pygame.time.get_ticks()
                for i in range(level*wave_l):
                    enemymob()
                if len(enemies) == 0 and level<4:
                        level += 1
            if level == 4 and len(speed_ship_group) == 0:
                for i in range(3):
                    speedshipmob(random.randrange(1,3),False)    
                if Speed_ship_count <= speedshipblitted:
                    level += 1
            if level == 5:
                if ufocount >= MAX_UFO:
                    level += 1
                    forward_drive_online = True
                    s = DrawText('Forward drive online!',40,WIDTH//2 - 60,HEIGHT//2 - 60,1500)
                    txt_g.add(s)
                elif len(ufogroup) == 0 and level == 5:
                    ufomob(-100,HEIGHT//2)
            if level == 6:
                if level6once == 0:
                    level6once += 1
                    #text,size,x,y,timer
                    s = DrawText('MINIBOSS INCOMING',40,WIDTH//2,HEIGHT//2,1500)
                    txt_g.add(s)
                dooncelevel7 = 0
                for i in ufogroup:
                    i.kill()
                    all_sprites.add(mini)
                level7c = 0
            if level == 7:
                if dooncelevel7 == 0:
                    for i in range(10):
                        enemymob()
                    dooncelevel7 += 1
                    for i in range(5):
                        speedshipmob(random.randrange(1,3),False)
                        level7c += 1
                if len(speed_ship_group) == 0 and level7c < 20:
                    for i in range(5):
                        speedshipmob(random.randrange(1,3),False)
                        level7c += 1
                if not level7c < 20 and len(speed_ship_group) == 0 and len(enemies) == 0:
                    level += 1
            if level == 8:
                if level8once == 0:
                    s1 = DrawText('BOSS INCOMING',40,WIDTH//2,HEIGHT//2,1000)
                    txt_g.add(s1)
                    level8once += 1
                    all_sprites.add(bossy)
                    
                
                
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                #pausing
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        
            # Update
            all_sprites.update()
        
            # check to see if a bullet hit a mob
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                plus = 50 - hit.radius
                score += 50 - hit.radius
                s1 = DrawText(f'+{plus}',25,hit.rect.centerx,hit.rect.centery,500)
                txt_g.add(s1)
                random.choice(expl_sounds).play()
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                if random.random() > 0.95:
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
                newmob()
            #check to see if miniboss hit player
            hits = pygame.sprite.collide_mask(player, mini)
            if hits and all_sprites.has(mini) and not player.hidden:
                player.shield -= random.randrange(60,80)
                mini.shield -= 10
                expl = Explosion(hit.rect.center,'lg')
                all_sprites.add(expl)
                
                if player.shield <= 0:
                    player_die_sound.play()
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.shield = 100
                if mini.shield <= 0:
                    death_explosion_mini = Explosion(mini.rect.center, 'player')
                    all_sprites.add(death_explosion_mini)
                    player_die_sound.play()
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
                    score += 500
                    s1 = DrawText('+500',30,mini.rect.centerx,mini.rect.centery,500)
                    txt_g.add(s1)
                    mini.kill()
                    level += 1
            #check if boss hit player
            hits = pygame.sprite.collide_mask(player, bossy)
            if hits and all_sprites.has(bossy) and not player.hidden:
                player.shield -= random.randrange(60,80)
                bossy.shield -= 4
                expl = Explosion(hit.rect.center,'lg')
                all_sprites.add(expl)
                
                if player.shield <= 0:
                    player_die_sound.play()
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.shield = 100
                if bossy.shield <= 0:
                    death_explosion_bossy = Explosion(bossy.rect.center, 'player')
                    all_sprites.add(death_explosion_bossy)
                    player_die_sound.play()
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
                    score += 800
                    s1 = DrawText('+800',30,bossy.rect.centerx,bossy.rect.centery,500)
                    txt_g.add(s1)
                    bossy.kill()
                    level += 1
            #check if bullet hit miniboss
            if all_sprites.has(mini):
                hits = pygame.sprite.spritecollide(mini, bullets, True)
                if hits and mini.rect.top > 0:
                    mini.shield -= random.randint(3,5)
                    expl = Explosion(hit.rect.center,'sm')
                    all_sprites.add(expl)
                    if mini.shield <= 0:
                        death_explosion_mini = Explosion(mini.rect.center, 'player')
                        all_sprites.add(death_explosion_mini)
                        player_die_sound.play()
                        pow = Pow(hit.rect.center)
                        all_sprites.add(pow)
                        powerups.add(pow)
                        score += 500
                        s1 = DrawText('+500',30,mini.rect.centerx,mini.rect.centery,500)
                        txt_g.add(s1)
                        mini.kill()
                        level += 1
            #check if bullet hit boss
            if all_sprites.has(bossy):
                hits = pygame.sprite.spritecollide(bossy, bullets, True)
                if hits and bossy.rect.top > 0:
                    bossy.shield -= random.randint(1,2)
                    expl = Explosion(hit.rect.center,'sm')
                    all_sprites.add(expl)
                    if bossy.shield <= 0:
                        death_explosion_boss = Explosion(bossy.rect.center, 'player')
                        all_sprites.add(death_explosion_boss)
                        player_die_sound.play()
                        pow = Pow(bossy.rect.center)
                        all_sprites.add(pow)
                        powerups.add(pow)
                        score += 800
                        s1 = DrawText('+800',30,bossy.rect.centerx,bossy.rect.centery,500)
                        txt_g.add(s1)
                        bossy.kill()
                        level += 1
            #check to see if a bullet hit a enemy
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                plus = random.randrange(50,70)
                score += plus
                s1 = DrawText(f'+{plus}',25,hit.rect.centerx,hit.rect.centery,500)
                txt_g.add(s1)
                random.choice(expl_sounds).play()
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                if random.random() > 0.95:
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
            #check to see if bullet hit UFO
            hits = pygame.sprite.groupcollide(ufogroup,bullets,True,True)
            for hit in hits:
                plus = random.randrange(50,70)
                score += plus
                s1 = DrawText(f'+{plus}',25,hit.rect.centerx,hit.rect.centery,500)
                txt_g.add(s1)
                random.choice(expl_sounds).play()
                expl = Explosion(hit.rect.center,'lg')
                all_sprites.add(expl)
                if random.random() > 0.97:
                    poww = Pow(hit.rect.center)
                    all_sprites.add(poww)
                    powerups.add(poww)
            #check to see if enemybullet hits player
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, enemybullets,True)
                for hit in hits:
                    player.shield -= random.randrange(30,45)
                    expl = Explosion(hit.rect.center,'sm')
                    all_sprites.add(expl)
                    
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
            
            # check to see if a mob hit the player
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
                for hit in hits:
                    player.shield -= hit.radius * 2
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    newmob()
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
                    
            #check to see if speed ship hit the player
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, speed_ship_group , True, pygame.sprite.collide_circle)
                for hit in hits:
                    player.shield -= random.randrange(60,80)
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    speedshipmob(random.randrange(1,3),False)
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
            
            #check to see if UFO hits the player
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, ufogroup, True ,pygame.sprite.collide_circle)
                for hit in hits:
                    player.shield -= random.randrange(20,40)
                    expl = Explosion(hit.rect.center,'sm')
                    all_sprites.add(expl)
                    
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
                    
            #check to see if a enemy hit the player
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, enemies, True ,pygame.sprite.collide_circle)
                for hit in hits:
                    player.shield -= random.randrange(20,40)
                    expl = Explosion(hit.rect.center,'sm')
                    all_sprites.add(expl)
                    
                    if player.shield <= 0:
                        player_die_sound.play()
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
        
            # check to see if player hit a powerup
            if not player.hidden:
                hits = pygame.sprite.spritecollide(player, powerups, True)
                for hit in hits:
                    if hit.type == 'shield':
                        player.shield += random.randrange(50, 80)
                        shield_sound.play()
                        if player.shield >= 100:
                            player.shield = 100
                    if hit.type == 'gun':
                        player.powerup()
                        power_sound.play()
                    if hit.type == 'score+':
                        plus = random.randrange(500,2000)
                        score += plus
                        s1 = DrawText(f'+{plus}',30,hit.rect.centerx,hit.rect.centery - 60,1000)
                        txt_g.add(s1)
                        power_sound.play()
                    if hit.type == 'speed':
                        player.speedup()
                        power_sound.play()
                    if hit.type == 'life':
                        player.lives += 1
                        if player.lives == 4:
                            player.lives = 3
        
            # if the player died and the explosion has finished playing
            if player.lives == 0 and not death_explosion.alive():
                game_over = True
                youloseI = True
            #if win
            if level == 9:
                youwinI = True
                game_over = True
                youloseI = False
    
        
            # Draw / render
            screen.blit(background, background_rect)
            if player.hidden or player.lives == 0:
                for i in all_sprites:
                    if not i ==player:
                        screen.blit(i.image,i.rect)
            else:
               all_sprites.draw(screen)
            draw_text(screen, str(score), 18, WIDTH / 2, 10,WHITE,font_name)
            for i in txt_g:
                i.update()
                if i.timedone:
                    i.kill()
            draw_shield_bar(screen, 5, 5, player.shield)
            if level == 6:
                draw_shield_bar(screen, mini.rect.left,mini.rect.top, mini.shield)
            if level == 8:
                draw_shield_bar(screen, bossy.rect.left + 20,bossy.rect.top, bossy.shield)
            draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
            # *after* drawing everything, flip the display
            
            pygame.display.flip()
            
            if int(hiscore)<score:
                    newhiscore = True
                    hiscore = str(score).encode('utf8')
                    with open("hiscore.txt", "wb") as f:
                        f.write(codecs.encode(hiscore,'base64','strict'))
                    
pygame.quit()