import pygame
import sys
import random
import player
from settings import *
from environmental_sprites import *

import camera

# Init Settings
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

clock = pygame.time.Clock()

# Player Settings
tim = player.player()

platforms = pygame.sprite.Group()
#ground = Platform(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40)
#floating_platform = Platform(300, 400, 200, 20)

level_sprites = pygame.sprite.Group()

# Enemy Settings
enemy_width = ENEMY_WIDTH
enemy_height = ENEMY_HEIGHT
enemy_x = ENEMY_X
enemy_y = ENEMY_Y
enemy_speed = ENEMY_SPEED

all_sprites = pygame.sprite.Group()


game_over = False

level_one = Level_One()
tile_width = len(level_one.level[0])
tile_height = len(level_one.level)
map_width = level_one.TILE_WIDTH * tile_width
map_height = level_one.TILE_HEIGHT* tile_height
camera = camera.Camera(map_width, map_height)

def draw_map():
    global level_one
    for row_index, row in enumerate(level_one.level):
        for col_index, tile_char in enumerate(row):
            if tile_char in level_one.tile_map:
                rect_y = row_index * level_one.TILE_HEIGHT
                rect_x = col_index * level_one.TILE_WIDTH
                if tile_char == "G":
                    platforms.add(grass(level_one.sheet,rect_x, rect_y,level_one.tile_size,level_one.TILE_WIDTH,level_one.TILE_HEIGHT))
                    level_sprites.add(grass(level_one.sheet, rect_x, rect_y, level_one.tile_size, level_one.TILE_WIDTH,
                                        level_one.TILE_HEIGHT))
                if tile_char == "Z":
                    level_sprites.add(rock1(level_one.sheet, rect_x, rect_y, level_one.tile_size, level_one.TILE_WIDTH,
                                            level_one.TILE_HEIGHT))
                if tile_char == "X":
                    level_sprites.add(rock2(level_one.sheet, rect_x, rect_y, level_one.tile_size, level_one.TILE_WIDTH,
                                            level_one.TILE_HEIGHT))
                if tile_char == "C":
                    level_sprites.add(rock3(level_one.sheet, rect_x, rect_y, level_one.tile_size, level_one.TILE_WIDTH,
                                            level_one.TILE_HEIGHT))
                if tile_char == "V":
                    level_sprites.add(rock4(level_one.sheet, rect_x, rect_y, level_one.tile_size, level_one.TILE_WIDTH,
                                            level_one.TILE_HEIGHT))
                #all_sprites.add(tile_image)
# Main Loop
def main():
    global enemy_x, enemy_y, game_over
    draw_map()
    all_sprites.add(tim, tim.bullets)
    while True:
        #Checks for quit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()

            tim.update(keys, platforms)
            camera.update(tim)

            enemy_y += enemy_speed
            if enemy_y > SCREEN_HEIGHT:
                enemy_y = 0
                enemy_x = random.randint(0,SCREEN_WIDTH - enemy_width)

            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

        screen.fill(WHITE)
        for sprite in level_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in tim.bullets:
            screen.blit(sprite.image, camera.apply(sprite))


        camera.update(tim)
        #pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))


        pygame.display.flip() #Updates screen
        clock.tick(FPS) #Frame Rate

if __name__ == "__main__":
    main()