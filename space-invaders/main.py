import pygame 
from pygame.locals import *
import models
import random

screen_width = 500
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

bg = pygame.image.load('assets/bg.png')

bullets = []
player = models.Player(screen)

enemies_col = 4
enemies_row = 3
enemies = []

last_alien_shot = pygame.time.get_ticks()
alien_cooldown = 100

fpsClock = pygame.time.Clock()
fps = 60

def draw_bg():
  screen.blit(bg,(0,0))

def create_enemies():
  for row in range(enemies_row):
    for enemy_col in range(enemies_col):
      pos_x = 100 + enemy_col * 100
      pos_y = 100 + row * 70
      enemies.append(models.Alien(screen, pos_x, pos_y))

create_enemies()

def draw_enemies():
  for enemy in enemies:
    enemy.update()

run = True
while run:
  fpsClock.tick(fps)
  draw_bg()
  
  player.draw()
  draw_enemies()

  # create random alien bullets
  time_now = pygame.time.get_ticks()
  if time_now - last_alien_shot > alien_cooldown:
    picked_alien = random.choice(enemies)
    picked_alien.bullets.append(models.AlienBullet(picked_alien.surface, picked_alien.rect.centerx, picked_alien.rect.bottom))
    last_alien_shot = time_now

  player.update()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()