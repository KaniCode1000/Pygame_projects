
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 14:07:38 2020

@author: Kanishk
Connect four game(both 2 player and AI!)
"""
import numpy
import pygame
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
playorclp = 0
ROW = 6
COLUMN = 7
images = []
FPS = 32
FPSCLOCK = pygame.time.Clock()
difficulty = 0

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
AImovegap = 500
WINDOW_LENGTH = 4
def imagess(size):
    for i in range(0,192):
        image = pygame.image.load(f'crp/frame{i}_crp.jpg')
        image = pygame.transform.scale(image, size)
        images.append(image)
    return images
def AIorplayerchoice():
    global playorclp
    run = True
    playerx = [250,490]
    playery = [250,354]
    clpx = [250,490]
    clpy = [450,554]
    while run:
        screen.fill(BLACK)
        pabuttons = [pygame.image.load('player.png'),pygame.image.load('AI.png')]
        
        screen.blit(pabuttons[0], (250,250))
        screen.blit(pabuttons[1], (250,450))
    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex,mousey = pygame.mouse.get_pos()
                if mousex >= playerx[0] and mousex <= playerx[1] and mousey >= playery[0] and mousey<=playery[1]:
                    playorclp = 1
                    run = False
                elif mousex >= clpx[0] and mousex <= clpx[1] and mousey >= clpy[0] and mousey<=clpy[1]:
                    playorclp = 0
                    options()
                    run = False
    
def options():
    global difficulty, AImovegap
    running = True
    easydepth = 3
    challengingdepth = 4
    harddepth = 5
    easyy = [230,330]
    buttonx = [250,410]   
    chay = [350,450]
    
    hardy = [470,570]
    while running:
        screen.fill(BLACK)
        buttons = [pygame.image.load('normal.png'),pygame.image.load('challenging.png'),pygame.image.load('hard.png')]
        for i in range(0,3):
            buttons[i] = pygame.transform.scale(buttons[i], (160,100))
        screen.blit(buttons[0], (250,230))
        screen.blit(buttons[1], (250,350))
        screen.blit(buttons[2], (250,470))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex,mousey = pygame.mouse.get_pos()
                if mousex >= buttonx[0] and mousex <= buttonx[1] and mousey >= easyy[0] and mousey<=easyy[1]:
                    difficulty = easydepth
                    running = False
                    break
                elif mousex >= buttonx[0] and mousex <= buttonx[1] and mousey >= chay[0] and mousey<=chay[1]:
                    difficulty = challengingdepth
                    running = False
                    break
                elif mousex >= buttonx[0] and mousex <= buttonx[1] and mousey >= hardy[0] and mousey<=hardy[1]:
                    difficulty = harddepth
                    AImovegap = 0
                    running = False
                    break
def create_board():
	board = numpy.zeros((ROW,COLUMN))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_loc(board, col):
	return board[ROW-1][col] == 0

def open_row(board, col):
	for r in range(ROW):
		if board[r][col] == 0:
			return r


def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN-3):
		for r in range(ROW):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN):
		for r in range(ROW-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(ROW-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(3, ROW):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN):
		for r in range(ROW):
			pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), RADIUS)
	
	for c in range(COLUMN):
		for r in range(ROW):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
	pygame.display.update()
#AI func
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW-3):
		for c in range(COLUMN-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW-3):
		for c in range(COLUMN-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN):
		if is_valid_loc(board, col):
			valid_locations.append(col)
	return valid_locations

def best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col
def main():
    global game_over,turn
    while not game_over:
        
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
                            sys.exit()
                            pygame.quit()
    		if event.type == pygame.MOUSEMOTION:
    			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
    			posx = event.pos[0]
    			if turn == 0:
    				pygame.draw.circle(screen, RED, (posx, int(SQUARE/2)), RADIUS)
    			else: 
    				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE/2)), RADIUS)
    		pygame.display.update()
    
    		if event.type == pygame.MOUSEBUTTONDOWN:
    			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
    			
    			# Ask for Player 1 Input
    			if turn == 0:
    				posx = event.pos[0]
    				col = int(math.floor(posx/SQUARE))
    
    				if is_valid_loc(board, col):
    					row = open_row(board, col)
    					drop_piece(board, row, col, 1)
    
    					if winning_move(board, 1):
    						label = myfont.render("Player 1 wins!!", 1, RED)
    						screen.blit(label, (20,10))
    						game_over = True
    
    
    			# # Ask for Player 2 Input
    			else:				
    				posx = event.pos[0]
    				col = int(math.floor(posx/SQUARE))
    
    				if is_valid_loc(board, col):
    					row = open_row(board, col)
    					drop_piece(board, row, col, 2)
    
    					if winning_move(board, 2):
    						label = myfont.render("Player 2 wins!!", 1, YELLOW)
    						screen.blit(label, (20,10))
    						game_over = True
    
    			draw_board(board)
    
    			turn += 1
    			turn = turn % 2
    
    			if game_over:
    				pygame.time.wait(3000)
    
def main_AI():
        global game_over, turn
        while not game_over:
        
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
                            sys.exit()
                            pygame.quit()
            
        
        		if event.type == pygame.MOUSEMOTION:
        			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
        			posx = event.pos[0]
        			if turn == PLAYER:
        				pygame.draw.circle(screen, RED, (posx, int(SQUARE/2)), RADIUS)
        
        		pygame.display.update()
        
        		if event.type == pygame.MOUSEBUTTONDOWN:
        			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
        			#print(event.pos)
        			# Ask for Player 1 Input
        			if turn == PLAYER:
        				posx = event.pos[0]
        				col = int(math.floor(posx/SQUARE))
        
        				if is_valid_loc(board, col):
        					row = open_row(board, col)
        					drop_piece(board, row, col, PLAYER_PIECE)
        
        					if winning_move(board, PLAYER_PIECE):
        						label = myfont.render("Player 1 wins!!", 1, RED)
        						screen.blit(label, (20,10))
        						game_over = True
        
        					turn += 1
        					turn = turn % 2
        
        					
        					draw_board(board)
    
    
    	# # Ask for Player 2 Input
        	if turn == AI and not game_over:				
        
        		#col = random.randint(0, COLUMN-1)
        		col = best_move(board, AI_PIECE)
        		col, minimax_score = minimax(board, difficulty, -math.inf, math.inf, True)
        
        		if is_valid_loc(board, col):
        			pygame.time.wait(AImovegap)
        			row = open_row(board, col)
        			drop_piece(board, row, col, AI_PIECE)
        
        			if winning_move(board, AI_PIECE):
        				label = myfont.render("Player 2 wins!!", 1, YELLOW)
        				screen.blit(label, (20,10))
        				game_over = True
        
        			
        			draw_board(board)
        
        			turn += 1
        			turn = turn % 2
        
        	if game_over:
        		pygame.time.wait(3000)
        
#Ai func end
if __name__ == '__main__':
    
    turn = random.randint(PLAYER, AI)
    board = create_board()
    
    game_over = False
    
    
    pygame.init()
    pygame.mixer.init()
    pygame.display.init()
    SQUARE = 100
    
    width = COLUMN * SQUARE
    height = (ROW+1) * SQUARE
    
    size = (width, height)
    
    RADIUS = int(SQUARE/2 - 5)
    
    screen = pygame.display.set_mode(size)
    imageplay = imagess(size)
    run = True
  
    intro = pygame.mixer.Sound('intro_song.wav')
    intro.set_volume(0.05)
    intro.play()
    play1 = pygame.mixer.Sound('main.wav')
    play1.set_volume(0.05)
    while run:
        for imageindex in range(0,192):
            screen.blit(imageplay[imageindex],(0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
            pygame.time.wait(20)
        run = False
    run = True
    while run:
        AIorplayerchoice()
        run = False
        
    screen.fill(BLACK)
    draw_board(board)
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 75)
    while True:
        if playorclp == 0:
            play1.play(-1)
            main_AI()
            break
        elif playorclp == 1:
            play1.play(-1)
            main()
            break
    pygame.quit()
    