import pygame
from pygame.locals import *

pygame.init()

# screen dimensions
screen_width = 600
screen_height = 500

# create window
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# game variables
live_ball = False
margin = 50
enemy_score = 0
player_score = 0
fps = 60
winner = 0
speed_increase = 0

# game colors
bg = (50, 25, 50)
text_color = (149, 197, 172)
paddle_color = (149, 197, 172)

# obj sizes
paddle_size = [30, 40]
ball_size = 14

# obj positions
ball_pos = [0,0]
player_pos = [0,0]
enemy_pos = [0,0]

# fonts
font = pygame.font.SysFont('Grand9k Pixel', 15)

# classes
class Paddle():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.rect = Rect(self.x, self.y, 20, 100)
    self.speed = 5

  def move(self):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and self.rect.top > margin:
      # move up
      self.rect.move_ip(0, -1 * self.speed)
    elif key[pygame.K_DOWN] and self.rect.bottom < screen_height:
      # move down
      self.rect.move_ip(0, self.speed)
 
  def draw(self):
    pygame.draw.rect(screen, paddle_color, self.rect)

  def ai(self):
    # align center with ball
    # move down
    if self.rect.centery < pong_ball.rect.top and self.rect.bottom < screen_height:
      self.rect.move_ip(0, self.speed)
    # move up
    if self.rect.centery > pong_ball.rect.bottom and self.rect.top > margin:
      self.rect.move_ip(0, -1 * self.speed)
    
class Ball():
  def __init__(self, x, y):
    self.reset(x, y)
  
  def move(self):
    # collision detection
    if self.rect.top < margin:
      self.speed_y *= -1
    elif self.rect.bottom > screen_height:
      self.speed_y *= -1
    
    # check collision
    if self.rect.colliderect(player_paddle) or self.rect.colliderect(enemy_paddle):
      self.speed_x *= -1
   

    # check for out of bounds
    if self.rect.left < 0:
      self.winner = 1
    elif self.rect.right > screen_width:
      self.winner = -1

    # update position
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y

    return self.winner

  def draw(self):
    pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

  def reset(self, x, y):
    self.x = x
    self.y = y
    self.ball_rad = 8
    self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
    self.speed_x = -4
    self.speed_y = 4
    self.winner = 0 # 1 is player, -1 is enemy


# create paddles
player_paddle = Paddle(screen_width - 40, screen_height // 2)
enemy_paddle = Paddle(20, screen_height // 2)

# creat pong ball
pong_ball = Ball(screen_width - 60, screen_height // 2 + 50)

# functions
def draw_board():
  screen.fill(bg)
  pygame.draw.line(screen, text_color, (0, margin), (screen_width, margin))

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_score():
  draw_text('Enemy: '+ str(enemy_score), font, text_color, 10, 10)
  draw_text('Player: '+ str(player_score), font, text_color, screen_width - 100, 10)

def draw_ball():
  pong_ball.draw()

def draw_paddles():
  player_paddle.draw()
  enemy_paddle.draw()

def check_score(winner):
  global player_score
  global enemy_score

  if winner == -1:
    enemy_score += 1
  elif winner == 1:
    player_score += 1

# run loop
run = True
while run:
  fpsClock.tick(fps)
  # draw loop
  draw_board()
  draw_score()
  draw_text('BALL SPEED: ' + str(abs(pong_ball.speed_x)), font, text_color, screen_width // 2 - 60, 15)
  draw_paddles()

  if live_ball:
    speed_increase += 1
    # move ball
    winner = pong_ball.move()
    if winner == 0:
      # move paddle
      player_paddle.move()
      enemy_paddle.ai()
      draw_ball()
    else:
      live_ball = False
      check_score(winner)

  # print player instructions
  if live_ball == False:
    if winner == 0:
      draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 - 100)
    elif winner == 1:
      draw_text('YOU SCORED', font, text_color, 100, screen_height // 2 - 100)
      draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 - 50)
    elif winner == -1:
      draw_text('ENEMY SCORED', font, text_color, 100, screen_height // 2 - 100)
      draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 - 50)


  # event loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    elif event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
      live_ball = True
      pong_ball.reset(screen_width - 60, screen_height // 2 + 50)

  if speed_increase > 500:
    speed_increase = 0
    if pong_ball.speed_x < 0:
      pong_ball.speed_x -= 1
    elif pong_ball.speed_x > 0:
      pong_ball.speed_x += 1
    if pong_ball.speed_y < 0:
      pong_ball.speed_y -= 1
    elif pong_ball.speed_y > 0:
      pong_ball.speed_y += 1
  # update screewn
  pygame.display.update()

pygame.quit()
