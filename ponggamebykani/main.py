# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
 
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
font = pygame.font.Font(None, 24)


# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong game by kani")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200
 
ball = Ball((255,0,0),10,10)
ball.rect.x = 345
ball.rect.y = 195
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0
#timerlimit

# -------- Main Program Loop -----------
while carryOn:
    timer = int(pygame.time.get_ticks())
    timershow = str((90000-timer)//60000)+":"+str((90000-timer)//1000%60).zfill(2), True, (0,0,0)
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)    
 
    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=690:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.SysFont('algerian', 70)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
    x = 0
    if timer >= 90000 and x == 0:
        if scoreA > scoreB:
            player = 'Player 1'
            result = 'wins!!'
            x+=1
        elif scoreA<scoreB:
            player = 'Player 2'
            result = 'wins!!'
            x+=1
        elif scoreA == scoreB:
            player = 'It is a'
            result = 'tie!'
            x+= 1
        screen.fill(BLACK)
        # font = pygame.font.Font(None, 24)
        text = f'{player} {result}'
        survivedtext = font.render(text, True, (255,255,255))
        textRect = survivedtext.get_rect()
        textRect.center=[300,250]
        screen.blit(survivedtext, textRect)
        
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
    if x ==1:
        pygame.time.delay(2000)
        break
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()