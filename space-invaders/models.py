import pygame
from pygame.locals import *

class Player():
  def __init__(self, surface):
    self.bullets = []
    self.surface = surface
    self.color = (0,255,0)
    self.width = 30
    self.height = 30
    self.x = (self.surface.get_width() // 2) - (self.width // 2)
    self.y = self.surface.get_height() - self.height * 2
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.speed = 5
    self.last_shot = pygame.time.get_ticks()

  def draw(self):
    pygame.draw.rect(self.surface, self.color, self.rect)
    for bullet in self.bullets:
      bullet.update()
      

  def update(self):
    bullet_cooldown = 500

    self.draw()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= self.speed
    elif key[pygame.K_RIGHT] and self.rect.right < self.surface.get_width():
      self.rect.x += self.speed

    time_now = pygame.time.get_ticks()
    if key[pygame.K_SPACE] and (time_now - self.last_shot ) > bullet_cooldown:
      bullet = Bullet(self.surface, self.rect.centerx, self.rect.top)
      self.bullets.append(bullet)
      self.last_shot = time_now

class Bullet():
  def __init__(self, surface, x, y):
    self.surface = surface
    self.color = (0,255,255)
    self.width = 5
    self.height = 8
    self.x = x - self.width // 2
    self.y = y
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.speed = -8

  def draw(self):
    pygame.draw.rect(self.surface, self.color, self.rect)

  def update(self):
    self.draw()
    self.rect.move_ip(0, self.speed) 

class Alien():
  def __init__(self, surface, x, y):
    self.bullets = []
    self.surface = surface
    self.color = (255,0,0)
    self.width = 30
    self.height = 30
    self.x = x
    self.y = y
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.speed = 1
    self.direction = 1

  def draw(self):
    pygame.draw.rect(self.surface, self.color, self.rect)
    for bullet in self.bullets:
      bullet.update()

  def update(self):
    self.draw()
    self.rect.move_ip(self.speed * self.direction, 0)
    move_tresh = self.width // 2
    if self.rect.right > (self.x + self.width + move_tresh):
      self.direction *= -1
    elif self.rect.left < (self.x - self.width - move_tresh):
      self.direction *= -1

class AlienBullet():
  def __init__(self, surface, x, y):
    self.surface = surface
    self.color = (255,0,255)
    self.width = 5
    self.height = 5
    self.x = x - self.width // 2
    self.y = y
    self.rect = Rect(self.x, self.y, self.width, self.height)
    self.speed = 2

  def draw(self):
    pygame.draw.rect(self.surface, self.color, self.rect)

  def update(self):
    self.draw()
    self.rect.move_ip(0, self.speed)