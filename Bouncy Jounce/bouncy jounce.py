# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:18:42 2021

@author: CODERKANI
"""
# Art from Kenney.nl
# Happy Tune by http://opengameart.org/users/syncopika
# Yippee by http://opengameart.org/users/snabisch


import pygame
from pygame.locals import *
import sys
import random
from PIL import Image
from os import path
import codecs
from math import atan2
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
#dir
dir_ = path.dirname(__file__)
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
font_name_init = 'Halvita'
Title_font = 'algerian'
TITLE_FONT = pygame.font.match_font(Title_font)
FONT_NAME = pygame.font.match_font(font_name_init)
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Jounce")

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
POWDERBLUE = (176,224,230)
LIGHTSKYBLUE = (135,206,250)
DODGERBLUE = (30,144,255)
ORANGE = (255,140,0)
GOLD = (255,215,0)
LEMON_CHIFFON = (255,250,205)
TITLE = 'Bouncy Jounce!'
#changeable var
platform_type = {'grass':0,'cake':4,'sand':8,'stone':12,'wood':16,'snow':20}
plat_type = random.choice(['grass','cake','sand','stone','wood','snow'])
mob_fly_man_timer = 0
mob_fly_man_timer2 = 0
New_high_score = False
player_dead = False
# time during game
tdg = 0
#layers
PLAYER_LAYER = 4
PLATFORM_LAYER = 2
PLATFORMD_LAYER = 1
POW_LAYER = 2
MOB_LAYER = 4
CLOUD_LAYER = 0
Prop_layer = 3


#other non changeable var
POW_SPAWN_PCT = 7
BOOST_POW = 45
SPIKEMAN_PCT = 20
SUM_BG = Image.new('RGBA',(400,450))
WIN_BG =  Image.new('RGBA',(400,450))
RAI_BG = Image.new('RGBA',(400,450))
season_list = [SUM_BG,WIN_BG,RAI_BG]
ses_type = 'summer'
#sounds

snd_dir = path.join(dir_, 'snd')
jump_sound = pygame.mixer.Sound(path.join(snd_dir, 'Jump33.wav'))
jump_sound_fem = pygame.mixer.Sound(path.join(snd_dir, 'Jump40.wav'))
boost_sound = pygame.mixer.Sound(path.join(snd_dir, 'Boost16.wav'))
jump_sound.set_volume(0.5)
jump_sound_fem.set_volume(0.2)
boost_sound.set_volume(0.5)

#png files
instruction = pygame.image.load('img/instructions.png').convert()
instructionbox = pygame.image.load('img/instructionbox.png').convert()

#blend circles
def circle_surf(radius, color,width):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius , radius), radius,width)
    
    surf.set_colorkey((0, 0, 0))
    return surf
#background image making func
def bg_img(img,season):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            season_dict = {'summer':[255,69 + ((HEIGHT-j)//2),0],
                   'winter':[j//2,220,220],
                   'rainy':[220 - (j//(450//115)),220 - (j//(450//115)),220 - (j//(450//115))]}
            color1 = season_dict[season][0]
            color2 = season_dict[season][1]
            color3 = season_dict[season][2]
            img.putpixel((i,j),(color1,color2,color3))
    
# text drawing func
def draw_text(text,size,color,x,y,font_name):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    displaysurface.blit(text_surface, text_rect)

#start screen func
def show_start_screen(highscore):
    global tdg
    season_var = 0
    last_update = 0
    pygame.mixer.music.load(path.join(snd_dir, 'Yippee.ogg'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    for i in range(3):
                c = Cloud(True)
                c.rect.y = random.randrange(0 + c.rect.height, HEIGHT - c.rect.height)
                
                clouds.add(c)
    surf = background(season_list[season_var])
    running =  True
    while running:
        if pygame.time.get_ticks() - last_update > 10000:
            last_update = pygame.time.get_ticks()-tdg
            season_var = (season_var + 1) % 3
            surf = background(season_list[season_var])
        FramePerSec.tick(FPS)
        
        displaysurface.blit(surf,(0,0))
        for entity in clouds:
            entity.move()
            displaysurface.blit(entity.surf,entity.rect)
        draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4,TITLE_FONT)
        draw_text('CoderKani presents', 30, BLACK, WIDTH/2 , HEIGHT/4 - 50, pygame.font.match_font('HP simplified'))
        draw_text("Arrow keys or WAD to move and jump.", 22, BLACK, WIDTH / 2, HEIGHT / 2,FONT_NAME)
        draw_text("Can use space to jump too!", 22, BLACK, WIDTH / 2, HEIGHT / 2 + 30,FONT_NAME)
        draw_text("Press a key to play", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4,FONT_NAME)
        draw_text("High Score: " + str(highscore), 22,BLACK, WIDTH / 2, 15,FONT_NAME)
        displaysurface.blit(instructionbox,(WIDTH//2 - 56,HEIGHT - 70))
        pygame.display.flip()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.display.quit()
                sys.exit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                if pygame.Rect(WIDTH//2 - 56,HEIGHT-70,112,39).collidepoint(mx,my):
                    inst_screen()
            if event.type == pygame.KEYUP:
                running = False
                
        
    pygame.mixer.music.fadeout(500)
    for entity in clouds:
        entity.kill()
    tdg = pygame.time.get_ticks()
    
#instruction screen func
def inst_screen():
    running = True
    while running:
        FramePerSec.tick(FPS)
        displaysurface.blit(instruction,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            
            
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.display.quit()
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYUP:
                running = False
                

#game over screen
def game_over_screen(player,highscore):
   # game over/continue
    global tdg
    pygame.mixer.music.load(path.join(snd_dir, 'Yippee.ogg'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    displaysurface.blit(bgsurf,(0,0))
    draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4,TITLE_FONT)
    draw_text("Score: " + str(player.score), 22, WHITE, WIDTH / 2, HEIGHT / 2,FONT_NAME)
    draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4,FONT_NAME)
    if New_high_score:
        
        draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40,FONT_NAME)
        
    else:
        draw_text("High Score: " + str(highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40,FONT_NAME)
    pygame.display.flip()
    wait_for_key()
    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.load(path.join(snd_dir, 'Happy_Tune.ogg'))
    pygame.mixer.music.set_volume(2.00)
    pygame.mixer.music.play(loops=-1)
    tdg = pygame.time.get_ticks()
#if key pressed
def wait_for_key():
    waiting = True
    while waiting:
        FramePerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def background(img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    surface = pygame.image.fromstring(data,size,mode)
    return surface
    
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width//3,height//3))
        return image

class Snow():
    def __init__(self):
        self.start_x = random.randrange(10,WIDTH - 9)
        self.start_y = random.randrange(-100,1)
        self.vel_x = random.choice([-1,1])
        self.vel_y = random.randrange(4,7)
        self.radius = random.randint(4, 6)
        self.x,self.y = self.start_x,self.start_y
        pygame.draw.circle(displaysurface , WHITE, (self.x,self.y), int(self.radius))
        
    def draw(self):
        pygame.draw.circle(displaysurface , WHITE, (self.x,self.y), int(self.radius))
        
    def move(self):
        self.draw()
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x = random.choice([-1,1])
        self.vel_y = random.randrange(4,7)
        self.radius -= (random.randrange(0,101)/10000)
        if self.y > HEIGHT or self.x < 0 or self.x > WIDTH or self.radius <= 0:
            snow_g.remove(self)
        
class Rain():
    def __init__(self):
        self.start_x = random.randrange(10,WIDTH - 9)
        self.start_y = random.randrange(-100,1)
        self.vel_y = random.randrange(4,7)
        self.height = random.randint(3, 9)
        self.width = random.randint(2,3)
        
        self.x,self.y = self.start_x,self.start_y
        pygame.draw.rect(displaysurface , POWDERBLUE , (self.x,self.y,self.width,self.height))
        pygame.draw.line(displaysurface, LIGHTSKYBLUE,(self.x + self.width//2,self.y), (self.x + self.width//2,self.y - self.height//2),3)
    def draw(self):
        pygame.draw.rect(displaysurface , POWDERBLUE , (self.x,self.y,self.width,self.height))
        pygame.draw.line(displaysurface, LIGHTSKYBLUE,(self.x + self.width//2,self.y), (self.x + self.width//2,self.y - self.height//2),3)
        
    def move(self):
        self.draw()
        
        self.y += self.vel_y
        
        self.vel_y = random.randrange(4,7)
        
        if self.y > HEIGHT:
            rain_g.remove(self)

class Dangercloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = CLOUD_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.surf = self.spritesheet.get_image(0,1152,260,134)
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)
        self.speed = random.randrange(-5,5)
        self.attack_update = 0
        self.attack_timer = 1000
        
    def move(self):
        self.attacking()
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
        if self.move:
            if self.speed == 0:
                self.speed = random.choice([4,-4,2,-2])
            self.rect.move_ip(self.speed,0)
        if not ses_type == 'rainy':
            self.kill()
            
    def attacking(self):
        if self.rect.centery > 0:
            now = pygame.time.get_ticks() - tdg
            if now - self.attack_update > self.attack_timer:
                l = lightning(self.rect.center)
                l_g.add(l)
                all_sprites.add(l)
                self.attack_update = pygame.time.get_ticks() - tdg
    
class circ_eff():
    def __init__(self,pos,color):
        self.pos = [pos[0],pos[1]]
        self.radius = 5
        self.thick = 5
        self.times = 0
        self.max_t = 20
        self.transparency = 250
        self.transparency_less = 10
        self.rgb = color
        self.color = (color[0],color[1],color[2],self.transparency)
        self.radius_up = 0.25
        
        if color == GREEN:
            self.bc = (30,144,255)
        elif color == ORANGE:
            self.bc = (255,69,0)
        elif color == LEMON_CHIFFON:
            self.bc = GOLD
        self.offset = self.radius * 2
        
    def circ(self):
        pygame.draw.circle(displaysurface,self.color,self.pos,self.radius,self.thick)
        
        displaysurface.blit(circle_surf(self.offset, (self.bc[0],self.bc[1],self.bc[2],self.transparency),0), (int(self.pos[0] - self.offset), int(self.pos[1] - self.offset)), special_flags=BLEND_RGB_MAX)
        
    def update(self):
        
            self.circ()
            self.transparency -= self.transparency_less
            self.color = (self.rgb[0],self.rgb[1],self.rgb[2],self.transparency)
            self.thick += 1
            self.times +=  1
            self.radius += self.radius_up
            self.offset = self.radius * 2
            if self.max_t == self.times or player_dead:
                circ_g.remove(self)
            

class Fireball(pygame.sprite.Sprite):
    def __init__(self,speed,pos):
        super().__init__()
        self._layer = MOB_LAYER
        self.surf1 = pygame.image.load("img/Fireball1.png").convert()
        self.surf2 = pygame.image.load('img/Fireball2.png').convert()
        self.surf_l = [pygame.transform.scale(self.surf1,(self.surf1.get_width() * 4,self.surf1.get_height() * 4)).convert(),
                       pygame.transform.scale(self.surf2,(self.surf2.get_width() * 4,self.surf2.get_height() * 4)).convert()]
        if ses_type == 'summer':
            self.type = 1
        else:
            self.type = 0
        self.surf = self.surf_l[self.type]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.rect.midbottom = pos
        self.mask = pygame.mask.from_surface(self.surf)
        self.colors = [GREEN,ORANGE]
    def set_target(self, pos):
        self.target = pygame.Vector2(pos)
        self.angle = atan2(self.target.y - (self.rect.centery + self.surf.get_height()), 
                           self.target.x - (self.rect.centerx + self.surf.get_width()))
        self.surf = pygame.transform.rotate(self.surf,360 - self.angle*57.29)
        self.rect = self.surf.get_rect()
    def update(self):
        global player_dead
        hits = pygame.sprite.spritecollide(self,platforms,False)
        if hits:
            hits = pygame.sprite.spritecollide(self,platforms,False,pygame.sprite.collide_mask)
            if hits:
                x = circ_eff(self.rect.center,self.colors[self.type])
                circ_g.append(x)
                self.kill()
        hit = pygame.sprite.collide_rect(self, P1)
        if hit:
            hit = pygame.sprite.collide_mask(self,P1)
            if hit:
                player_dead = True
                x = circ_eff(self.rect.center,self.colors[self.type])
                circ_g.append(x)
                self.kill()
        if len(prop_g) != 0 and P1.shield:
            pygame.sprite.spritecollide(self, prop_g, True)
            x = circ_eff(self.rect.center,self.colors[self.type])
            circ_g.append(x)
            self.kill()
        move = self.target - self.pos
        move_length = move.length()

        if move_length < self.speed:
            self.pos = self.target
            x = circ_eff(self.rect.center,self.colors[self.type])
            circ_g.append(x)
            if player_dead == False:
                self.kill()
        elif move_length != 0:
            move.normalize_ip()
            move = move * self.speed
            self.pos += move

        self.rect.midtop = list(int(v) for v in self.pos)
                
class lightning(pygame.sprite.Sprite):
    def __init__(self,pos):
        self._layer = MOB_LAYER
        super().__init__()        
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.surf = self.spritesheet.get_image(897,0,55,114)
        self.vy = random.randint(4,10)
        self.rect = self.surf.get_rect()
        self.rect.midtop = pos
        self.mask = pygame.mask.from_surface(self.surf)
        self.color = LEMON_CHIFFON
        self.surf.set_colorkey(BLACK)
    def move(self):
        global player_dead
        self.rect.y += self.vy
        if self.rect.top > HEIGHT:
            self.kill()
        hit = pygame.sprite.spritecollide(self,platforms,False)
        if hit:
            hit = pygame.sprite.spritecollide(self,platforms,False,pygame.sprite.collide_mask)
            if hit:
                c = circ_eff(self.rect.midbottom,self.color)
                circ_g.append(c)
                self.kill()
        
        if not P1.wing and not P1.boost and not P1.shield:
            hits = pygame.sprite.collide_rect(self,P1)
            if hits:
                hits = pygame.sprite.collide_mask(self,P1)
                if hits:
                    player_dead = True
                    c = circ_eff(self.rect.midbottom,self.color)
                    circ_g.append(c)
                    self.kill()
        if len(prop_g) != 0 and P1.shield:
            hit = pygame.sprite.spritecollide(self, prop_g, False)
            if hit:
                x = circ_eff(self.rect.midbottom,self.color)
                circ_g.append(x)
                self.kill()
            
            
class Particle(pygame.sprite.Sprite):
    def __init__(self,pos,plat_nom):
        super().__init__()
        self._layer = PLATFORM_LAYER
        self.x,self.y = pos
        self.vx, self.vy = random.randrange(-2,3),10#*0.1
        
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.surf10 = [2,3,22,23,10,11,18,19]
        self.surf11 = [6,7]
        self.plat_typ = None
        # [brown,darkbrown,grey]
        self.surf_style1 = [self.spritesheet.get_image(820, 1877, 44, 48),
                            self.spritesheet.get_image(784, 2003, 54, 43),
                            self.spritesheet.get_image(623,2005, 38, 41)]
        if plat_nom in self.surf10:
            self.surf1_choose = 0
            if plat_nom == 2 or plat_nom == 3:
                self.plat_typ = 'grass'
            elif plat_nom == 10 or plat_nom == 11:
                self.plat_typ = 'sand'
            elif plat_nom == 22 or plat_nom == 23:
                self.plat_typ = 'snow'
            else:
                self.plat_typ = 'wood'
        elif plat_nom in self.surf11:
            self.surf1_choose = 1
            self.plat_typ = 'cake'
        else:
            self.surf1_choose = 2
            self.plat_typ = 'stone'
        self.surf_style2 = {'wood':self.spritesheet.get_image(784, 2003, 54, 43),
                            'grass':self.spritesheet.get_image(800, 1003, 48, 46),
                            'cake':self.spritesheet.get_image(829, 86, 53, 46),
                            'stone':self.spritesheet.get_image(826, 1364,51 ,43 ),
                            'sand':self.spritesheet.get_image(563,2005,58 ,41 ),
                            'snow':self.spritesheet.get_image(852,1168 ,51 ,49 )}
        self.surf = random.choice([self.surf_style1[self.surf1_choose],self.surf_style2[self.plat_typ]])
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.center = pos
        
    def move(self):
       
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        
        
        
        
    def draw(self):
        displaysurface.blit(self.surf,self.rect)        
    
class Props(pygame.sprite.Sprite):
    def __init__(self,player,costume_type,costume_nom):
        if costume_type != 2:
            self._layer = Prop_layer
        else:
            self._layer = 1
        super().__init__()
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.player = player
        #[wings,boost,shield]
        self.images = [[self.spritesheet.get_image(558, 651, 85, 74),self.spritesheet.get_image(571,1458 ,85 ,74)],[self.spritesheet.get_image(563,1843 ,133 ,160),self.spritesheet.get_image(900, 1733, 41,80)],
                       [pygame.transform.scale(self.spritesheet.get_image(0,1662,211,215),((211//5)*3,(215//5)*3))]]
        self.surf = self.images[costume_type][costume_nom]
        
        self.surf.set_colorkey(BLACK)
        
        self.rect = self.surf.get_rect()
        self.costume_type = costume_type
        self.costume_nom = costume_nom
        if self.costume_type == 0:
            if self.costume_nom == 0:
                self.rect.right = self.player.rect.left + 10
                self.rect.centery = self.player.rect.centery
            else:
                self.rect.left = self.player.rect.right - 10
                self.rect.centery = self.player.rect.centery
        elif self.costume_type == 1:          
            if self.costume_nom == 0:
                before_offsetx = self.player.rect.centerx
                
                self.rect.center = (before_offsetx + 8,self.player.rect.centery )
            else:
                before_offsetx = self.player.rect.midbottom[0]
                self.rect.center = (before_offsetx + 5,self.player.rect.midbottom[1])
                
        else:
            self.rect.center = self.player.rect.center
    def move(self):
        if self.player.power == False:            
            self.kill()
        if self.player.shield:
            self.rect.center = self.player.rect.center
        elif self.player.wing == True:
            if self.costume_nom == 0:
                self.rect.right = self.player.rect.left + 10
                self.rect.centery = self.player.rect.centery
            else:
                self.rect.left = self.player.rect.right - 7
                self.rect.centery = self.player.rect.centery
        else:
            
            if self.costume_nom == 0:
                before_offsetx = self.player.rect.centerx
                self.rect.center = (before_offsetx + 5,self.player.rect.centery)
            else:
                before_offsetx = self.player.rect.midbottom[0]
                self.rect.center = (before_offsetx + 3,self.player.rect.midbottom[1])
            
class sun(pygame.sprite.Sprite):
    def __init__(self,player):
        self._layer = CLOUD_LAYER
        super().__init__()
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.images = [[self.spritesheet.get_image(534, 913, 142, 148),
                        self.spritesheet.get_image(421, 1390, 148, 142)],
                       [self.spritesheet.get_image(534, 763, 142, 148),
                        self.spritesheet.get_image(464, 1122, 148, 141)]]
        
        self.last_update = 0
        self.sun_type = 0
        if ses_type == 'summer':
            self.sun = 0
        else:
            self.sun = 1
        self.surf = self.images[self.sun][self.sun_type]
        self.rect = self.surf.get_rect()
        for img in self.images[0]:
            img.set_colorkey(BLACK)
        for img in self.images[1]:
            img.set_colorkey(BLACK)
        self.pos = (WIDTH -  self.surf.get_width() - 10,0 + self.surf.get_height() + 4)
        self.rect.bottomleft = self.pos
        self.attack_update = 0
        self.attack_timer = 13000
        self.p = player
    def move(self):
        self.attacking()
        if pygame.time.get_ticks() - tdg - self.last_update >= 100:
            self.sun_type += 1
            self.sun_type %= 2
            self.last_update = pygame.time.get_ticks() -tdg
        if ses_type == 'summer':
            self.sun = 0
        elif ses_type == 'rainy':
            self.kill()
        else:
            self.sun = 1
        self.surf = self.images[self.sun][self.sun_type]
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = self.pos
    def attacking(self):
        if pygame.time.get_ticks() - self.attack_update - tdg >= self.attack_timer:
            self.attack_update = pygame.time.get_ticks() - tdg
            f = Fireball(random.randint(5,8),self.rect.midtop)
            f.set_target(self.p.rect.center)
            fireball_g.add(f)
            
            
class Pow(pygame.sprite.Sprite):
    def __init__(self,plat):
        super().__init__()
        self._layer = POW_LAYER
        
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        
        self.plat = plat
        self.type = random.choice(['boost','random','shield','wings','life'])
        
        self.image_dict = {'wings':self.spritesheet.get_image(826, 1292, 71, 70),
                      'random':self.spritesheet.get_image(894, 1661, 71, 70),
                      'shield':self.spritesheet.get_image(826,134,71,70),
                      'boost':self.spritesheet.get_image(820,1805,71,70),
                      'life': self.spritesheet.get_image(826,1220, 71, 70)}
        self.surf = self.image_dict[self.type]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
        self.moving = self.plat.moving

    def move(self):
        if not platforms.has(self.plat):
            self.kill()
        if self.moving == True:  
            self.rect.centerx = self.plat.rect.centerx
            
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self,move):
        super().__init__()
        self._layer = CLOUD_LAYER
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(path.join('img', 'cloud{}.png'.format(i))).convert())
        self.surf = random.choice(self.cloud_images)
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.scale = random.randrange(50, 101) / 100
        self.surf = pygame.transform.scale(self.surf, (int(self.rect.width * self.scale),
                                                     int(self.rect.height * self.scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)
        self.speed = random.randrange(-5,5)
        
    def move(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()
        if self.move:
            if self.speed == 0:
                self.speed = random.choice([4,-4,2,-2])
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
            
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self._layer = PLAYER_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.load_images()
        self.bunny = 0
        self.powhit = False
        self.broken_list = [2,3,6,7,10,11,14,15,18,19,22,23]
        self.surf = self.standing_frames[self.bunny][0]
        self.rect = self.surf.get_rect()
        self.walking = False
        self.last_update = 0
        self.current_frame = 0
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0
        self.wing = False
        self.wing_time = 1000
        self.boost = False
        self.wing_updated = False
        self.now_wing = 0
        self.last_update_2 = 0
        self.power = False
        self.shield = False
        self.now_shield = 0
        self.shield_time = 5000
        self.shield_updated = False
        self.power_was_boost = False
        self.power_once = 0
        self.lives = 3
        
    def load_images(self):
        self.standing_frames = [[self.spritesheet.get_image(614, 1063, 120, 191),
                                self.spritesheet.get_image(690, 406, 120, 201)],
                                [self.spritesheet.get_image(581, 1265, 121, 191),
                                self.spritesheet.get_image(584, 0, 121, 201)]]
        for framelist in self.standing_frames:
            for frame in framelist:
                frame.set_colorkey(BLACK)
        self.walk_frames_r = [[self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
                              ,[self.spritesheet.get_image(584, 203, 121, 201),
                              self.spritesheet.get_image(678, 651, 121, 207)]]
        self.walk_frames_l = [[],[]]
        self.list = -1
        for framelist in self.walk_frames_r:
            self.list += 1
            for frame in framelist:
                
                frame.set_colorkey(BLACK)
                self.walk_frames_l[self.list].append(pygame.transform.flip(frame, True, False))
        self.jump_frame = [self.spritesheet.get_image(382, 763, 150, 181),
                            self.spritesheet.get_image(416, 1660, 150, 181)]
        
        for frame in self.jump_frame:
            frame.set_colorkey(BLACK)
        self.dead_frame = [self.spritesheet.get_image(382, 946, 150, 174),
                           self.spritesheet.get_image(411, 1866, 150,174)]
        for frame in self.dead_frame:
            frame.set_colorkey(BLACK)
        
    
    def animate(self):
        now = pygame.time.get_ticks() - tdg
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking and not self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l[self.bunny])
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.surf = self.walk_frames_r[self.bunny][self.current_frame]
                else:
                    self.surf = self.walk_frames_l[self.bunny][self.current_frame]
                self.rect = self.surf.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if (not self.jumping and not self.walking):
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames[self.bunny])
                bottom = self.rect.bottom
                self.surf = self.standing_frames[self.bunny][self.current_frame]
                self.rect = self.surf.get_rect()
                self.rect.bottom = bottom
                
        # show jump image
        if self.jumping:
            self.surf = self.jump_frame[self.bunny]
        self.mask = pygame.mask.from_surface(self.surf)
        if self.wing or self.boost:
            self.surf = self.jump_frame[self.bunny]
    def move(self):
        
        if self.vel.y > -0.2 and self.vel.y < 0.2:
            self.boost = False
            if self.power_was_boost == True:
                self.power = False
                self.powhit = False
                self.power_was_boost = False
                self.power_once = 0
            
        
            
            
        self.animate()
        #wing power
        if self.wing == False:
            self.acc = vec(0,0.5)
        else:
            self.acc = vec(0,-0.5)
            
            if self.wing_updated == False:
                self.now_wing = pygame.time.get_ticks() - tdg
                self.wing_updated = True
        if self.wing:
            if (pygame.time.get_ticks() - self.now_wing - tdg) >= self.wing_time:
                self.wing = False
                self.wing_updated = False
                self.powhit = False
                self.power_once = 0
                self.power = False
                self.acc = vec(0,0.5)
        if self.shield == True:
            if self.shield_updated == False:
                self.now_shield = pygame.time.get_ticks() - tdg
                self.shield_updated = True    
            if (pygame.time.get_ticks() - self.now_shield - tdg) >= self.shield_time:
                self.shield = False
                self.shield_updated = False
                self.power = False
                self.powhit = False
                self.power_once = 0
                
        
            
    
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            
           self.boost = False
           self.jumping = True
           self.vel.y = -15
           if P1.bunny == 0:
                jump_sound.play()
           else:
                jump_sound_fem.play()
           
 
    def cancel_jump(self):
        if self.jumping and self.boost == False and self.wing == False:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        
        
        if self.vel.y > 0: 
            hits = pygame.sprite.spritecollide(self ,platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.pos.y < lowest.rect.bottom: 
                    if self.pos.x < lowest.rect.right + 10 and \
                    self.pos.x > lowest.rect.left - 10:
                        
                        self.pos.y = lowest.rect.top +1
                        self.vel.y = 0
                        self.jumping = False
                        for i in self.broken_list:
                            if lowest.choice == i:
                                lowest.death_time -= FPS
                                if lowest.death_time <= 0:
                                    lowest.kill()
                                    plat_gen()
                                    for d in range(random.randrange(6,10)):
                                        p = Particle((random.randint(lowest.rect.left,lowest.rect.right),
                                                  random.randint(lowest.rect.top, lowest.rect.bottom)),i)
                                        all_sprites.add(p)
                            else:
                                continue
                            break
               
class COINS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = Prop_layer
        self.pos = vec(random.randint(40,WIDTH-40),random.randint(-HEIGHT * 3,-30))
        self.type = random.choice(['silver','gold','bronze','bronze','bronze'
                                   ,'bronze','bronze','bronze','silver','silver'])
        self.lastan = 6
        self.cf = 0
        ss = Spritesheet('img/spritesheet_jumper.png')
        gold = [ss.get_image(698, 1931, 84, 84),
                ss.get_image(829, 0, 66, 84),
                ss.get_image(897, 1574, 50, 84),
                ss.get_image(645, 651, 15, 84),
                pygame.transform.flip(ss.get_image(897, 1574, 50, 84),True,False),
                pygame.transform.flip(ss.get_image(829, 0, 66, 84),True,False)]
        silver = [ss.get_image(584,406,84,84),
                  ss.get_image(852,1003,66,84),
                  ss.get_image(899,1219,50,84),
                  ss.get_image(662,651,14,84),
                  pygame.transform.flip(ss.get_image(899,1219,50,84),True,False),
                  pygame.transform.flip(ss.get_image(852,1003,66,84),True,False)]
        bronze = [ss.get_image(707,296,84,84),
                  ss.get_image(826,206,66,84),
                  ss.get_image(899,116,50,84),
                  ss.get_image(670,406,14,84),
                  pygame.transform.flip(ss.get_image(899,116,50,84),True,False),
                  pygame.transform.flip(ss.get_image(826,206,66,84),True,False)]
        self.images = {'gold':gold,
                       'silver':silver,
                       'bronze':bronze}
        self.plus = {'gold':50,
                     'silver': 30,
                     'bronze': 10}
        self.surf = self.images[self.type][self.cf]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
        self.time = 100
        self.last_update = pygame.time.get_ticks() - tdg
        
    def animate(self):
        if pygame.time.get_ticks() - tdg - self.last_update > self.time:
            self.cf += 1
            self.cf = self.cf % 6
            self.last_update = pygame.time.get_ticks() - tdg
            
    def move(self):
        self.animate()
        self.surf = self.images[self.type][self.cf]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
        hits = pygame.sprite.collide_rect(P1,self)
        if hits:
            P1.score += self.plus[self.type]
            self.kill()

class Carrot(pygame.sprite.Sprite):
    def __init__(self,ctype):
        super().__init__()
        self._layer = Prop_layer
        self.ss = Spritesheet('img/spritesheet_jumper.png')
        self.carrots = {'gold':self.ss.get_image(814,1661,78,70),
                        'normal': self.ss.get_image(820,1733,78,70)}
        self.surf = self.carrots[ctype]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.pos = vec(random.randint(40,WIDTH-40),random.randint(-HEIGHT * 3,-30))
        self.rect.center = self.pos
        self.ctype = ctype 
        
    def move(self):
        self.rect.center = self.pos
        hits = pygame.sprite.collide_rect(P1,self)
        if hits:
            if self.ctype == 'gold':
                if random.randint(1,100) <= 70:
                    P1.lives += 1
                    
            else:
                if random.randint(1,100) <= 20:
                    P1.lives += 1
                   
            self.kill()
            
        
class platformdetail(pygame.sprite.Sprite):
    def __init__(self,choice,p,excp = 'n'):
        super().__init__()
        self._layer = PLATFORMD_LAYER
        self.ss = Spritesheet('img/spritesheet_jumper.png')
        self.mushroom = {'big': self.ss.get_image(812, 453, 81,99),
                         'small': self.ss.get_image(814,1574,81,85)}
        self.cactus = {'big':self.ss.get_image(707,134,117,160),
                       'small':self.ss.get_image(707,134,117,160)}
        self.nograss = [12,13,14,15,4,5,6,7]
        self.greengrass = [0,1,2,3]
        if choice in self.nograss:
            self.grass = random.choice([self.mushroom,self.cactus])
        elif choice in self.greengrass:
            self.grass = {'big':self.ss.get_image(784,1931,82,70),
                          'small': self.ss.get_image(868,1877,58,57)}
        else:
            self.grass = {'big':self.ss.get_image(801,752,82,70),
                          'small': self.ss.get_image(534,1063,58,57)}
        self.choice = choice % 4
        if self.choice == 0 or self.choice == 2:
            self.type = 'big'
        else:
            self.type = 'small'
        self.nomchoice = [0,1,2]
        self.excp = {'m':0,"c":1,'g':2}
        self.e = {0:'m',1:'c',2:'g'}
        if excp != 'n':
            self.nomchoice.remove(self.excp[excp])
        self.images = [self.mushroom[self.type],self.cactus[self.type],self.grass[self.type]]
        self.nom = random.choice(self.nomchoice)
        self.surf = self.images[self.nom]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.p = p
        self.coffset = random.randrange(-4,5)
        self.exoffset = random.randrange(2,6)
        self.rect.center = (50,-HEIGHT)
    def move(self):
        if not platforms.has(self.p):
            self.kill()
        if self.nom == 0:
            self.rect.bottom = self.p.rect.top + 1
            self.rect.centerx = self.p.rect.centerx + self.coffset
        elif self.nom == 2:
            self.rect.bottom = self.p.rect.top + 1
            self.rect.left = self.p.rect.left + self.exoffset
        else:
            self.rect.bottom = self.p.rect.top + 1
            self.rect.right = self.p.rect.right - self.exoffset
            
class spikes(pygame.sprite.Sprite):
    def __init__(self,p,choice):
        super().__init__()
        self._layer = MOB_LAYER
        self.p = p
        self.nom = random.choice([0,1,2])
        self.up = random.choice([True,False])
        self.s = Spritesheet('img/spritesheet_jumper.png')
        self.images = {0:{True:self.s.get_image(232,1390,95,53),
                          False:self.s.get_image(147,1988,95,53)},
                       1:{True:self.s.get_image(885,752,51,87),
                          False:self.s.get_image(894,206,51,87)}}
        self.surf = self.images[(choice % 2)][self.up]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.coffset = random.randrange(-4,5)
        self.exoffset = random.randrange(5,10)
        self.choice = choice
        
    def move(self):
        if not platforms.has(self.p):
            self.kill()
        if self.nom == 0:
            if self.up:
                self.rect.bottom = self.p.rect.top + 1
                self.rect.centerx = self.p.rect.centerx + self.coffset
            else:
                self.rect.top = self.p.rect.bottom - 1
                self.rect.centerx = self.p.rect.centerx + self.coffset
        elif self.nom == 2:
            if self.up:
                self.rect.bottom = self.p.rect.top + 1
                self.rect.left = self.p.rect.left + self.exoffset
            else:
                self.rect.top = self.p.rect.bottom - 1
                self.rect.left = self.p.rect.left + self.exoffset
        else:
            if self.up:
                self.rect.bottom = self.p.rect.top + 1
                self.rect.right = self.p.rect.right - self.exoffset
            else:
                self.rect.top = self.p.rect.bottom - 1
                self.rect.right = self.p.rect.right - self.exoffset
        
        
class platform(pygame.sprite.Sprite):
    def __init__(self,bool1):
        super().__init__()
        self._layer = PLATFORM_LAYER
        self.trapped= False
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        #[big,small,big_broken,small_broken]
        self.images = [self.spritesheet.get_image(0, 288, 380, 94),self.spritesheet.get_image(213, 1662, 201, 100),
                       self.spritesheet.get_image(0, 384, 380, 94),self.spritesheet.get_image(382, 204,200, 100),
                       self.spritesheet.get_image(0, 576, 380, 94),self.spritesheet.get_image(218, 1456, 201, 100),
                       self.spritesheet.get_image(0, 0, 380, 94),self.spritesheet.get_image(262, 1152,201, 100),
                       self.spritesheet.get_image(0, 672, 380, 94),self.spritesheet.get_image(208, 1879, 201, 100),
                       self.spritesheet.get_image(0, 1056, 380, 94),self.spritesheet.get_image(382, 102,200, 100),
                       self.spritesheet.get_image(0, 96, 380, 94),self.spritesheet.get_image(382, 408, 200, 100),
                       self.spritesheet.get_image(0, 192, 380, 94),self.spritesheet.get_image(232, 1288,200, 100),
                       self.spritesheet.get_image(0, 960, 380, 94),self.spritesheet.get_image(218, 1558, 200, 100),
                       self.spritesheet.get_image(0, 864, 380, 94),self.spritesheet.get_image(382, 0,200, 100),
                       self.spritesheet.get_image(0, 768, 380, 94),self.spritesheet.get_image(213, 1764, 201, 100),
                       self.spritesheet.get_image(0, 480, 380, 94),self.spritesheet.get_image(382, 306,200, 100),]
        if bool1 == True:
            self.choice = random.choice([platform_type[plat_type] ,platform_type[plat_type]+3,platform_type[plat_type],platform_type[plat_type],
                                     platform_type[plat_type]+1,platform_type[plat_type]+1,platform_type[plat_type]+2] )
        else:
            self.choice = random.choice([platform_type[plat_type],platform_type[plat_type]+1])
        self.surf = self.images[self.choice]
        self.rect = self.surf.get_rect(center = (random.randint(self.surf.get_width()+2,WIDTH - self.surf.get_width() - 2),
                                           random.randint(0, HEIGHT-50))) 
        self.surf.set_colorkey(BLACK)
        
        self.mask = pygame.mask.from_surface(self.surf)
        self.death_time = random.randrange(2150,2750)
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
                     
class spikeman(pygame.sprite.Sprite):
    def __init__(self,pos,xlow,xup,platform):
        super().__init__()
        self._layer = MOB_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.surf = self.spritesheet.get_image(814,1417,90,155)
        self.surf.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.surf)
        self.vel = vec(0,0)
        self.rect = self.surf.get_rect()
        self.rect.midbottom = pos[0],pos[1] + 1
        self.jumping = False
        self.walking = False
        self.llimit = xlow
        self.ulimit = xup
        self.cf = 0
        self.last_update = 0
        self.walk_l = False
        self.walk_r = False
        self.standu = 0
        #check
        self.standing = False
        self.speed = random.randrange(1,4)
        self.accy = 0
        self.to_do_once = 0
        self.walkdone = False
        self.standone = False
        self.jumpdone = False
        self.walk_type = 1
        self.walk_list = [self.walk_l,self.walk_r]
        self.plat = platform
        self.didonce = 0
        self.loadonce = 0
        
    def load_images(self):
        self.walkr = [self.spritesheet.get_image(704,1256,120,159),
                      self.spritesheet.get_image(812,296,90,155)]
        self.walkl = []
        
        for i in self.walkr:
             self.walkl.append(pygame.transform.flip(i, True , False))
             i.set_colorkey(BLACK)
        for i in self.walkl:
            i.set_colorkey(BLACK)
            
        self.jump = self.spritesheet.get_image(736,1063,114,155)
        self.jump.set_colorkey(BLACK)
        
        self.stand = self.spritesheet.get_image(814,1417,90,155)
        self.stand.set_colorkey(BLACK)
        
    def animate(self):
        if self.loadonce == 0:
            self.load_images()
            self.loadonce += 1
        if self.walking == False and self.jumping == False and self.standing:
            self.surf = self.stand
        if self.jumping or self.vel.y < -1 and not self.walking and not self.standing:
            self.surf = self.jump
        if self.walking and not self.jumping and not self.standing:
            if self.vel.x > 0:
                self.surf = self.walkr[self.cf]
                if pygame.time.get_ticks() - tdg - self.last_update >= 180:
                    self.cf = (self.cf + 1) % 2
                    self.last_update = pygame.time.get_ticks() - tdg
            elif self.vel.x < 0:
                self.surf = self.walkl[self.cf]
                if pygame.time.get_ticks() - tdg - self.last_update >= 180:
                    self.cf = (self.cf + 1) % 2
                    self.last_update = pygame.time.get_ticks() - tdg
        self.mask = pygame.mask.from_surface(self.surf)
                    
    
    def move(self):
        self.animate()
        self.update()
        if self.walking:
            self.vel.y = 0
            if self.walk_r:
                self.vel.x = self.speed
                if self.rect.right > self.ulimit - 2:
                    self.walkdone = True
            elif self.walk_l:
                self.vel.x = -self.speed
                if self.rect.left < self.llimit + 2:
                    self.walkdone = True 
        if self.standing:
            self.vel.x = 0
            self.vel.y = 0
            if pygame.time.get_ticks() - tdg - self.standu > random.choice([2000,3000,4000]):
                self.standone = True
        if self.jumping:
            if self.didonce == 0:
                self.didonce+= 1
                self.vel.y = -10
                self.accy = 0.5
            if self.vel.y >= 8:
                self.jumpdone = True
                self.vel.y = 0
                self.accy = 0
                self.didonce = 0
        self.rect.y += self.vel.y
        self.rect.x += self.vel.x
        self.vel.y += self.accy
        if not self.jumping:
            self.rect.bottom = self.plat.rect.top + 1
        if not platforms.has(self.plat):
            self.kill()
        
        
        
    def update(self):
        if self.to_do_once == 0:
            self.walking = True
            self.standing = False
            self.jumping = False
            self.walk_list[self.walk_type] = True
            self.walk_type = (self.walk_type + 1) % 2
            self.standu = pygame.time.get_ticks() - tdg
            self.to_do_once += 1
        if self.walkdone:
            self.standing = True
            self.walking = False
            self.jumping = False
            self.walkdone = False
            self.walk_r = False
            self.walk_l = False
            self.walk_list = self.walk_l,self.walk_r
            self.standu = pygame.time.get_ticks() - tdg
        if self.standone:
            self.walking = False
            self.standing = False
            self.standone = False
            self.jumping = True
        if self.jumpdone:
            self.jumpdone = False
            self.jumping = False
            self.standing = False
            self.walking = True
            self.walk_list[self.walk_type] = True
            self.walk_type = (self.walk_type + 1) % 2
        self.walk_l,self.walk_r = self.walk_list
        self.walk_list = [self.walk_l,self.walk_r]

class Jump_dude(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = MOB_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        
class Mob_fly_man(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = MOB_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.image_up = self.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)
        self.image_dead = self.spritesheet.get_image(698, 1801, 120, 128)
        self.surf = self.image_up
        self.rect = self.surf.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT // 2)
        self.vy = 0
        self.dy = 0.5

    def move(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.surf = self.image_up
        else:
            self.surf = self.image_down
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()                    
        
class lifeshow(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self._layer = PLATFORM_LAYER
        self.surf = life_img
        self.rect = self.surf.get_rect()
        self.pos = pos
        self.rect.topleft = self.pos
    def move(self):
        self.rect.topleft= self.pos
        
class Fly_dude(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = MOB_LAYER
        self.spritesheet = Spritesheet('img/spritesheet_jumper.png')
        self.images = [spritesheet.get_image(382,635,174,126),
                       spritesheet.get_image(0,1879,206,107),
                       spritesheet.get_image(0,1559,216,101),
                       spritesheet.get_image(0,1456,216,101),
                       spritesheet.get_image(382,510,182,123),
                       spritesheet.get_image(0,1456,216,101),
                       spritesheet.get_image(0,1559,216,101),
                       spritesheet.get_image(0,1879,206,107)]
        self.img_type = 0
        self.img_l = len(self.images) - 1
        self.surf = self.images[self.img_type]
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.last_update = pygame.time.get_ticks() - tdg
        self.delta_t = 200
        self.rect.center = random.randrange(20,WIDTH - 20),random.randrange(HEIGHT + 50,HEIGHT + 101)
        self.speedx = random.randrange(-2,3)
        self.speedy = random.randint(-4,0)
        self.center = self.rect.center
    def animate(self):
        self.center = self.rect.center
        if pygame.time.get_ticks() -tdg - self.last_update >= self.delta_t:
            self.last_update = pygame.time.get_ticks() - tdg
            self.img_type = (self.img_type + 1) % self.img_l
            self.surf = self.images[self.img_type]
            self.surf.set_colorkey(BLACK)
            self.rect = self.surf.get_rect()
            self.mask = pygame.mask.from_surface(self.surf)
        
    def move(self):
        self.animate()
        self.rect.center = self.center
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
        if self.rect.bottom <= 0:
            self.kill()
        self.speedx = random.randrange(-2,3)
        self.speedy = random.randint(-4,0)
        
def plat_gen():
    global plat_type
    plat_type = random.choice(['grass','cake','sand','stone','wood','snow'])
    platlist = platforms.sprites()
    highest = platlist[0]
    has_spikedude = False
    for plat in platforms:
        if plat.rect.top < highest.rect.top:
            highest = plat
        
    
    width = random.randrange(50,100)
    p  = platform(True)      
    
     
    
         
    p.rect.center = (random.randrange(0 + width, WIDTH - width),
                     random.randrange(highest.rect.centery - 100 , highest.rect.centery - 70 ))
         
    platforms.add(p)
    all_sprites.add(p)
    if random.randrange(100) < POW_SPAWN_PCT:
        po = Pow(p)
        all_sprites.add(po)
        powerups.add(po)
    if p.choice % 4 == 2 or p.choice % 4 == 0:
        if random.randrange(1,100) < SPIKEMAN_PCT and p.speed == 0:
            se = spikeman(p.rect.midtop, p.rect.left, p.rect.right,p)
            all_sprites.add(se)
            spikeman_g.add(se)
            has_spikedude = True
            p.trapped = True
    p_det = platformdetail (p.choice, p)
    all_sprites.add(p_det)
    plat_detail.add(p_det)
    if random.randint(1,100) < 50 and p.choice % 4 != 1 and p.choice % 4 != 3:
        pdet = platformdetail(p.choice,p,p_det.e[p_det.nom])
        all_sprites.add(pdet)
        plat_detail.add(pdet)
    if not has_spikedude and random.randint(1,100) < 12:
        s = spikes(p, p.choice)
        spike_g.add(s)
        all_sprites.add(s)
        p.trapped = True
        
if __name__ == '__main__':
    if(not path.exists("hiscore.txt")):
        with open("hiscore.txt", "wb") as f:
            f.write(codecs.encode(b'4010','base64','strict'))
            
    try:
        with open("hiscore.txt", "rb") as f:
            hiscor = f.read()
            hiscore = int(codecs.decode(hiscor,'base64','strict'))
            
            
    except:
        with open("hiscore.txt", "wb") as f:
            f.write(codecs.encode(b'52006','base64','strict'))
        with open("hiscore.txt", "rb") as f:
            hiscor = f.read()
            hiscore = int(codecs.decode(hiscor,'base64','strict'))
    spritesheet = Spritesheet('img/spritesheet_jumper.png')
    life_img = spritesheet.get_image(868, 1936, 52, 71)
    life_img.set_colorkey(BLACK)
    pygame.display.set_icon(life_img)

    #groups define
    all_sprites = pygame.sprite.LayeredUpdates()
    clouds = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    mobs_fly_man = pygame.sprite.Group()
    prop_g = pygame.sprite.Group()
    fireball_g = pygame.sprite.Group()
    sun_g = pygame.sprite.Group()
    cloud_g = pygame.sprite.Group()
    l_g = pygame.sprite.Group()
    spikeman_g = pygame.sprite.Group()
    flydude_g = pygame.sprite.Group()
    plat_detail = pygame.sprite.Group()
    spike_g = pygame.sprite.Group()
    coin_g = pygame.sprite.Group()
    carrot_g = pygame.sprite.Group()
    lifeshow_g = pygame.sprite.Group()
    snow_g = []
    rain_g = []
    circ_g = []
    #list containing bg_img
    bg_list = [SUM_BG,WIN_BG,RAI_BG]
    ses_list = ['summer','winter','rainy']
    #bg img making
    for i in range(3):
        bg_img(bg_list[i], ses_list[i])
    #start screen
    show_start_screen(hiscore)
    #game loop season
    season_var = 0
    season_updated = 0
    bgsurf = background(SUM_BG)
    #game over and game loop
    pygame.mixer.music.load(path.join(snd_dir, 'Happy_Tune.ogg'))
    pygame.mixer.music.set_volume(2.00)
    pygame.mixer.music.play(loops=-1)
    while True:
        player_dead = False
        PT1 = platform(False)
        
        P1 = Player()
        PT1.moving = False
        
        #starting point
        
        PT1.surf = PT1.images[platform_type[plat_type]]
        PT1.surf.set_colorkey(BLACK)
        PT1.rect = PT1.surf.get_rect(center = (70, HEIGHT - 30))
       
        
        all_sprites.add(PT1)
        all_sprites.add(P1)
        
        
        platforms.add(PT1)
        p_det = platformdetail (PT1.choice, PT1)
        all_sprites.add(p_det)
        plat_detail.add(p_det)
        if random.randint(1,100) < 50 and PT1.choice % 4 != 1 and PT1.choice % 4 != 3:
            pdet = platformdetail(PT1.choice,PT1,p_det.e[p_det.nom])
            all_sprites.add(pdet)
            plat_detail.add(pdet)
        for i in range(8):
            # c = Cloud(random.choice([True,False]))
            c = Cloud([False])
            c.rect.y += (HEIGHT * 5//6)
            clouds.add(c)
            all_sprites.add(c)
        
        #cloud dead
        for entity in clouds:
            if entity.rect.y > HEIGHT or entity.rect.left > WIDTH or entity.rect.right<0:
                entity.kill()
        # starting blocks!
        init_plat_y = random.randint(-100, -70)
        for x in range(random.randint(5,6)):
            plat_type = random.choice(['grass','cake','sand','stone','wood','snow'])
            init_plat_y_offset = random.randint(-100,-70)
            width = random.randrange(50,100)
            p  = platform(True)      
           
             
            
            
            p.rect.center = (random.randrange(0, WIDTH - width),
                             HEIGHT + init_plat_y)
             
            platforms.add(p)
            all_sprites.add(p)
            if random.randrange(100) < POW_SPAWN_PCT:
                po = Pow(p)
                all_sprites.add(po)
                powerups.add(po)
            init_plat_y += init_plat_y_offset
            p_det = platformdetail (p.choice, p)
            all_sprites.add(p_det)
            plat_detail.add(p_det)
            if random.randint(1,100) < 50 and p.choice % 4 != 1 and p.choice % 4 != 3:
                pdet = platformdetail(p.choice,p,p_det.e[p_det.nom])
                all_sprites.add(pdet)
                plat_detail.add(pdet)
         
         #actual game loop
        while True:
            if pygame.time.get_ticks() - season_updated - tdg >= 30000:
                season_var = (season_var + 1) % 3
                ses_type = ses_list[season_var]
                season_updated = pygame.time.get_ticks() -  tdg
                bgsurf = background(season_list[season_var])
            #update func of player class
            P1.update()
            if P1.lives > 5:
                P1.lives = 5 
            #sun
            if len(sun_g) == 0 and ses_type != 'rainy':
                Sun = sun(P1)
                all_sprites.add(Sun)
                sun_g.add(Sun)
            #dcloud
            if len(cloud_g) == 0 and ses_type == 'rainy':
                d = Dangercloud()
                cloud_g.add(d)
                all_sprites.add(d)
                
            #handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        P1.jump()
                        
                if event.type == pygame.KEYUP:    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        P1.cancel_jump()  
            # getting killed         
            if (P1.rect.bottom > HEIGHT + P1.surf.get_height()//5 or player_dead == True) and P1.lives == 0:  
                pygame.mixer.music.fadeout(500)
                displaysurface.blit(bgsurf,(0,0))
                P1.surf = P1.dead_frame[P1.bunny]
                
                for entity in all_sprites:
                   
                    displaysurface.blit(entity.surf, entity.rect)
                    pygame.display.update()
                
                for s in snow_g:
                    s.draw()
                
                for s in rain_g:
                    s.draw()
                for e in fireball_g:
                    e.update()
                pygame.display.update()
                pygame.time.wait(1000)
                for entity in all_sprites:
                    entity.kill()
                circ_g.clear()
                snow_g.clear()
                rain_g.clear()
                
                for i in fireball_g:
                    i.kill()
                game_over_screen(P1, hiscore)
                
                break
            elif P1.rect.bottom > HEIGHT + P1.surf.get_height()//5 or player_dead == True:
                P1.lives -= 1
                P1.shield = False
                P1.boost = False
                P1.powhit = False
                P1.power = False
                displaysurface.blit(bgsurf,(0,0))
                P1.surf = P1.dead_frame[P1.bunny]
                
                for entity in all_sprites:
                   
                    displaysurface.blit(entity.surf, entity.rect)
                    pygame.display.update()
                
                for s in snow_g:
                    s.draw()
                
                for s in rain_g:
                    s.draw()
                for e in fireball_g:
                    e.update()
                pygame.display.update()
                pygame.time.wait(500)
                
                for i in prop_g:
                    i.kill()
                P1.vel = vec(0,0)
                player_dead = False
                P1.wing = True
                P1.power = True
                P1.powhit = True
                lowest = 0
                for i in platforms:
                    if not i.trapped:
                        lowest = i
                        break
                for i in platforms:
                    if i.rect.centery > lowest.rect.centery and not i.trapped:
                        lowest = i
                P1.pos = vec(lowest.rect.centerx,lowest.rect.top + 1)
            
            #power collisions
            if P1.powhit == False:
                
                hits = pygame.sprite.spritecollide(P1, powerups, True)
                for power in hits:
                    P1.powhit = True
                    boost_sound.play()
                    if power.type == 'random':
                       power.type = random.choice(['boost','wings','life','shield']) 
                    if power.type == 'boost':
                        P1.vel.y = - BOOST_POW
                        P1.jumping = False
                        P1.boost = True
                        P1.power_was_boost = True
                        P1.power = True
                    elif power.type == 'wings':
                        P1.wing = True
                        P1.power = True
                        
                        
                    elif power.type == 'life':
                        P1.bunny = (P1.bunny + 1) % 2
                        P1.powhit = False
                    elif power.type == 'shield':                        
                        P1.power = True
                        P1.shield = True
                    
            #Power related props for P1
            if P1.power == True and P1.power_once == 0:
                for i in prop_g:
                    i.kill()
                if P1.shield == True:
                    p = Props(P1, 2, 0)
                    prop_g.add(p)
                    all_sprites.add(p)
                if P1.wing == True:
                     p1 = Props(P1,0,0)
                     p2 = Props(P1,0,1)
                     all_sprites.add(p1)
                     all_sprites.add(p2)
                     
                if P1.boost == True:
                    p = Props(P1,1,0)
                    p1 = Props(P1,1,1)
                    all_sprites.add(p)
                    all_sprites.add(p1)
                P1.power_once += 1
                
            #snow
            if ses_type == 'winter' and len(snow_g) < 300:
                s = Snow()
                snow_g.append(s)
                
            #rain
            if ses_type == 'rainy' and len(rain_g) < 450:
                r = Rain()
                rain_g.append(r)
            
            #coins
            if len(coin_g)< 6 and random.randint(0,200) < 10:
                    c = COINS()
                    all_sprites.add(c)
                    coin_g.add(c)
                    
            
            #fireball

            for i in fireball_g:
                i.update()
                    
            
            #broken platform
        
            for p in particles:
                p.move()
                p.draw()
            
            #kill lifeshow
            for i in lifeshow_g:
                i.kill()
            #lifeshow
            for i in range(P1.lives):
                offset = (life_img.get_width() + 5) * i
                s = lifeshow((5 + offset,5))
                all_sprites.add(s)
                lifeshow_g.add(s)
                    
            if P1.shield:
                hits = pygame.sprite.groupcollide(mobs_fly_man,prop_g, True, False)
            
            if P1.shield:
                hits = pygame.sprite.groupcollide(flydude_g,prop_g, True, False)
                
                    
                
            #Enemies - Fly Man
            now = pygame.time.get_ticks() - tdg
            if now - mob_fly_man_timer > 5000 + random.choice([-1000,-500,0,500,1000]) and len(mobs_fly_man) < 2:
                mob_fly_man_timer = now
                m = Mob_fly_man()
                all_sprites.add(m)
                mobs_fly_man.add(m)
            #Fly dude
            now = pygame.time.get_ticks() - tdg
            if now - mob_fly_man_timer2 > 13000 + random.choice([-1000,-500,0,500,1000]) and len(flydude_g) < 2:
                mob_fly_man_timer2 = now
                m = Fly_dude()
                all_sprites.add(m)
                flydude_g.add(m)
            
            #spike hits
            hits = pygame.sprite.spritecollide(P1,spike_g,False)
            if hits and not P1.wing and not P1.boost:
                hits = pygame.sprite.spritecollide(P1,spike_g,False,pygame.sprite.collide_mask)
                if hits:
                    player_dead = True
                    continue
                
            #mob - fly man hits
            if not P1.shield and not P1.wing:
                mob_fly_man_hits = pygame.sprite.spritecollide(P1,mobs_fly_man, False)
                if mob_fly_man_hits:
                    mob_fly_man_hits = pygame.sprite.spritecollide(P1,mobs_fly_man, False,pygame.sprite.collide_mask)
                    if mob_fly_man_hits:
                        player_dead = True
                        continue
                    
            #flydude hit
            if not P1.wing and len(flydude_g) < 3 and not P1.shield:
                hit = pygame.sprite.spritecollide(P1,flydude_g,False)
                if hit:
                    hit = pygame.sprite.spritecollide(P1,flydude_g,False,pygame.sprite.collide_mask)
                    if hit: 
                        player_dead = True
                        continue
            
            #spikeman hits
            if not P1.wing and not P1.boost:
                hits = pygame.sprite.spritecollide(P1 , spikeman_g, False)
                if hits:
                    hits = pygame.sprite.spritecollide(P1,spikeman_g,False,pygame.sprite.collide_mask)
                    if hits:
                        player_dead = True
                        continue            
                    
            #Scroll!
            
            if P1.rect.top <= HEIGHT / 3:
                #clouds
                if random.randrange(100) < 15:
                    Cloud(random.choice([True,False]))
                    c = Cloud(False)
                    clouds.add(c)
                    all_sprites.add(c)
                
                # normal carrots
                if random.randint(1,500) < 2 and len(carrot_g) < 1:
                    c = Carrot('normal')
                    all_sprites.add(c)
                    carrot_g.add(c)
                
                #gold carrot
                if random.randint(1,700) == 1 and len(carrot_g) < 1:
                    c = Carrot('gold')
                    all_sprites.add(c)
                    carrot_g.add(c)
                P1.pos.y += max(abs(P1.vel.y),2)
                for cloud in clouds:
                    cloud.rect.y += max(abs(P1.vel.y//2),1)
                    if cloud.rect.top >= HEIGHT:
                        cloud.kill()
                for powers in powerups:
                    powers.rect.y += max(abs(P1.vel.y),2)
                    if powers.rect.top >= HEIGHT - 20:
                        powers.kill()
                for plat in platforms:
                    plat.rect.y += max(abs(P1.vel.y),2)
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
                        P1.score += 10
                        plat_gen()
                for particle in particles:
                    particle.rect.y += abs(P1.vel.y)
                    if particle.rect.top >= HEIGHT:
                        particle.kill()
                for i in plat_detail:
                    i.rect.y += abs(P1.vel.y)
          
                for i in spikeman_g:
                    i.rect.y += abs(P1.vel.y)
                    if i.rect.top >= HEIGHT:
                        i.kill()
                for i in coin_g:
                    i.pos.y += abs(P1.vel.y)
                    if i.rect.top > HEIGHT:
                        i.kill()
                for s in snow_g:
                    s.y += abs(P1.vel.y)
                for r in rain_g:
                    r.y += abs(P1.vel.y)

                for i in cloud_g:
                    i.rect.y += abs(P1.vel.y)
                for i in carrot_g:
                    i.pos.y += abs(P1.vel.y)
                    
                for c in circ_g:
                    c.pos[1] += abs(P1.vel.y)
                    if c.pos[1] > HEIGHT + (c.radius/2):
                        circ_g.remove(c)
                for i in mobs_fly_man:
                    i.rect.y += abs(P1.vel.y)
            
                for i in l_g:
                    i.rect.y += abs(P1.vel.y)
                for i in spike_g:
                    i.rect.y += abs(P1.vel.y)
                for i in flydude_g:
                    i.rect.centery += abs(P1.vel.y)
                # for i in fireball_g:
                #     i.rect.y += abs(P1.vel.y)
                #     i.target[1] += abs(P1.vel.y)
                #     if i.rect.top >= HEIGHT:
                #         i.kill()
           
            displaysurface.blit(bgsurf,(0,0))
            scorefont = pygame.font.SysFont("Verdana", 20)     
            scoresurf  = scorefont.render(str(P1.score), True, (85,107,47))   
            displaysurface.blit(scoresurf, (WIDTH/2, 10))   
            #snow blitting
            if len(snow_g) != 0:
                for s in snow_g:
                    s.move()
            #rain blitting
            if len(rain_g) != 0:
                for s in rain_g:
                    s.move()
            
            #fireball blitting
            if len(fireball_g) != 0:
                for i in fireball_g:
                    displaysurface.blit(i.surf, i.rect)
            #all entity
            for entity in all_sprites:
                displaysurface.blit(entity.surf, entity.rect)
                entity.move()
            
            #circle effect
            if len(circ_g) != 0:
                for i in circ_g:
                    i.update()
         
            pygame.display.update()
            FramePerSec.tick(FPS)
            if int(hiscore)<P1.score:
                New_high_score = True
                hiscore = str(P1.score).encode('utf8')
                with open("hiscore.txt", "wb") as f:
                    f.write(codecs.encode(hiscore,'base64','strict'))