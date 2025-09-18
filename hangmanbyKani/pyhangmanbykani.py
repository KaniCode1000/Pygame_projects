# Kani's Hangman Game!!
import pygame
import random
import math



#setting up the display

pygame.init()
pygame.mixer.init()

WIDTH , HEIGHT = 800, 500
display_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kani's Hangman Game!!")

#handling backgrounds

bgchoosing = random.randint(0,4)
# if not bgchoosing == 3:
#     bgimg = pygame.image.load(f'hangmanbg{bgchoosing}.jpg')
# elif bgchoosing == 3:
#     bgimg = pygame.image.load(f'hangmanbg{bgchoosing}.png')
# bgimg = pygame.transform.scale(bgimg , (WIDTH, HEIGHT))
gameover = pygame.image.load('game_over.jpg')
gameover = pygame.transform.scale(gameover , (WIDTH, HEIGHT))


#colors
GOLD      = (195, 175, 0)
abcd = (173,255,47)
BLACK     = (0,0,0)
RED = (255,0,0)
LIME =(50,205,50)
WHITE =(255,255,255)
#fonts 
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('algerian', 70)

#hint
hintbool = [True]

#images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
    

#Game specific variables
hang_stats = 0
guessed = []
words = ["NOSTALGIC","CHILDREN","USUALLY" ,"EXPRESS", "THEIR", "FRUSTATION","PERSPECTIVE","RANDOM","HANGMAN",
         "GENIUS","PROTEGEE","DEVELOPER","OBJECT","ZOOLOGY","ELEPHANT","INGENIUS","INTRUSIVE","LAVISH",
         "EXCITED","PROVOKE","RETRENCH","DIMINISH","ARBITRARY","INDIAN","BROTHER","CODING","TRUNCATE",
         "HEED","HONOUR","OBEDIENCE","SERENITY","SYMPATHY","XEROPHYTE","EMPATHY","XENON",
         "XENOBIOTIC","XYLOPHONE","AJAR","ABRIDGE","BIRD","TOUCAN","ORCA","SPIN",
         "SCAR","LESION","BLOTCH","INJURE","SPRINT","SCRATCH","CREATIVE","SPEAKER","PUBLIC","PRIVATE","INDIGENOUS"
         ,"MARTYR","DEMOCRACY","AUTOCRACY","EGOISTIC","NARCISSISM","ALTRUISTIC","MONARCHY","GESTURE","JESTER"
         ,"ARCHITECT","RECURSIVE","ITERATIVE","FAMOUS","HARP","ACID","TOMB","DUKE","ZONE","ZERO","COMPLETE"
         ,"LANGUAGE","BACKGROUND","RADIUS","DIAMETER","TANGENT","SECTOR","SEGMENT",
         "CHOICE","GRACE","GOD","DARK","DARKNESS","GODDESS","TAURUS","HYDRA","WATERFALL",
         "CARPET","STORE","STATION","STATIONARY","LORD","FROST","FORK","FLOOR","FROM","FIRE",
         "FIG","SIN","FIT","FIN","BIN","TIN","SHAME","FRAME","DWARF","DEN","MINOTAUR","SLOPPY"
         ,"FLOPPY","FLAP","AEROPLANE","CAR","TRUCK","BUS","CRUSH","VAN","HELICOPTER"
         ,"ORTHODOX","TRANQUIL","ZEALOUS","JAM","JAR","JEALOUS","TRAFFIC","INTROVERT","EXTROVERT"
         ,"HOP","HARD","HANG","HARM","CALM","CHAOS","HURT","LUNGS","HEART","SPLEEN","LIVER"
         ,"AMBITIOUS","SKILL","SKIN","HAIR","DOOR","CROWBAR","HOST","EXORCISM","ENERGY","ARC","ARCTIC"
         ,"BALL","BAT","CRICKET","FOOTBALL","TENNIS","TRUNK","TREE","LEAF","KILOGRAM","GRAM"
         ,"KINGDOM","LION","TIGER","PANTHER","BLACK","LIME","QUICK","FAST","SWIFT","DEVOUT","VIBRANT"
         ,"VIGOROUS","JACKAL","JUNIOR","JUDICIARY","ZOO","ZIMBABWE","ZEN","ZINC",
         "BOX","FOX","TAX","TAXONOMY","TAXA","TACKLE","TART","PANCAKE","ROD","CELLULAR",
         "GARBAGE","GRAIN","LANTERN","LICK","LIST","DICTIONARY","TUPLE","SET","BRONCHIOLE"
         ,"ALVEOLI","SYNTHESIS","SOLAR","CITRUS","ORANGE","LEMON","APPLE","BANANA","REMINANT"
         ,"SUPERNOVA","LUMINOUS","HYPERNOVA","TELEPORT","LIZARD","CAMOUFLAGE","STELLAR"
         ,"SPACE","PANEL","CRATE","GRAVEYARD","SPINDLE","VOLATILE","MOLECULE","ATOM","ATMOSPHERE"
         ,"BIOSPHERE","EXOSPHERE","LITHOSPHERE","IONOSPHERE","STRATA","SPHERE"
         ,"TROPICAL","PYRAMID","PENTAGON","TRIANGLE","RECTANGLE","SQUARE"]
the_word = random.choice(words)




#button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
    
    
    

    


#message display

def display_message(message, colours):
    pygame.time.delay(4000)
    display_screen.blit(gameover, (0,0))
    text = WORD_FONT.render(message, 1, colours)
    display_screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    
    
# drawing the mainscreen


def bgchange():
    global bgchoosing
    bgchoosing = random.randint(0, 4)
def draw():
    global bgchoosing
    if not bgchoosing == 3:
        bgimg = pygame.image.load(f'hangmanbg{bgchoosing}.jpg')
    elif bgchoosing == 3:
        bgimg = pygame.image.load(f'hangmanbg{bgchoosing}.png')
    bgimg = pygame.transform.scale(bgimg , (WIDTH, HEIGHT))
    display_screen.blit(bgimg, (0,0))
    
    #draw title
    text = TITLE_FONT.render("KANISHK'S HANGMAN", 1, GOLD)
    display_screen.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
     # draw word
    display_word = ""
    for letter in the_word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    display_screen.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(display_screen, abcd, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, abcd)
            display_screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    display_screen.blit(images[hang_stats], (150, 100))
    pygame.display.update()


#mainloop
def main():
    global hang_stats, guessed, words, the_word, hintbool
    
    FPS = 80
    clock = pygame.time.Clock()
    running = True
    pygame.mixer.music.load('Spiral.wav')
    pygame.mixer.music.play()
    
    while running:
    
        
        
       
        try:
             
            if len(the_word) > 5 and hintbool[0] == True:
                x = random.randint(0,len(the_word))        
                for qv in guessed:
                    if qv == the_word[x]:
                        x = random.randint(0,len(the_word))
                    else:
                        continue  
                
                hint = pygame.image.load('hint.png')
                hint = pygame.transform.scale(hint, (100,100))
                display_screen.blit(hint, (680,100))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.display.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            pygame.music.stop()
                            pygame.quit()
                            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                       mousex, mousey = pygame.mouse.get_pos()
                       s = math.sqrt((680 - mousex)**2 + (100 - mousey)**2)
                       if s < 140:
                           htext = TITLE_FONT.render(f"Choose {the_word[x]}", 1, WHITE)
                           hrect = htext.get_rect()
                           display_screen.blit(htext, (250,250))
                           pygame.display.update()
                           a = pygame.draw.rect(display_screen, BLACK, hrect)
                           hintbool[0] = False
                           pygame.time.wait(400)
                           display_screen.blit(a,(250,250))
                           continue
            else:
                nohint = pygame.image.load('nhint.png')
                nohint = pygame.transform.scale(nohint, (80,80))
                display_screen.blit(nohint, (680,100))
                pygame.display.update()
                               
                          
        except:
            pass
            
        
                    
        finally:        
        
            # FPS rate handling
            clock.tick(FPS) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                   m_x, m_y = pygame.mouse.get_pos()
                   for letter in letters:
                       x, y, letr, in_sight = letter
                       if in_sight:
                           dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                           if dis < RADIUS:
                               letter[3] = False 
                               guessed.append(letr)
                               if letr not in the_word:
                                   hang_stats += 1
            
            draw()    
            won = True
            for letter in the_word:
                if letter not in guessed:
                   won = False
                   break
            
            
            if won:
                display_message("YOU WON!", LIME)
                pygame.mixer.music.stop()
                pygame.mixer.music.load('win.wav')
                pygame.mixer.music.play()
                
                hang_stats = 0
                guessed = []
                the_word = random.choice(words)
                hintbool[0] = True
                for letter in letters:
                    letter[3] = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('Spiral.wav')
                    pygame.mixer.music.play()
                    bgchange()
                continue
            
            if hang_stats == 6:
                display_message(f"YOU LOST! The word was {the_word}",RED)
                pygame.mixer.music.stop()
                pygame.mixer.music.load('lost.wav')
                pygame.mixer.music.play()
                
                hang_stats = 0
                guessed = []
                the_word = random.choice(words)
                hintbool[0] = True
                for letter in letters:
                    letter[3] = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('Spiral.wav')
                    pygame.mixer.music.play()
                    bgchange()
                continue
            
                
            
            
if __name__ == '__main__':     
    while True:
        
        main()
        
    
    
pygame.quit()