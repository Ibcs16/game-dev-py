import pygame
from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TicTacToe')

# Define variavles
line_width = 6
game_board = [
  [0,0,0],
  [0,0,0],
  [0,0,0]
]
clicked = False
pos = []
player = 1
winner = 0
game_over = False

# define colors
green = (0,255,0)
red = (255, 0,0)
blue = (0,0,255)

# define font
font = pygame.font.SysFont(None, 40)

# create play again rectangle
again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)

def draw_grid():
  bg = (255, 255, 200)
  grid = (50, 50, 50)
  screen.fill(bg)

  for x in range(1,3):
    pygame.draw.line(screen, grid, (0, x * 100), (SCREEN_WIDTH, x * 100), line_width)
    pygame.draw.line(screen, grid, (x * 100, 0), (x * 100,SCREEN_HEIGHT ), line_width)

def draw_markers():
  x_pos = 0
  for x in game_board:
    y_pos = 0
    for y in x:
      if y == 1:
        pygame.draw.line(screen, green, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
        pygame.draw.line(screen, green, (x_pos * 100 + 15, y_pos * 100 + 85), (x_pos * 100 + 85, y_pos * 100 + 15), line_width)
      elif y == -1:
        pygame.draw.circle(screen, red,( x_pos * 100 + 50, y_pos * 100 +50), 38, line_width)
      y_pos += 1
    x_pos += 1

def check_winner():
  global winner
  global game_over

  y_pos = 0
  for x in game_board:
    # check columns
    if sum(x) == 3:
      winner = 1
      game_over = True
    elif sum(x) == -3:
      winner = 2
      game_over = True
      
    # check rows
    if game_board[0][y_pos] + game_board[1][y_pos] + game_board[2][y_pos] == 3:
      winner = 1
      game_over = True
    elif game_board[0][y_pos] + game_board[1][y_pos] + game_board[2][y_pos] == -3:
      winner = 2
      game_over = True
    y_pos += 1

    # check cross
    if game_board[0][0] + game_board[1][1] + game_board[2][2] == 3 or game_board[2][0] + game_board[1][1] + game_board[0][2] == 3:
      winner = 1
      game_over = True
    elif game_board[0][0] + game_board[1][1] + game_board[2][2] == -3 or game_board[2][0] + game_board[1][1] + game_board[0][2] == -3:
      winner = 2
      game_over = True

def reset_game_board():
  winner = 0
  player = 1
  pos = []
  game_over = False
  game_board = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
  ]
 
def draw_winner(winner):
  win_text = 'Player ' + str(winner) + ' wins!'
  win_img = font.render(win_text, True, blue)
  win_color = red

  if winner == 1:
    win_color = green
  elif winner == 2:
    win_color = red

  pygame.draw.rect(screen, win_color, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 - 60, 200, 50))
  screen.blit(win_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

  again_text = 'Play Again?'
  again_img = font.render(again_text, True, blue)
  pygame.draw.rect(screen, green, again_rect)
  screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))

run = True
while run:
  draw_grid()
  draw_markers()
 
  # event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if game_over == False:
      if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
        clicked = True
      elif event.type == pygame.MOUSEBUTTONUP and clicked == True:
        clicked = False
        pos = pygame.mouse.get_pos()
        cell_x  = pos[0]
        cell_y = pos[1]
        if game_board[cell_x // 100][cell_y // 100] == 0:
          game_board[cell_x // 100][cell_y // 100] = player
          player *= -1
          check_winner()
    elif game_over == True:
      # check mouse click on Play again
      if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
        clicked = True
      elif event.type == pygame.MOUSEBUTTONUP and clicked == True:
        clicked = False
        pos = pygame.mouse.get_pos()
        if again_rect.collidepoint(pos):
          print('clicked play again')
          reset_game_board()
  
  if game_over == True:
    draw_winner(winner)
    
  pygame.display.update()

pygame.quit()