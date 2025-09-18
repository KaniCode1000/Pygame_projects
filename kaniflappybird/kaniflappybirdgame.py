# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:36:55 2020

@author: Goutam
"""
import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
from time import time
from time import sleep
from math import sqrt
from os import path
# Global Variables for the game
FPS = 32
bgchange = 0
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
BACKGROUND = 'background.png'
PIPE = 'pipe.png'
playerchose = 0
midtowhat = True
LIME =(50,205,50)
GOLD=(195,175,0)
BLACK = (0,0,0)
colourchose = 0
pipechose = 0
PIPEr = 'pipe-red.png'
score = 0
White = (255,255,255)


def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP) or(event.type == pygame.MOUSEBUTTONDOWN):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'][bgchange], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def pipe_fill_screen():
    global pipechose
    ChoseFont = pygame.font.Font('freesansbold.ttf', 20)
    ChoseSurf = ChoseFont.render('Chose a pipe',  True, BLACK)
    ChoseSurfRect = ChoseSurf.get_rect()
    ChoseSurfRect.midtop = (SCREENWIDTH / 2,SCREENHEIGHT - 461)
    redpipe = pygame.image.load('pipe-red.png')
    greenpipe = pygame.image.load('pipe.png')
    redpipe = pygame.transform.scale(redpipe,(50,150))
    greenpipe = pygame.transform.scale(greenpipe,(50,150))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                pipechose = random.randint(0,1)
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'][0], (0, 0))
                SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
                SCREEN.blit(redpipe,(SCREENWIDTH/3-60,SCREENHEIGHT/2))
                SCREEN.blit(greenpipe,(SCREENWIDTH-90,SCREENHEIGHT/2))
                SCREEN.blit(ChoseSurf, ChoseSurfRect)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                           mousex, mousey = pygame.mouse.get_pos()
                           
                           piper = sqrt(((SCREENWIDTH/3 - 60) - mousex)**2 + (SCREENHEIGHT/2 - mousey)**2)
                           pipeg = sqrt(((SCREENWIDTH - 90) - mousex)**2 + (SCREENHEIGHT/2 - mousey)**2)
                           if piper < 159:
                               pipechose = 0
                               return
                           if pipeg < 159:
                               pipechose = 1
                               return
def loadscreen():
    Load = pygame.image.load('credits.png').convert_alpha()
    Load = pygame.transform.scale(Load,(SCREENWIDTH,SCREENHEIGHT))   
    SCREEN.blit(Load,(0,0))      
    pygame.display.update()
    pygame.time.wait(2000)
    while True:
        instruction = pygame.image.load('instructions.png').convert_alpha()
        instruction = pygame.transform.scale(instruction,(SCREENWIDTH,SCREENHEIGHT))   
        SCREEN.blit(instruction,(0,0))      
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return
def gameover():
    global score
    if(not path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
                f.write("0")
    with open("hiscore.txt", "r") as f:
            hiscore = f.read()
    if int(hiscore)<int(score):
        hiscore = str(score)
    while True:
        if bgchange == 0:
            if score>10 and score<20:
                gameoverbird = pygame.image.load('gameoverbirdbronze.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=20 and score<30:
                gameoverbird = pygame.image.load('gameoverbirdsilver.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=30 and score<40:
                gameoverbird = pygame.image.load('gameoverbirdgold.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=40:
                gameoverbird = pygame.image.load('gameoverbirdplatinum.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            else:
                gameoverbird = pygame.image.load('gameoverbird.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
        if bgchange == 1:
            if score>=10 and score<20:
                gameoverbird = pygame.image.load('gameoverbirdnightbronze.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=20 and score<30:
                gameoverbird = pygame.image.load('gameoverbirdnightsilver.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=30 and score<40:
                gameoverbird = pygame.image.load('gameoverbirdnightgold.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            elif score>=40:
                gameoverbird = pygame.image.load('gameoverbirdnightplatinum.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
            else:
                gameoverbird = pygame.image.load('gameoverbirdnight.png')
                gameoverbird = pygame.transform.scale(gameoverbird,(SCREENWIDTH,SCREENHEIGHT))
        SCREEN.blit(gameoverbird,(0,0))
        width = 0
        wwidth = 0
        myDigits = [int(x) for x in list(str(score))]
        for digit in myDigits:
            width += GAME_SPRITES['gameovernumbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2
    
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['gameovernumbers'][digit], (Xoffset+85, 223.5))
            Xoffset += GAME_SPRITES['gameovernumbers'][digit].get_width()
        myhiscore = [int(y) for y in list(str(hiscore))]
        for highscore in myhiscore:
            wwidth += GAME_SPRITES['gameovernumbers'][highscore].get_width()
        Xhighoffset = (SCREENWIDTH - wwidth)/2
    #hiscore
        for highscore in myhiscore:
            SCREEN.blit(GAME_SPRITES['gameovernumbers'][highscore], (Xhighoffset+85, 273))
            Xhighoffset += GAME_SPRITES['gameovernumbers'][highscore].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        with open("hiscore.txt", "w") as f:
                    f.write(str(hiscore))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                score = 0
                return
                           
    
def birdchose():
    global colourchose
    red = pygame.image.load('redbird-downflap.png')
    blue = pygame.image.load('bluebird-downflap.png')
    yellow = pygame.image.load('yellowbird-downflap.png')
    redpipe = pygame.image.load('pipe-red.png')
    greenpipe = pygame.image.load('pipe.png')
    redpipe = pygame.transform.scale(redpipe,(50,150))
    greenpipe = pygame.transform.scale(greenpipe,(50,150))
    
    ChoseFont = pygame.font.Font('freesansbold.ttf', 20)
    ChoseSurf = ChoseFont.render('Chose a bird',  True, BLACK)
    ChoseSurfRect = ChoseSurf.get_rect()
    ChoseSurfRect.midtop = (SCREENWIDTH / 2,SCREENHEIGHT - 461)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                colourchose = random.randint(0,2)
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'][0], (0, 0))
                SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
                SCREEN.blit(red,(SCREENWIDTH/3-60,SCREENHEIGHT/2))
                SCREEN.blit(blue,(2*SCREENWIDTH/3-60,SCREENHEIGHT/2))
                SCREEN.blit(yellow,(SCREENWIDTH-60,SCREENHEIGHT/2))
                SCREEN.blit(ChoseSurf, ChoseSurfRect)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                           mousex, mousey = pygame.mouse.get_pos()
                           mousex+=60
                           sr = sqrt(((SCREENWIDTH/3) - mousex)**2 + (SCREENHEIGHT/2 - mousey)**2)
                           sb = sqrt(((2*(SCREENWIDTH/3)) - mousex)**2 + (SCREENHEIGHT/2 - mousey)**2)
                           sy = sqrt(((SCREENWIDTH) - mousex)**2 + (SCREENHEIGHT/2 - mousey)**2)
                           
                           if sr < 50:
                               colourchose = 0
                               pipe_fill_screen()
                               return
                           elif sb < 50:
                               colourchose = 1
                               pipe_fill_screen()
                               return
                           elif sy < 50:
                               colourchose = 2
                               pipe_fill_screen()
                               return
def mainGame():
    global bgchange,playerchose,midtowhat,score
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or (event.type == pygame.MOUSEBUTTONDOWN):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
            
                

        
        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest: 
            GAME_SOUNDS['die'].play()
            SCREEN.fill(White)
            pygame.display.update()
            pygame.time.wait(30)
            while True:
                SCREEN.blit(GAME_SPRITES['background'][bgchange], (0, 0))
                for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                    SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                    SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES['birdcrash'][colourchose],(playerx,playery))
                pygame.event.clear()
                pygame.event.pump()
                pipeVelX = 0
                playerVelY = -9
                playerMaxVelY = 10
                playerAccY = 1
                playerFlapAccv = -9
                pygame.display.flip()
                playery += 5
                pygame.time.wait(8)
                if playery > GROUNDY -6 :
                    pygame.time.wait(500)
                    return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        bgtime = time() 
        bgtime = bgtime//10
        if bgtime%2 == 0 and bgchange == 0:
            bgchange = 1
        elif bgtime%2 and bgchange == 1:
            bgchange = 0
        # Lets blit our sprites now
        if playerchose == 0:
            playerchose += 1
            midtowhat = True
        elif playerchose == 1 and midtowhat == True:
            playerchose += 1
        elif playerchose == 1 and midtowhat == False:
            playerchose -= 1
        elif playerchose == 2:
            playerchose -= 1
            midtowhat = False
        SCREEN.blit(GAME_SPRITES['background'][bgchange], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player2'][playerchose], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'] - 10) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x'] - 10) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(20, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Kani')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha(),
    )
    GAME_SPRITES['gameovernumbers'] = [
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha(),
    ]
    for i in range (0,10):
        GAME_SPRITES['gameovernumbers'][i] = pygame.transform.scale(GAME_SPRITES['gameovernumbers'][i],(16,28))
    GAME_SPRITES['message'] =pygame.image.load('message.png').convert_alpha()
    GAME_SPRITES['message'] = pygame.transform.scale(GAME_SPRITES['message'],(200,280))
    GAME_SPRITES['base'] =pygame.image.load('base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )
    
    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('wing.wav')

    GAME_SPRITES['background'] = (pygame.image.load(BACKGROUND).convert(),
    pygame.image.load('background-night.png').convert())
    GAME_SPRITES['birdcrash'] = [pygame.image.load('redbird-down.png').convert_alpha(),
                                 pygame.image.load('bluebird-down.png').convert_alpha(),
                                 pygame.image.load('yellowbird-down.png').convert_alpha()]
    for i in range(0,3):
        GAME_SPRITES['birdcrash'][i] = pygame.transform.scale(GAME_SPRITES['birdcrash'][i],(26,34))
    loadscreen()
    birdchose()
    
    if colourchose == 2:
        GAME_SPRITES['player'] = pygame.image.load('yellowbird-downflap.png').convert_alpha()
        GAME_SPRITES['player'] = pygame.transform.scale(GAME_SPRITES['player'],(34,24))
        GAME_SPRITES['player2'] = (pygame.image.load('yellowbird-downflap.png').convert_alpha(),
                               pygame.image.load('yellowbird-midflap.png').convert_alpha(),
                               pygame.image.load('yellowbird-upflap.png').convert_alpha())
        
    if colourchose == 0:
        GAME_SPRITES['player'] = pygame.image.load('redbird-downflap.png').convert_alpha()
        GAME_SPRITES['player'] = pygame.transform.scale(GAME_SPRITES['player'],(34,24))
        GAME_SPRITES['player2'] = (pygame.image.load('redbird-downflap.png').convert_alpha(),
                                   pygame.image.load('redbird-midflap.png').convert_alpha(),
                               pygame.image.load('redbird-upflap.png').convert_alpha())
    if colourchose == 1:
        GAME_SPRITES['player'] = pygame.image.load('bluebird-downflap.png').convert_alpha()
        GAME_SPRITES['player'] = pygame.transform.scale(GAME_SPRITES['player'],(34,24))
        GAME_SPRITES['player2'] = (pygame.image.load('bluebird-downflap.png').convert_alpha(),
                               pygame.image.load('bluebird-midflap.png').convert_alpha(),
                               pygame.image.load('bluebird-upflap.png').convert_alpha())
        
    if pipechose == 1:
        
        GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
                           pygame.image.load(PIPE).convert_alpha()
                           )
    elif pipechose == 0:
        GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPEr).convert_alpha(), 180), 
                               pygame.image.load(PIPEr).convert_alpha()
                               )
    
    while True:
        
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
        gameover()