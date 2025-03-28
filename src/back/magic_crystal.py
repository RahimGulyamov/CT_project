import pygame
from src.back.images_of_proj import projectiles


class Crystal:
    def __init__(self, path_to_image, image_of_projectile, name):
        self.path_to_image = path_to_image
        self.image_of_projectile = image_of_projectile
        self.name = name
        self.image_of_crystal = None

    def set_image(self):
        if self.image_of_crystal is None:
            self.image_of_crystal = pygame.image.load(self.path_to_image).convert_alpha()
            self.image_of_crystal = pygame.transform.scale(
                self.image_of_crystal, (8, 8))


crystals = []

fire_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/orange_crystal.png", projectiles[0],
                       "Fire Crystal")
flash_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/light_crystal.png", projectiles[1],
                        "Light Crystal")
blue_fire_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/blue_crystal.png", projectiles[2],
                            "Blue Fire Crystal")
purple_fire_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/purple_crystal.png", projectiles[3],
                              "Purple Fire Crystal")
blood_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/red_crystal.png", projectiles[4],
                        "Blood Crystal")
ice_crystal = Crystal("src/tile_sets/tiles_for_chars/magic_crystals/ice_crystal.png", projectiles[5],
                      "Ice Crystal")

crystals.append(fire_crystal)
crystals.append(flash_crystal)
crystals.append(blue_fire_crystal)
crystals.append(purple_fire_crystal)
crystals.append(blood_crystal)
crystals.append(ice_crystal)
