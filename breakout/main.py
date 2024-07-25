import pygame
from pygame.locals import *

pygame.init()

# window
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BreakOut')

# fonts
font = pygame.font.SysFont('Grand9k Pixel', 15)

# colors
bg = (50, 25, 50)
text_color = (149, 197, 172)
paddle_color = (149, 197, 172)

# block colors
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

# assets

# obj sizes
paddle_size = (30, 40)
ball_size = 14

# game variables
cols = 6
rows = 6
live_ball = False
game_over = 0

def draw_text(text, font, color, x, y):
  img = font.render(text, True, color)
  screen.blit(img, (x, y))

class Paddle():
  def __init__(self):
    self.reset()

  def move(self):
    self.direction = 0
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= self.speed
      self.direction = -1
    elif key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += self.speed
      self.direction = 1

  def draw(self):
    pygame.draw.rect(screen, paddle_color, self.rect)
  
  def reset(self):
    self.width = int(screen_width / cols)
    self.height = 20
    self.x = int((screen_width / 2) - (self.width / 2))
    self.y = screen_height - (self.height * 2)
    self.speed = 10
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.direction = 0

class Wall():
  def __init__(self):
    self.width = screen_width // cols
    self.height = 50

  def create(self):
    self.blocks = []
    for row in range(rows):
      # row list
      block_row = []
      for col in range(cols):
        block_x = col * self.width
        block_y = row * self.height
        rect = pygame.Rect(block_x, block_y, self.width, self.height)
        # assign block strength based on row
        if row < 2:
          strength = 3
        elif row < 4:
          strength = 2
        elif row < 6:
          strength = 1
        block_individual = [rect, strength]
        block_row.append(block_individual)
      self.blocks.append(block_row)

  def draw(self):
    for row in self.blocks:
      for block in row:
        color = block_red
        if block[1] == 3:
          color = block_blue
        elif block[1] == 2:
          color = block_green

        pygame.draw.rect(screen, color, block[0])
        pygame.draw.rect(screen, bg, (block[0]), 2)

  def reset(self):
    self.width = screen_width // cols
    self.height = 50
    self.create()

class Ball():
  def __init__(self, x, y):
    self.reset(x, y)

  def draw(self):
    pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

  def move(self, player, wall):
    max_speed = 5
    collision_thresh = 5
    wall_destroyed = 1

    # check collision with blocks
    row_count = 0
    for row in wall.blocks:
      block_count = 0
      for block in row:
        if self.rect.colliderect(block[0]):
          # check collision point from block
          if abs(self.rect.bottom - block[0].top) < collision_thresh and self.speed_y > 0:
            self.speed_y *= -1
          if abs(self.rect.top - block[0].bottom) < collision_thresh and self.speed_y < 0:
            self.speed_y *= -1
          if abs(self.rect.right - block[0].left) < collision_thresh and self.speed_x > 0:
            self.speed_x *= -1
          if abs(self.rect.left - block[0].right) < collision_thresh and self.speed_x < 0:
            self.speed_x *= -1
          # reduce block strength
          if wall.blocks[row_count][block_count][1] > 1:
             wall.blocks[row_count][block_count][1] -= 1
          else:
             wall.blocks[row_count][block_count][0] = (0,0,0,0)
        if wall.blocks[row_count][block_count][0] != (0,0,0,0):
          wall_destroyed = 0
        
        block_count += 1
      row_count += 1

    if wall_destroyed == 1:
      self.game_over = True
    # check collision with left-right wall
    if self.rect.left < 0 or self.rect.right > screen_width:
      self.speed_x *= -1

    # check collision with top-bottom wall
    if self.rect.top < 0:
      self.speed_y *= -1
    if self.rect.bottom > screen_height:
      self.game_over = -1

    # cehck collision with paddle
    if self.rect.colliderect(player):
      # check if colliding from top
      if abs(self.rect.bottom - player.rect.top) < collision_thresh and self.speed_y > 0:
        self.speed_y *= -1
        self.speed_x += player.direction
        if self.speed_x > max_speed:
          self.speed_x = max_speed
        elif self.speed_x < 0 and self.speed_x < -max_speed:
          self.speed_x = -max_speed
      else:
        self.speed_x *= -1

    self.rect.x += self.speed_x
    self.rect.y += self.speed_y

    return self.game_over

  def reset(self, x, y):
    self.ball_rad = 10
    self.x = x - self.ball_rad
    self.y = y
    self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
    self.speed_x = 4
    # start going up
    self.speed_y = -4
    self.game_over = 0

wall = Wall()
wall.create()
player = Paddle()
ball = Ball(player.x + (player.width  // 2), player.y - player.height )

clock = pygame.time.Clock()
fps = 60

run = True
while run:
  clock.tick(fps)
  # draw
  screen.fill(bg)
  wall.draw()
  player.draw()
  ball.draw()
  
  if live_ball:
    player.move()
    game_over = ball.move(player, wall)
    if game_over != 0:
      live_ball = False
  
  # print instructions
  if not live_ball:
    if game_over == 0:
      draw_text('Click Anywhere to Start', font, text_color, 100, screen_height // 2 + 100)
    elif game_over == 1:
      draw_text('You Won!', font, text_color, 100, screen_height // 2 + 50)
      draw_text('Click Anywhere to Play Again!', font, text_color, 100, screen_height // 2 + 100)
    elif game_over == -1:
      draw_text('You Lost!', font, text_color, 100, screen_height // 2 + 50)
      draw_text('Click Anywhere to Play Again!', font, text_color, 100, screen_height // 2 + 100)

  # event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
      live_ball = True
      ball.reset(player.x + (player.width  // 2), player.y - player.height )
      player.reset()
      wall.reset()
  # update
  pygame.display.update()

pygame.quit()