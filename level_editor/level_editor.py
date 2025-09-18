# -*- coding: utf-8 -*-
"""
Created on Mon May 17 21:39:00 2021

@author: Goutam
"""
import pygame
from os import environ
from os.path import join,exists
from sys import exit as exitt
import csv
import random

pygame.init()
monitor_size = [pygame.display.Info().current_w-10,pygame.display.Info().current_h-40]
screen = pygame.display.set_mode(monitor_size)
pygame.display.set_caption('Coderkani\'s level editor')
desktop = join(join(environ['USERPROFILE']), 'Desktop')
grid = []
FPS = 30
clock = pygame.time.Clock()
doonce = 0
#NON CHANGEABLE VAR
RED = (255,0,0)
ORANGE = (255,165,0)
GOLD = (255,215,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SILVER = (192,192,192)
DARKIVORY = (150,150,140)
IVORY = (255,255,240)
GHOSTWHITE = (248,248,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
MINTCREAM = (245,255,250)
GREY = (169,169,169)
DARKGREY = (128,128,128)
LIGHTGREY = (211,211,211)
TBH = 100
SW = (monitor_size[0] - 620)//32 * 32
SH = (monitor_size[1] - 100)//32 * 32
TW = monitor_size[0] - 200
ROWS = 15
COLS = 100
TILE_SIZE = 36
SPACING = 0
E_TILE = 18
OFFSET_TILE = E_TILE + SPACING
font_name = pygame.font.match_font('Halvita')
FONT_NAME = pygame.font.Font(font_name,35)
TITLE_FONT = pygame.font.Font(pygame.font.match_font('algerian'),85)
SHEET = 'tilesheet.png'
FILE_NOM = 2
BG_DIM = [1030,1030]
BG_SPACING_W= 40
BG_SPACING_H = 44
OFFSET_BG_W = BG_DIM[0] + BG_SPACING_W
OFFSET_BG_H = BG_DIM[1] + BG_SPACING_H
#changeable variables
scrollw = 0
scrollh = 0
gridwant = True
scroll_l = False
scroll_r = False
scroll_up = False
scroll_d = False
scrollhs = 1
scrollws = 1
tscrollw = 0
tscrollh = 0
tscroll_l = False
tscroll_r = False
tscroll_up = False
tscroll_d = False
tscrollws = 1
tscrollhs = 1
current_tile = - 1
current_multi_tile = [-1]
img_list = []
bg_list = []
buttons = []
data = []
text_g = []
level = 0
layernum = 1
current_layer = 1
layer_bg = []
layer_showbg = []
changed = True
Random = False
img_list_there = False
img_write_list = []
obliterate = False
bg_nom = 0
bg_file = 'bg.png'
complete_sh = 'spritesheet_complete.png'
enemy_mode = False
enemy_nom = 0
enemy_types = ['come out',
               'frog',
               'bee',
               'piranha',
               'black bee',
               'rat',
               'ladybug',
               'snail',
               'slime',
               'water snake',
               'alien']

for r in range(ROWS):
    i = [-1] * COLS
    data.append(i)


layers = {1:data}


    
    
def makerect(x,y,width,height,color,fill):
    pygame.draw.rect(screen, color, (x,y,width,height),fill)

def tiledraw(img_list):
    startiter = 0
    for i in range(20):
       x = SW - tscrollw
       y = TBH + (i*TILE_SIZE) - tscrollh
       for j in range(27):
           screen.blit(img_list[startiter],(x,y))
           makerect(x, y, TILE_SIZE, TILE_SIZE, BLACK, 1)
           x += TILE_SIZE
           startiter += 1
    
def drawgrid():
    #vertical lines
    for i in range(COLS+1):
        x = i * TILE_SIZE-scrollw
        if x < SW:
            pygame.draw.line(screen, DARKGREY, (x,100), (x,SH+100))
        
    #horizontal lines
    for i in range(ROWS + 1):
        pygame.draw.line(screen, DARKGREY, (0,i * TILE_SIZE-scrollh+100), (SW,i * TILE_SIZE-scrollh+100))
    
def draw_world(enemies):
    for i in range(layernum):
        if layer_bg[i].show: 
            for y, row in enumerate(layers[i+1]):
                for x, tile in enumerate(row):
                    if str(tile) != tile:
                        if tile > -1:
                            x1 = x * TILE_SIZE - scrollw
                            y1 = y * TILE_SIZE - scrollh
                            if x1 <= SW -32:
                                screen.blit(img_list[tile], (x1,y1+TBH))
                    else:
                        x1 = x * TILE_SIZE - scrollw
                        y1 = y * TILE_SIZE - scrollh
                        if x1 <= SW -32:
                            screen.blit(enemies[enemy_types[int(tile)]], (x1,y1+TBH))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height,scale = (TILE_SIZE,TILE_SIZE)):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, scale)
        return image

class Button:
    
    def __init__(self,font,text,width,height,x,y,cc,color = ORANGE):
        self.surf = pygame.Surface((int(width),int(height)))
        self.rect = self.surf.get_rect()
        self.color = color
        self.surf.fill(self.color)
        self.pos = (x,y)
        self.font = font
        self.text = text
        self.colour = GOLD
        self.cc = cc
        self.cc1 = False
        self.rect.topleft = self.pos
        
    def draw(self):
        if self.cc:
            if not self.cc1:
                self.surf.fill(self.color)
            else:
                self.surf.fill(self.colour)
        screen.blit(self.surf,self.pos)
        draw_text(self.text, self.font, BLACK, self.pos[0] + 5, self.pos[1] + 5)
        
    def click(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.cc1 = not self.cc1
                    action = True

        return action

class TimeText:
    def __init__(self,text,color = BLACK):
        self.time = 2000
        self.text = text
        self.font = TITLE_FONT
        self.color  = color
        self.last_update = pygame.time.get_ticks()
        
    def draw(self):
        if pygame.time.get_ticks() - self.last_update < self.time:
            draw_text(self.text, self.font, self.color, monitor_size[0]//2 - 150, monitor_size[1]//2)
        else:
            text_g.remove(self)
            
if __name__ == '__main__':

    spritesheet = Spritesheet(SHEET)
    spritesheet1 = Spritesheet(bg_file)
    spritesheet2 = Spritesheet(complete_sh)
    start_width = 0
    doneonce = False
    start_height = 0
    for i in range(20):
        start_width = 0
        start_height = i*OFFSET_TILE
        for j in range(27):
            img = spritesheet.get_image(start_width, start_height, E_TILE, E_TILE)
            img.set_colorkey(BLACK)
            img_list.append(img)
            start_width += OFFSET_TILE
    for i in range(3):
        bg_sw = 0
        bg_sh = i*(OFFSET_BG_H - 10)
        for j in range(4):
            img = spritesheet1.get_image(bg_sw,bg_sh, BG_DIM[0], BG_DIM[1],(SW,SH))
            img.set_colorkey(BLACK)
            bg_list.append(img)
            bg_sw += (OFFSET_BG_W-6)
            
    enemies = {'come out':spritesheet2.get_image(3250,650,128,128),
               'frog':spritesheet2.get_image(3380,130,128,128),
               'bee':spritesheet2.get_image(3510,130,128,128),
               'piranha':spritesheet2.get_image(3380,1690,128,128),
               'black bee':spritesheet2.get_image(3380,520,128,128),
               'rat':spritesheet2.get_image(3250,1300,128,128),
               'ladybug':spritesheet2.get_image(3250,1690,128,128),
               'snail':spritesheet2.get_image(3120,130,128,128),
               'slime':spritesheet2.get_image(3250,130,128,128),
               'water snake':spritesheet2.get_image(2990,1690,128,128),
               'alien': spritesheet2.get_image(780,1548,128,256)}
    for typo in enemies:
        enemies[typo].set_colorkey(BLACK)
    while True:
        if current_tile not in current_multi_tile and Random:
            current_multi_tile.append(current_tile)
            
        if not doneonce:
            if len(current_multi_tile) > 1:
                doneonce = not doneonce
                current_multi_tile.remove(-1)
        else:
            if len(current_multi_tile) > 1 and not Random:
                current_multi_tile.pop(1)
        if scroll_l:
            scrollw -= (4*scrollws)
        if scroll_r:
            scrollw += (4*scrollws)
        if scroll_up:
            scrollh -= (4*scrollhs)
        if scroll_d:
            scrollh += (4*scrollhs)
        if tscroll_l:
            tscrollw -= (4*tscrollws)
        if tscroll_r:
            tscrollw += (4*tscrollws)
        if tscroll_up:
            tscrollh -= (4*tscrollhs)
        if tscroll_d:
            tscrollh += (4*tscrollhs)
        if scrollw <0:
            scrollw = 0
        if scrollh < 0:
            scrollh = 0
        if scrollw > (COLS-20)* TILE_SIZE:
            scrollw = (COLS-20)* TILE_SIZE
        if scrollh > (ROWS-18)*TILE_SIZE:
            scrollh = (ROWS-18)*TILE_SIZE
        if tscrollw <0:
            tscrollw = 0
        if tscrollh < 0:
            tscrollh = 0
        if tscrollw > 14* TILE_SIZE:
            tscrollw = 14 * TILE_SIZE
        if tscrollh > 2*TILE_SIZE:
            tscrollh = 2*TILE_SIZE

        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exitt()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    scroll_up = True
                if event.key == pygame.K_s:
                    scroll_d = True
                if event.key == pygame.K_d:
                    scroll_r = True
                if event.key == pygame.K_a:
                    scroll_l = True
                if event.key == pygame.K_UP:
                    tscroll_up = True
                if event.key == pygame.K_DOWN:
                    tscroll_d = True
                if event.key == pygame.K_RIGHT:
                    tscroll_r = True
                if event.key == pygame.K_LEFT:
                    tscroll_l = True
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollws = 5
                    tscrollws = 5
                    scrollhs = 5
                    tscrollhs = 5
                if event.key == pygame.K_x:
                    level = max(level-1,0)
                if event.key == pygame.K_z:
                    level = min(level + 1,100)
 
                
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    scroll_up = False
                if event.key == pygame.K_s:
                    scroll_d = False
                if event.key == pygame.K_d:
                    scroll_r = False
                if event.key == pygame.K_a:
                    scroll_l = False
                if event.key == pygame.K_UP:
                    tscroll_up = False
                if event.key == pygame.K_DOWN:
                    tscroll_d = False
                if event.key == pygame.K_RIGHT:
                    tscroll_r = False
                if event.key == pygame.K_LEFT:
                    tscroll_l = False
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    scrollws = 1
                    tscrollws =1 
                    scrollhs = 1
                    tscrollhs = 1
                if event.key == pygame.K_q:
                    gridwant = not gridwant
                if event.key == pygame.K_b:
                    bg_nom += 1
                    bg_nom %= 13
                if event.key == pygame.K_e:
                    if not Random:
                        enemy_mode = not enemy_mode
                if event.key == pygame.K_1:
                    enemy_nom += 1
                    enemy_nom %= len(enemy_types)
        if Random:
            enemy_mode = False
                    
        #Mouse stuff
        mx,my = pygame.mouse.get_pos()
        screenx = (mx + scrollw)//TILE_SIZE
        screeny = (my + scrollh)//TILE_SIZE -3
        tx = (mx + tscrollw-SW)//TILE_SIZE
        ty = (my + tscrollh-TBH)//TILE_SIZE
        #screen check
        if mx < SW and my < SH+TBH and mx >0 and my>TBH:
            if not enemy_mode:
                if pygame.mouse.get_pressed()[0] == 1 and current_tile != -1:
                    if layers[current_layer][screeny][screenx] != current_tile:
                        if not Random:
                            layers[current_layer][screeny][screenx] = current_tile
                        elif Random and len(current_multi_tile) > 0:
                            layers[current_layer][screeny][screenx] = current_multi_tile[random.randrange(0,len(current_multi_tile))]
            else:
                if pygame.mouse.get_pressed()[0] == 1 and current_tile != -1:
                    layers[current_layer][screeny][screenx] = f'{enemy_nom}'
            if pygame.mouse.get_pressed()[2] == 1:
                layers[current_layer][screeny][screenx] = -1
        
        #tile check
        if mx < TW and my < TBH + SH and mx>SW and my > TBH:
            if pygame.mouse.get_pressed()[0] == 1:
                current_tile = (tx) + (ty*27)
            if pygame.mouse.get_pressed()[2] == 1:
                if ((tx) + (ty*27)) in current_multi_tile:
                    current_multi_tile.remove((tx) + (ty*27))
        '''BUTTONS'''
        #new button
        new_button = Button(FONT_NAME, 'New', 64, 32, 5, 10, False)
        buttons.append(new_button)
        #save button
        save_button = Button(FONT_NAME, 'Save', 64, 32, 5, 57, False)
        buttons.append(save_button)
        #layer button
        layer_button = Button(FONT_NAME, 'Layer+', 85, 32, monitor_size[0] - 240, 10, False)
        buttons.append(layer_button)
        #load button
        load_button = Button(FONT_NAME, 'Load', 64, 32, 84, 10, False)
        buttons.append(load_button)
        #fill button
        fill_button = Button(FONT_NAME, 'Fill', 50, 32, 84, 57, False )
        buttons.append(fill_button)
        #Random button
        random_button = Button(FONT_NAME, 'Random',105,32,monitor_size[0] - 240, 57, False)
        buttons.append(random_button)
        #LAYER SHOWING BUTTON
        x = TW + 20
        y = TBH + 2 + (layernum-1)*32
        if changed:
            l1 = Button(FONT_NAME,f'layer {layernum}', 100, 30, x, y, False)
            l2 = Button(FONT_NAME,'', 30, 30, x+120, y, False)
            l1.layer = layernum
            l2.layer = layernum
            l1.show = True
            buttons.append(l1)
            buttons.append(l2)
            layer_showbg.append(l2)
            layer_bg.append(l1)
            changed = False
        #BLITTING
        screen.fill(WHITE)
        # TILES
        makerect(SW,TBH,TW,SH,BLACK,0)
        makerect(SW,TBH,TW,SH,BLACK,2)
        #tilesheet
        tiledraw(img_list)
        # SCREEN
        makerect(0,TBH,SW,SH,SILVER,0)
        makerect(0,TBH,SW,SH,BLACK,2)
        #bg
        if bg_nom != 0:
            screen.blit(bg_list[bg_nom-1], (0,TBH))
        #world draw
        draw_world(enemies)
        #grid
        if gridwant:
           drawgrid()
        #current tile
        for i in current_multi_tile:
            tix = (i%27)*TILE_SIZE - tscrollw+SW
            tiy = (i- (i%27))/27*TILE_SIZE-tscrollh+TBH
            if tiy >= TBH and tix < monitor_size[0] - 200 and tix >= SW: 
                makerect(tix, tiy, TILE_SIZE, TILE_SIZE, GOLD, 2)
        
        if current_tile>-1:
            tix = (current_tile%27)*TILE_SIZE - tscrollw+SW
            tiy = (current_tile - (current_tile%27))/27*TILE_SIZE-tscrollh+TBH
            if tiy >= TBH and tix < monitor_size[0] - 200 and tix >= SW: 
                makerect(tix, tiy, TILE_SIZE, TILE_SIZE, RED, 1)
                
        
        # LAYERS
        makerect(TW,TBH,200,SH,MINTCREAM,0)
        makerect(TW,TBH,200,SH,BLACK,2)
        #TOOLBAR
        makerect(0, 0, monitor_size[0], TBH, GHOSTWHITE, 0)
        makerect(0, 0, monitor_size[0], TBH, BLACK, 2)
        
        #belowfill
        makerect(0,monitor_size[1]-3,monitor_size[0],10,GREY,0)
        #level text
        draw_text(f'level:{level}', FONT_NAME, BLACK, monitor_size[0] - 110, 5)
        #layer text
        draw_text(f'layer:{current_layer}', FONT_NAME, BLACK, monitor_size[0] - 110, 60)
        #current enemy
        draw_text('character:', FONT_NAME, BLACK, monitor_size[0] - 195, monitor_size[1] - 100)
        screen.blit(enemies[enemy_types[enemy_nom]], (monitor_size[0] - 50,monitor_size[1] - 110))
        #blitting buttons
        for i in buttons:
            i.draw()
        #BUTTON CLICKS
        # new button
        if new_button.click():
            for i in layers[current_layer]:
                for j,k in enumerate(i):
                    i[j] = -1
        
        #fill button
        if fill_button.click():
            if Random:
                for i in layers[current_layer]:
                    for j,k in enumerate(i):
                        i[j] = current_multi_tile[random.randrange(0,len(current_multi_tile))]
            else:
                for i in layers[current_layer]:
                    for j,k in enumerate(i):
                        i[j] = current_tile
                        
        # random button
        if random_button.click():
            Random = not Random
            if Random == False:
                obliterate = True
                  
        #obliterate
        if obliterate:
            current_multi_tile.clear()
            current_multi_tile.append(-1)
            doneonce = False
            obliterate = False
            
        # save button
        if save_button.click():
            for i in range(layernum):
                with open(f'level{level}{i+1}_map.csv','w',newline = '') as csvfile:
                    writing = csv.writer(csvfile, delimiter = ',')
                    for row in layers[i+1]:
                        writing.writerow(row)
            
            save_text = TimeText('SAVED',BLACK)
            save_text.last_update = pygame.time.get_ticks()
            text_g.append(save_text)
        # layer button
        if layernum <= 5:
            if layer_button.click():
                layernum += 1
                changed = True
                datacopy = data.copy()
                datacopy.clear()
                for r in range(ROWS):
                    i = [-1] * COLS
                    datacopy.append(i)
                layers[layernum] = datacopy
        #layer changing
        for i in layer_bg:
            if i.click():
                current_layer = i.layer
            if i.show:
                makerect(i.pos[0]+120, TBH+2+(i.layer-1)*32, 30, 30, GREEN, 2)
            if not i.show:
                makerect(i.pos[0]+120, TBH+2+(i.layer-1)*32, 30, 30, RED, 2)
        #layer showing
        for i in layer_showbg:
            if i.click():
                layer_bg[i.layer-1].show = not layer_bg[i.layer-1].show
        #load button
        if load_button.click():
            for i in range(layernum):
                try:
                    with open(f'level{level}{i+1}_map.csv','r',newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                layers[i+1][x][y] = int(tile)
                except Exception as e:
                    print(e)
                    loaderror_text = TimeText('ERROR IN LOADING',RED)
                    loaderror_text.last_update = pygame.time.get_ticks()
                    text_g.append(loaderror_text)
        
        
                
        #text draw
        for i in text_g:
            i.draw()
        
        
        pygame.display.update()
        clock.tick(FPS)

        
            