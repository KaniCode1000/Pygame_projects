# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import time
# 2 - Initialize the game
pygame.init()
pygame.mixer.init()


width, height = 640, 480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('castledefendbykani')
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0]
arrows=[]
badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194
badtime = 100
badmul = 1
runa = True
timer = 0
# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
normalb = pygame.image.load("resources/images/normal.png")
normalb = pygame.transform.scale(normalb,(80,50))
hardb = pygame.image.load("resources/images/hard.png")
hardb = pygame.transform.scale(hardb,(80,50))
challengingb = pygame.image.load("resources/images/challenging.png")
challengingb = pygame.transform.scale(challengingb,(80,50))
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

def startscreen():
    global badtime, badmul
    run = True
    while run:
        screen.fill((0,0,0))
        screen.blit(normalb, (width/2,height/2-60))
        screen.blit(challengingb, (width/2,height/2))
        screen.blit(hardb, (width/2,height/2+ 60))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if mx> width/2 and mx<width/2 + 80 and my>height/2 -60 and my<height/2 -10:
                    badtime = 200
                    badmul = 40
                    run = False
                elif mx> width/2 and mx<width/2+80 and my>height/2 and my<height/2+50:
                    badtime = 100
                    badmul = 25
                    run = False
                elif mx> width/2 and mx<width/2+80 and my>height/2+60 and my<height/2+110:
                    badtime = 100
                    badmul = 35
                    run = False
    
# 4 - keep looping through
if __name__=='__main__':
    while True:
        o = time.time()//1 
        runa = True
        startscreen()
        running = 1
        exitcode = 0
        oo = int(((time.time()//1)-o)*1000)
        while running:
            badtimer-=1
        
        
            # 5 - clear the screen before drawing it again
            screen.fill(0)
            # 6 - draw the screen elements
            for x in range(width//grass.get_width()+1):
                for y in range(height//grass.get_height()+1):
                    screen.blit(grass,(x*100,y*100))
            screen.blit(castle,(0,30))
            screen.blit(castle,(0,135))
            screen.blit(castle,(0,240))
            screen.blit(castle,(0,345 ))
            # 6.1 - Set player position and rotation
            position = pygame.mouse.get_pos()
            angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
            playerrot = pygame.transform.rotate(player, 360-angle*57.29)
            playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
            screen.blit(playerrot, playerpos1) 
            # 6.2 - Draw arrows
            for bullet in arrows:
                index=0
                velx=math.cos(bullet[0])*10
                vely=math.sin(bullet[0])*10
                bullet[1]+=velx
                bullet[2]+=vely
                if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                    arrows.pop(index)
                index+=1
                for projectile in arrows:
                    arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                    screen.blit(arrow1, (projectile[1], projectile[2]))
            # 6.3 - Draw badgers
            if badtimer==0:
                badguys.append([640, random.randint(50,430)])
                badtimer=badtime-(badtimer1*2)
                if badtimer1>=badmul:
                    badtimer1=badmul
                else:
                    badtimer1+=5
            index=0
            for badguy in badguys:
                if badguy[0]<-64:
                    badguys.pop(index)
                badguy[0]-=7
                        # 6.3.1 - Attack castle
                badrect=pygame.Rect(badguyimg.get_rect())
                badrect.top=badguy[1]
                badrect.left=badguy[0]
                if badrect.left<64:
                    hit.play()
                    healthvalue -= random.randint(5,20)
                    badguys.pop(index)
                        #6.3.2 - Check for collisions
                index1=0
                for bullet in arrows:
                    bullrect=pygame.Rect(arrow.get_rect())
                    bullrect.left=bullet[1]
                    bullrect.top=bullet[2]
                    if badrect.colliderect(bullrect):
                        enemy.play()
                        acc[0]+=1
                        badguys.pop(index)
                        arrows.pop(index1)
                    index1+=1
        
                # 6.3.3 - Next bad guy
        
                index+=1
            for badguy in badguys:
                screen.blit(badguyimg, badguy)
        
                # 6.4 - Draw clock
            font = pygame.font.Font(None, 24)
            x = int((pygame.time.get_ticks() - oo)-timer)
            survivedtext = font.render(str((90000-x)//60000)+":"+str((90000-x)//1000%60).zfill(2), True, (0,0,0))
            textRect = survivedtext.get_rect()
            textRect.topright=[635,5]
            screen.blit(survivedtext, textRect)
                # 6.5 - Draw health bar
            screen.blit(healthbar, (5,5))
            for health1 in range(healthvalue):
                screen.blit(health, (health1+8,8))
        
            # 7 - update the screen
            pygame.display.flip()
            # 8 - loop through the events
            for event in pygame.event.get():
                # check if the event is the X button 
                if event.type==pygame.QUIT:
                    # if it is quit the game
                    pygame.quit() 
                    exit(0) 
                    
                if event.type == pygame.KEYDOWN:
                    if event.key==K_w or event.key == K_UP:
                        keys[0]=True
                    elif event.key==K_a or event.key == K_LEFT:
                        keys[1]=True
                    elif event.key==K_s or event.key == K_DOWN:
                        keys[2]=True
                    elif event.key==K_d or event.key == K_RIGHT:
                        keys[3]=True
                if event.type == pygame.KEYUP:
                    if event.key==pygame.K_w or event.key == pygame.K_UP:
                        keys[0]=False
                    elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                        keys[1]=False
                    elif event.key==pygame.K_s or event.key==pygame.K_DOWN:
                        keys[2]=False
                    elif event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                        keys[3]=False
                if event.type==pygame.MOUSEBUTTONDOWN:
                    shoot.play()
                    position=pygame.mouse.get_pos()
                    acc[1]+=1
                    arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
        
            # 9 - Move player
            if keys[0]:
                playerpos[1]-=5
            elif keys[2]:
                playerpos[1]+=5
            if keys[1]:
                playerpos[0]-=5
            elif keys[3]:
                playerpos[0]+=5
            if playerpos[1] <= 5:
                playerpos[1] = 5
            elif playerpos[1] >= height - 5:
                playerpos[1] = height - 5
            elif playerpos[0] <= 5:
                playerpos[0] = 5
            elif playerpos[0] >= width - 5:
                playerpos[0] = width - 5
                #10 - Win/Lose 
                
            if x>=90000:
                running=0
                exitcode=1
            if healthvalue<=0:
                running=0
                exitcode=0
            if acc[1]!=0:
                accuracy=acc[0]*1.0/acc[1]*100
                accuracy = round(accuracy,2)
            else:
                accuracy=0
        # 11 - Win/lose display        
        if exitcode==0:
            
            pygame.font.init()
            font = pygame.font.Font(None, 24)
            text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
            textRect = text.get_rect()
            textRect.centerx = screen.get_rect().centerx
            textRect.centery = screen.get_rect().centery+24
            screen.blit(gameover, (0,0))
            screen.blit(text, textRect)
            
            
        else:
            
            pygame.font.init()
            font = pygame.font.Font(None, 24)
            text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
            textRect = text.get_rect()
            textRect.centerx = screen.get_rect().centerx
            textRect.centery = screen.get_rect().centery+24
            screen.blit(youwin, (0,0))
            screen.blit(text, textRect)
            
        while runa:
            
            pygame.display.flip()
            keys = [False, False, False, False]
            playerpos=[100,100]
            acc=[0,0]
            arrows=[]
            badtimer=100
            badtimer1=0
            badguys=[[640,100]]
            healthvalue=194
            badtime = 100
            badmul = 1
            timer = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        runa = False
            
                   
               

