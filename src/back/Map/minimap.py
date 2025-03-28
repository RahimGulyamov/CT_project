import pygame
from src.back.constants_with_paths_to_files import *
from src.back.Map.map import Map
from src.back.Map.constants_for_map import *
from src.back.Config import *
import math


class MiniMap:
    def __init__(self):
        self.map_for_minimap = pygame.Surface(
            (SIZE_OF_MAP[0] * SIZE_OF_TILE_ON_MINI_MAP, SIZE_OF_MAP[1] * SIZE_OF_TILE_ON_MINI_MAP),
            flags=pygame.SRCALPHA)
        self.map_for_minimap.fill((0, 0, 0, 0))

        self.mini_map = pygame.Surface(SIZE_OF_MINI_MAP, flags=pygame.SRCALPHA)
        self.mini_map.fill((0, 0, 0, 0))

        self.mini_map_position = [0, 0]
        self.position_of_minimap_on_screen = POSITION_OF_MINI_MAP
        self.size_of_mini_map = SIZE_OF_MINI_MAP
        self.is_tabed = False

    def BlitImageOnMiniMap(self, image, position_on_the_map):
        position = [math.ceil(position_on_the_map[0] * MINI_MAP_SCALE),
                    math.ceil(position_on_the_map[1] * MINI_MAP_SCALE)]
        image = pygame.transform.scale(image, (SIZE_OF_ITEM_ON_MINI_MAP, SIZE_OF_ITEM_ON_MINI_MAP))
        self.map_for_minimap.blit(image, position)

    def BlitOnMiniMap(self, tiles_for_blit):
        Map.BlitSpecificTilesOnSurface(self.map_for_minimap, tiles_for_blit, SIZE_OF_TILE_ON_MINI_MAP)

    def RenderMiniMap(self, display):
        self.mini_map.fill((0, 0, 0, 0))
        self.mini_map.blit(self.map_for_minimap, self.mini_map_position)
        image_for_icon = pygame.image.load(PATH_TO_CHARACTER_ON_MINI_MAP)
        image_for_icon = pygame.transform.scale(image_for_icon, SIZE_OF_ICON_ON_MINIMAP)
        self.mini_map.blit(image_for_icon, (self.size_of_mini_map[0] // 2 - SIZE_OF_ICON_ON_MINIMAP[0] // 2,
                                            self.size_of_mini_map[1] // 2 - SIZE_OF_ICON_ON_MINIMAP[1] // 2))
        display.blit(self.mini_map, self.position_of_minimap_on_screen)

    def ExtendMiniMap(self):
        self.mini_map = pygame.Surface(SIZE_OF_TABED_MINIMAP, flags=pygame.SRCALPHA)
        self.mini_map.fill((0, 0, 0, 0))

        self.mini_map.set_alpha(180)
        self.position_of_minimap_on_screen = POSITION_OF_TABED_MINIMAP
        self.size_of_mini_map = SIZE_OF_TABED_MINIMAP
        self.mini_map_position[0] += (SIZE_OF_TABED_MINIMAP[0] - SIZE_OF_MINI_MAP[0]) // 2
        self.mini_map_position[1] += (SIZE_OF_TABED_MINIMAP[1] - SIZE_OF_MINI_MAP[1]) // 2

    def ShrinkMiniMap(self):
        self.mini_map = pygame.Surface(SIZE_OF_MINI_MAP, flags=pygame.SRCALPHA)
        self.mini_map.fill((0, 0, 0, 0))
        self.mini_map.set_alpha(255)
        self.position_of_minimap_on_screen = POSITION_OF_MINI_MAP
        self.size_of_mini_map = SIZE_OF_MINI_MAP
        self.mini_map_position[0] -= (SIZE_OF_TABED_MINIMAP[0] - SIZE_OF_MINI_MAP[0]) // 2
        self.mini_map_position[1] -= (SIZE_OF_TABED_MINIMAP[1] - SIZE_OF_MINI_MAP[1]) // 2

    def ProcessEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.mini_map.get_size() == SIZE_OF_MINI_MAP:
                    self.is_tabed = True
                    self.ExtendMiniMap()
                else:
                    self.is_tabed = False
                    self.ShrinkMiniMap()

    def MoveMiniMap(self, vector):
        self.mini_map_position[0] += vector[0] * SIZE_OF_TILE_ON_MINI_MAP / SIZE_OF_TILE
        self.mini_map_position[1] += vector[1] * SIZE_OF_TILE_ON_MINI_MAP / SIZE_OF_TILE

    def SetStartPosition(self, position):
        self.mini_map_position = [position[0] * SIZE_OF_TILE_ON_MINI_MAP + SIZE_OF_MINI_MAP[0] // 2,
                                  position[1] * SIZE_OF_TILE_ON_MINI_MAP + SIZE_OF_MINI_MAP[1] // 2]
