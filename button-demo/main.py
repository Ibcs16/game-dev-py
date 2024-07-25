import pygame
import button

pygame.init()
# create window
screen_height = 500
screen_width = 800

# set game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Button Demo')

# load button assets
start_img = pygame.image.load('button-demo/start_btn.png').convert_alpha()
exit_img = pygame.image.load('button-demo/exit_btn.png').convert_alpha()


# create button instances
start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(450, 200, exit_img, 0.8)

# game loop
run = True
while run:
  screen.fill((202, 228, 241))

  if start_button.draw(screen):
    print('start')
  if exit_button.draw(screen):
    run = False

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()