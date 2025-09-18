# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:27:16 2022

@author: Goutam
"""
import pygame,random,sys, math
from pygame.locals import*

WIDTH = 1080
HEIGHT = 720
FPS = 60

pygame.display.set_caption('warp_field')
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,0,255)
RED = (255,0,0)
BLUE = (0,255,0)

#other vars
star_num = 600
Clock = pygame.time.Clock()


#functions
def ratio_translate(num,r1,r2,r3,r4):
    
    new_r = ((num/r2-r1) * (r4-r3)) + r3
    return new_r

#classes
class Stars():
    def __init__(self):
        self.x = random.randint(-WIDTH//2,WIDTH//2)
        self.y = random.randint(-HEIGHT,HEIGHT)
        self.z = random.randint(1, WIDTH)
        self.radius = 0
        self.pz = self.z 
        self.colour = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.ax+WIDTH/2,self.ay+HEIGHT/2), self.radius)
        pygame.draw.line(screen, self.colour, (self.ax+WIDTH/2,self.ay+HEIGHT/2),(ratio_translate(self.x/self.pz, 0, 1, 0, WIDTH)+WIDTH/2,ratio_translate(self.y/self.pz, 0, 1, 0, HEIGHT)+HEIGHT/2))
    def update(self,x,y):
        self.speed = ratio_translate(x,0,WIDTH,0,30)
        self.pz = self.z 
        self.z -= self.speed
        if self.z <= 0:
            self.x = random.randint(-WIDTH,WIDTH)
            self.y = random.randint(-HEIGHT,HEIGHT)
            self.z = random.randint(1, WIDTH)
            self.pz = self.z
        
        self.ax = ratio_translate(self.x/self.z, 0, 1, 0, WIDTH)
        self.ay = ratio_translate(self.y/self.z,0,1,0,HEIGHT)
        self.radius = 5 - ratio_translate(self.z, 0, WIDTH, 0, 5)
        
        
        
    
if __name__ == '__main__':
    
    stars_g = []
    
    #produce stars
    for i in range(star_num):
        s = Stars()
        stars_g.append(s)
    
    while True:
        
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
        #draw stuff 
        screen.fill(BLACK)
        for i in stars_g:
            i.update(*pygame.mouse.get_pos())
            i.draw()
        #update
        pygame.display.update()
        Clock.tick(FPS)