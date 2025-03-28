import pygame
from src.back.projectile import Projectile
import time
from src.back.magic_crystal import crystals

list_of_coord = ((0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (7, 4), (9, 4), (11, 4),
                 (12, 4), (14, 4), (16, 4), (18, 4), (20, 3), (21, 2), (22, 1), (23, 0))

kSizeOfStaff = (32, 48)


class Staff:
    def __init__(self, path_to_staff, players_rect, display):
        self.path_to_staff = path_to_staff
        self.staff_y = 0
        self.staff_delta = 1
        self.diff_with_players_x = (28, -12)
        self.diff_with_players_x_num = 1

        self.image_of_staff = pygame.image.load(self.path_to_staff).convert_alpha()
        self.image_of_staff = pygame.transform.scale(
            self.image_of_staff, kSizeOfStaff)
        display.blit(self.image_of_staff,
                     (players_rect[0] + self.diff_with_players_x[self.diff_with_players_x_num],
                      players_rect[1] + self.staff_y))

        self.num_of_crystals = 0
        self.coord_y_of_crystals = (6, 14, 26)
        self.list_of_crystal_num = [0, 10, 5]
        self.crystal_delta = [1, 1, 1]
        self.crystals = [None, None, None]

        for i, crystal in enumerate(self.crystals):
            if crystal is not None:
                crystal.set_image()
                display.blit(crystal.image_of_crystal, (
                    players_rect[0] + self.diff_with_players_x[self.diff_with_players_x_num],
                    players_rect[1] + self.staff_y + self.coord_y_of_crystals[i]))

    def blit_mineral(self, display, players_rect, diff_with_players_x_num, i):
        if self.crystals[i] is not None:
            self.crystals[i].set_image()
            display.blit(self.crystals[i].image_of_crystal,
                         (players_rect[0] + self.diff_with_players_x[diff_with_players_x_num] +
                          list_of_coord[self.list_of_crystal_num[i] // 3][0],
                          players_rect[1] + self.staff_y + self.coord_y_of_crystals[i] +
                          list_of_coord[self.list_of_crystal_num[i] // 3][
                              1]))

    def render(self, display, players_rect):
        for i, crystal in enumerate(self.crystals):
            if self.crystal_delta[i] == -1 and crystal is not None:
                self.blit_mineral(display, players_rect, self.diff_with_players_x_num, i)

        display.blit(self.image_of_staff, (players_rect[0] + self.diff_with_players_x[self.diff_with_players_x_num],
                                           players_rect[1] + self.staff_y // 2))
        if abs(self.staff_y) >= 20:
            self.staff_delta *= -1
        self.staff_y += self.staff_delta
        for i, crystal in enumerate(self.crystals):
            if crystal is not None:
                if self.crystal_delta[i] == 1:
                    self.blit_mineral(display, players_rect, self.diff_with_players_x_num, i)

                self.list_of_crystal_num[i] += (self.crystal_delta[i] * (-1 if i == 1 else 1))
                if self.list_of_crystal_num[i] == 45 or self.list_of_crystal_num[i] == 0:
                    self.crystal_delta[i] *= -1

    def add_crystal(self, crystal):
        for i, crystall in enumerate(self.crystals):
            if crystall is None:
                self.crystals[i] = crystal
                self.num_of_crystals += 1
                break

    def delete_crystal(self, crystal_num):
        self.crystals[crystal_num] = None
        self.num_of_crystals -= 1
