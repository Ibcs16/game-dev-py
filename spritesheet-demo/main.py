import pygame
import spritesheet 

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spritesheets")

# colors
bg = (50, 50, 50)
black = (0,0,0)

# assets
sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# game variables
animation_list = []
animation_steps = [4, 6, 3, 4]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 250 # how fast animation will play
current_frame = 0
step_counter = 0

for animation in animation_steps:
  temp_img_list = []
  for _ in range(animation):
    temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, black))
    step_counter += 1
  animation_list.append(temp_img_list)

# fonts

# functions
def draw_character():
  screen.blit(animation_list[action][current_frame], (0,0))
  pass

# game loop
run = True
while run:
  screen.fill(bg)

  # update animation
  current_time = pygame.time.get_ticks()
  if current_time - last_update >= animation_cooldown:
    current_frame += 1
    last_update = current_time
    if current_frame >= len(animation_list[action]):
      current_frame = 0
  # show frame image
  draw_character()


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN and action > 0:
        action -= 1
        current_frame = 0
      elif event.key == pygame.K_UP and action < len(animation_list) - 1:
        action += 1
        current_frame = 0

  pygame.display.update()

pygame.quit()