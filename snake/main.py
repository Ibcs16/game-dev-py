import random
import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((screen_width, screen_width))

# game variables
cell_size = 10
direction = 1# 1 is up, 2 is right, 3 is down, 4 is left

# create snake
snake_pos = [
  [int(screen_width / 2), int(screen_height / 2)],
  [int(screen_width / 2), int(screen_height / 2) + cell_size],
  [int(screen_width / 2), int(screen_height / 2) + cell_size * 2],
  [int(screen_width / 2), int(screen_height / 2) + cell_size * 3]
]
update_snake = 0
food = [0,0]
new_food = True
new_piece = [0,0]
score = 0
game_over = False

# define colors
bg = (255, 200, 150)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
red = (255, 0, 0)
blue = (0, 0, 255)
# define colors
font = pygame.font.SysFont(None, 40)

def check_game_over(game_over):
  global snake_pos
  # check if snake has gone out of bounds
  is_out_of_bounds = snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][0] > screen_height
  if is_out_of_bounds:
    game_over = True
  else:
    head_count = 0
    # check if snake has eaten itself
    for segment in snake_pos:
      if segment == snake_pos[0] and head_count > 0:
        game_over = True
      head_count += 1
  return game_over

def draw_score():
  score_txt = 'Score: ' + str(score)
  score_img = font.render(score_txt, True, blue)
  screen.blit(score_img, (0,0))

def create_food():
  global new_food
  global food
  if new_food:
    new_food = False
    food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)
    food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)

def draw_food():
  pygame.draw.rect(screen, red, (food[0], food[1], cell_size, cell_size))

def check_food_eaten():
  global snake_pos
  global food
  global new_food
  global new_piece
  global score

  if snake_pos[0] == food:
    new_food = True
    # create new_piece
    new_piece = list(snake_pos[-1])
    if direction == 1:
      new_piece[1] += cell_size
    elif direction == 3:
      new_piece[1] -= cell_size
    elif direction == 2:
      new_piece[0] -= cell_size
    elif direction == 4:
      new_piece[0] += cell_size
    # attach to snake tail
    snake_pos.append(new_piece)
    # increase score
    score += 1

def draw_snake():
  global snake_pos
  head = 1
  for x in snake_pos:
    if head == 0:
      pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
      pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
    elif head == 1:
      pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
      pygame.draw.rect(screen, red, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
      head = 0

def move_snake():
  global snake_pos
  snake_pos = snake_pos[-1:] + snake_pos[:-1]
  # heading up
  if direction == 1:
    snake_pos[0][0] = snake_pos[1][0]
    snake_pos[0][1] = snake_pos[1][1] - cell_size
  elif direction == 3:
    snake_pos[0][0] = snake_pos[1][0]
    snake_pos[0][1] = snake_pos[1][1] + cell_size
  elif direction == 2:
    snake_pos[0][1] = snake_pos[1][1]
    snake_pos[0][0] = snake_pos[1][0] + cell_size
  elif direction == 4:
    snake_pos[0][1] = snake_pos[1][1]
    snake_pos[0][0] = snake_pos[1][0] - cell_size

def draw_screen():
  screen.fill(bg)

run = True
while run:
  draw_screen()
  draw_score()
  draw_snake()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP and direction != 3:
        direction = 1
      elif event.key == pygame.K_RIGHT  and direction != 4:
        direction = 2
      elif event.key == pygame.K_DOWN  and direction != 1:
        direction = 3
      elif event.key == pygame.K_LEFT  and direction != 2:
        direction = 4

  create_food()
  draw_food()
  check_food_eaten()

  if game_over == False:
    if update_snake > 99:
      update_snake = 0
      move_snake()
      game_over = check_game_over(game_over)

  pygame.display.update()
  update_snake += 1
pygame.quit()