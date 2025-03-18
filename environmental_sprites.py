import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x ,y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))


class Level_One():
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.tile_size = 16
        ROWS, COLS = 12, 16
        self.TILE_WIDTH, self.TILE_HEIGHT = SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS
        self.dir = "/home/tasberry/Documents/PyCharm/Pygame/Environmental Sprites/NES - Contra - Stage 3.png"
        self.sheet = pygame.image.load(self.dir)
        self.floor_tiles = ["G"]
        self.tile_map = {
                         "Z": self.get_tile("Z", self.sheet, self.tile_size,self.TILE_WIDTH, self.TILE_HEIGHT),  # Gray Rock1
                         "X": self.get_tile("X", self.sheet, self.tile_size,self.TILE_WIDTH, self.TILE_HEIGHT),  # Gray Rock2
                         "C": self.get_tile("C", self.sheet, self.tile_size,self.TILE_WIDTH, self.TILE_HEIGHT),  # Gray Rock3
                         "V": self.get_tile("V", self.sheet, self.tile_size,self.TILE_WIDTH, self.TILE_HEIGHT),  # Gray Rock4
                         "G": self.get_tile("G", self.sheet, self.tile_size,self.TILE_WIDTH, self.TILE_HEIGHT),  # Grass
                                                                                         }

        self.level = self.load_level("/home/tasberry/Documents/PyCharm/Pygame/Level_One.txt")


    def get_tile(self, char, sheet, tile_size, new_width, new_height):
        if char == "Z":
            return rock1(sheet, tile_size, new_width, new_height)

        if char == "X":
            return rock2(sheet, tile_size, new_width, new_height)

        if char == "C":
            return rock3(sheet, tile_size, new_width, new_height)

        if char == "V":
            return rock4(sheet, tile_size, new_width, new_height)

        if char == "G":
            return grass(sheet, tile_size, new_width, new_height)



    def load_level(self, filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f]


class grass(pygame.sprite.Sprite):
    def __init__(self,sheet, tile_size, new_width, new_height):
        super().__init__()
        self.x = 6
        self.y = 0
        self.image = pygame.Surface((new_width, new_height))
        self.image = sheet.subsurface(pygame.Rect(self.x*tile_size, self.y * tile_size, tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

class rock1(pygame.sprite.Sprite):
    def __init__(self,sheet, tile_size, new_width, new_height):
        super().__init__()
        self.x = 7
        self.y = 2
        self.image = pygame.Surface((new_width, new_height))
        self.image = sheet.subsurface(pygame.Rect(self.x*tile_size, self.y * tile_size, tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

class rock2(pygame.sprite.Sprite):
    def __init__(self,sheet, tile_size, new_width, new_height):
        super().__init__()
        self.x = 8
        self.y = 2
        self.image = pygame.Surface((new_width, new_height))
        self.image = sheet.subsurface(pygame.Rect(self.x*tile_size, self.y * tile_size, tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

class rock3(pygame.sprite.Sprite):
    def __init__(self,sheet, tile_size, new_width, new_height):
        super().__init__()
        self.x = 9
        self.y = 2
        self.image = pygame.Surface((new_width, new_height))
        self.image = sheet.subsurface(pygame.Rect(self.x*tile_size, self.y * tile_size, tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

class rock4(pygame.sprite.Sprite):
    def __init__(self,sheet, tile_size, new_width, new_height):
        super().__init__()
        self.x = 10
        self.y = 2
        self.image = pygame.Surface((new_width, new_height))
        self.image = sheet.subsurface(pygame.Rect(self.x*tile_size, self.y * tile_size, tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))