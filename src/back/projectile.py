import pygame
from math import sqrt, pi, sin
from src.back.animation import Animation
from src.back.images_of_proj import projectiles, ImageOfProj
from src.back.magic_crystal import crystals

kSizeOfCharacter = 48
kSizeOfProjectile = 32

fireball_path = "src/tile_sets/tiles_for_chars/ranged_attack/fireball_animation/sprite_"
flash_path = "src/tile_sets/tiles_for_chars/ranged_attack/flash_animation/flash_"


class Projectile:
    def __init__(self, players_damage, players_pos, player_pos_on_screen, aim_pos, len_from_player, num_of_mineral,
                 sinnum, image_of_projectile: ImageOfProj):
        self.move_image = Animation(image_of_projectile.move_path, image_of_projectile.move_num,
                                    (kSizeOfProjectile, kSizeOfProjectile), image_of_projectile.frequency)
        self.blast_image = Animation(image_of_projectile.blast_path, image_of_projectile.blast_num,
                                     (kSizeOfCharacter, kSizeOfCharacter), image_of_projectile.frequency)
        # players_pos = (players_pos[0] + kSizeOfCharacter // 2, players_pos[1] + kSizeOfCharacter // 2)
        self.speed = 8
        # self.accel = 0
        self.damage = players_damage
        self.direction = (
            (aim_pos[0] - player_pos_on_screen[0]) / sqrt(
                (player_pos_on_screen[0] - aim_pos[0]) ** 2 + (player_pos_on_screen[1] - aim_pos[1]) ** 2),
            (aim_pos[1] - player_pos_on_screen[1]) / sqrt(
                (player_pos_on_screen[0] - aim_pos[0]) ** 2 + (player_pos_on_screen[1] - aim_pos[1]) ** 2))
        self.cur_dist = 0
        self.dist = 6000  # это просто рандомная чиселка пока что
        # self.image = pygame.Surface(
        #     (kSizeOfProjectile, kSizeOfProjectile), flags=pygame.SRCALPHA)
        # self.image.fill((0, 0, 0, 0))
        self.image_of_projectile = self.move_image.get_image()
        # self.image.blit(self.image_of_character, (0, 0))
        self.rect = self.image_of_projectile.get_rect(
            topleft=(players_pos[0] + self.direction[0] * 30 + (kSizeOfCharacter - kSizeOfProjectile) // 2,
                     players_pos[1] + self.direction[1] * 30 + (kSizeOfCharacter - kSizeOfProjectile) // 2))
        self.image_num = 0
        self.image_num_move = 0
        self.len = len_from_player if len_from_player <= self.dist else self.dist

        self.num_of_mineral = num_of_mineral
        self.sin_num = sinnum
        self.is_touch_with_rival = False

    def render(self, display, screen_position, map_position, mappa):
        if mappa.IsInCurrentRoom((self.rect.x, self.rect.y)):
            display.blit(self.image_of_projectile, (
                self.rect[0] - map_position[0] + screen_position[0],
                self.rect[1] - map_position[1] + screen_position[1]))

    def update(self, mappa, rivals=None):
        if rivals is None or rivals == []:
            rivals = []
        elif not self.is_touch_with_rival:
            for rival in rivals:
                if self.rect.colliderect(rival.rect):
                    self.is_touch_with_rival = True
                    # тут будет вызываться команда от rival, которая нанесет ему урон (дебафф)
                    rival.Hurt(self.damage)

        if self.is_touch_with_rival or self.dist - self.cur_dist < 0 or not mappa.CanStandThere(
                (round(self.rect.x) + kSizeOfProjectile // 2,
                 round(self.rect.y) + kSizeOfProjectile)):
            if self.blast_image.num_of_image >= self.blast_image.amount_of_paints * self.blast_image.frequency - 1:
                return True
            self.image_of_projectile = self.blast_image.get_image()
        else:
            # display.blit(self.image_of_projectile, self.rect)
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            if self.num_of_mineral != 0:
                delta = self.len / pi * (
                        sin(((self.cur_dist + self.speed) % (2 * self.len)) * pi / self.len) - sin(
                    (self.cur_dist % (2 * self.len)) * pi / self.len))
                self.rect.x -= self.direction[1] * delta * (-1 if self.sin_num == 0 else 1)
                self.rect.y += self.direction[0] * delta * (-1 if self.sin_num == 0 else 1)
            self.cur_dist += self.speed
            self.image_of_projectile = self.move_image.get_image()

        return False
