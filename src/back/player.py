import pygame
from src.back.Config import *
from src.back.projectile import Projectile
from src.back.staff import Staff
from src.back.animation import Animation
from src.back.personages import Personage
import time
from math import sqrt

kSizeOfDisplay = WINDOW_SIZE

kSizeOfCharacter = 48
kSpawnPosition = [kSizeOfDisplay[0] // 2, kSizeOfDisplay[1] // 2]

kOneHeartInHP = 200
kSizeOfHeart = 24
path_to_heart = "src/tile_sets/tiles_for_chars/hearts/heart_"
path_to_skeleton = "src/tile_sets/tiles_for_chars/personages/skeleton/skeleton_"
path_to_slash = "src/tile_sets/tiles_for_chars/slash/slash_"


def norm(vector):
    return sqrt(vector[0] ** 2 + vector[1] ** 2)


def normalized(vector):
    if norm(vector) != 0:
        vector[0] /= norm(vector)
        vector[1] /= norm(vector)
    return vector


class Player:
    def __init__(self, display, personage: Personage, spawn_position):
        self.personage = personage
        self.image_stat = Animation(self.personage.path_stat, self.personage.num_stat,
                                    (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.image_stat_left = Animation(self.personage.path_stat_left, self.personage.num_stat,
                                         (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.image_down = Animation(self.personage.path_down, self.personage.num_down,
                                    (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.image_up = Animation(self.personage.path_up, self.personage.num_up,
                                  (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.image_right = Animation(self.personage.path_right, self.personage.num_right,
                                     (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.image_left = Animation(self.personage.path_left, self.personage.num_left,
                                    (kSizeOfCharacter, kSizeOfCharacter), self.personage.frequency)
        self.last_move_was_left = False

        self.image_of_character = self.image_stat.get_image()

        self.rect = self.image_of_character.get_rect(topleft=spawn_position)
        # self.rect = self.image_of_character.get_rect(topleft=(1920 // 2, 1080 // 2))
        display.blit(self.image_of_character, self.rect)

        self.max_speed = 8
        # self.acceleration = 2  # ускорение
        self.direction = [0, 0]  # направление

        self.melee_attack_damage = 50  # урон ближней атакой
        self.ranged_attack_damage = 20  # урон дальней атакой
        self.max_health = 1000
        self.health_points = self.max_health
        self.health_recovery = 0.2
        self.max_magic = 100
        self.magic_points = self.max_magic
        self.magic_recovery = 0.15

        self.last_fire_slash = 0
        self.right_mouse_down = False
        self.right_mouse_up = False
        self.slash_animation = Animation(path_to_slash, 15, (2 * kSizeOfCharacter, 2 * kSizeOfCharacter), 1)

        self.fires = []  # список еще не долетевших до цели выстрелов
        self.last_fire_time = 0  # чтобы сделать ограничение на кол-во выстрелов по времени

        self.staff = Staff("src/tile_sets/tiles_for_chars/staff/staff.png", self.rect, display)
        self.sin_num = 0

        self.path_to_icon = self.personage.path_icon
        self.image_of_icon = pygame.image.load(self.path_to_icon).convert_alpha()
        self.image_of_icon = pygame.transform.scale(
            self.image_of_icon, (kSizeOfCharacter, kSizeOfCharacter))

    def SetPosition(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def GetPersonage(self):
        return self.personage

    def GetImage(self):
        return self.image_of_character

    def GetPosition(self):
        return self.rect.x, self.rect.y

    def GetCenterPosition(self):
        return self.rect.x + kSizeOfCharacter // 2, self.rect.y + kSizeOfCharacter // 2

    def GetStandPosition(self):
        return self.rect.x + kSizeOfCharacter // 2, self.rect.y + kSizeOfCharacter

    def GetSize(self):
        return self.rect.size

    def ChangePosition(self, vector):
        self.rect.x += vector[0]
        self.rect.y += vector[1]

    def move(self, mappa, render):
        self.direction = [0, 0]

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.direction[1] -= 1
            self.staff.diff_with_players_x_num = 0

        if key[pygame.K_a]:
            self.direction[0] -= 1
            self.staff.diff_with_players_x_num = 0

        if key[pygame.K_s]:
            self.direction[1] += 1
            self.staff.diff_with_players_x_num = 1

        if key[pygame.K_d]:
            self.direction[0] += 1
            self.staff.diff_with_players_x_num = 1

        if self.direction != [0, 0]:
            self.direction = normalized(self.direction)
            self.direction[0] *= self.max_speed
            self.direction[1] *= self.max_speed
        else:
            self.staff.diff_with_players_x_num = 1

        self.direction[0] = round(self.direction[0])
        self.direction[1] = round(self.direction[1])

        if self.direction[0] < 0 and not mappa.CanStandThere(
                (self.rect.x + self.direction[0], self.rect.y + kSizeOfCharacter)):
            self.direction[0] = 0

        elif self.direction[0] > 0 and not mappa.CanStandThere(
                (self.rect.x + kSizeOfCharacter + self.direction[0], self.rect.y + kSizeOfCharacter)):
            self.direction[0] = 0

        if self.direction[1] < 0:
            if not mappa.CanStandThere(
                    (self.rect.x, self.rect.y + kSizeOfCharacter - 8 + self.direction[1])) or not mappa.CanStandThere(
                (self.rect.x + kSizeOfCharacter,
                 self.rect.y + kSizeOfCharacter - 8 + self.direction[1])):
                self.direction[1] = 0
        elif self.direction[1] > 0:
            if not mappa.CanStandThere(
                    (self.rect.x, self.rect.y + kSizeOfCharacter + self.direction[1])) or not mappa.CanStandThere(
                (self.rect.x + kSizeOfCharacter,
                 self.rect.y + kSizeOfCharacter + self.direction[1])):
                self.direction[1] = 0

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        # mini_map.MoveMiniMap([-self.direction[0], -self.direction[1]])

        if self.direction == [0, 0]:
            if self.last_move_was_left:
                self.image_of_character = self.image_stat_left.get_image()
            else:
                self.image_of_character = self.image_stat.get_image()

        elif self.direction[0] > 0:
            self.image_of_character = self.image_right.get_image()
            self.last_move_was_left = False

        elif self.direction[0] < 0:
            self.image_of_character = self.image_left.get_image()
            self.last_move_was_left = True

        elif self.direction[1] > 0:
            self.image_of_character = self.image_down.get_image()

        elif self.direction[1] < 0:
            self.image_of_character = self.image_up.get_image()

        render.ChangePositionOfPlayerAccordingToMoveBox(self.direction)

    def ranged_attack(self, screen_position, mouse):
        # self.left_mouse_up = not pygame.mouse.get_pressed()[0]
        if self.magic_points >= 5:  # self.left_mouse_up and
            # mouse = pygame.mouse.get_pos()  # self.left_mouse_down and (time.time()-self.last_fire_time) > 0.3
            len_from_player = sqrt((screen_position[0] - mouse[0]) ** 2 + (screen_position[1] - mouse[1]) ** 2)
            for i, crystal in enumerate(self.staff.crystals):
                if crystal is not None:
                    self.fires.append(Projectile(self.ranged_attack_damage,
                                                 (self.rect.x, self.rect.y), screen_position, mouse, len_from_player, i,
                                                 self.sin_num, crystal.image_of_projectile))
                    if i != 0:
                        self.sin_num += 1
                        self.sin_num %= 2

            self.last_fire_time = time.time()
            self.left_mouse_up = False
            # self.left_mouse_down = False
            self.magic_points -= 5

        # self.left_mouse_down = pygame.mouse.get_pressed()[0]

    def melee_attack(self, rivals=None):  # display, mappa
        self.right_mouse_up = not pygame.mouse.get_pressed()[2]

        if self.slash_animation.num_of_image == 0 and self.right_mouse_up and self.right_mouse_down and \
                (time.time() - self.last_fire_slash) > 0.3:
            self.right_mouse_up = False
            # self.right_mouse_down = False
            self.last_fire_slash = time.time()

            image_of_slash = self.slash_animation.get_image()
            slash_rect = image_of_slash.get_rect(
                topleft=(self.rect[0] - kSizeOfCharacter // 2, self.rect[1] - kSizeOfCharacter // 2))
            # display.blit(image_of_slash, slash_rect)

            if rivals is None or not rivals:
                return
            else:
                for rival in rivals:
                    if slash_rect.colliderect(rival.rect):
                        # тут будет передаваться урон мобу
                        rival.Hurt(self.melee_attack_damage)

        self.right_mouse_down = pygame.mouse.get_pressed()[2]

    def health_icon(self, display):
        full_hearts = int(self.health_points // kOneHeartInHP)
        is_mode_null = self.health_points % kOneHeartInHP == 0
        num_of_not_full_heart = 4 - ((self.health_points % kOneHeartInHP) * 5 // kOneHeartInHP)
        empty_hearts = self.max_health // kOneHeartInHP - full_hearts

        x = 100
        y = 15

        for i in range(full_hearts):
            image_path = path_to_heart + "0" + ".png"
            image_of_heart = pygame.image.load(image_path).convert_alpha()
            image_of_heart = pygame.transform.scale(
                image_of_heart, (kSizeOfHeart, kSizeOfHeart))
            display.blit(image_of_heart, (x, y))
            x += kSizeOfHeart * 5 // 4
        if not is_mode_null:
            image_path = path_to_heart + str(int(num_of_not_full_heart)) + ".png"
            image_of_heart = pygame.image.load(image_path).convert_alpha()
            image_of_heart = pygame.transform.scale(
                image_of_heart, (kSizeOfHeart, kSizeOfHeart))
            display.blit(image_of_heart, (x, y))
            x += kSizeOfHeart * 5 // 4
            empty_hearts -= 1
        if empty_hearts != 0:
            for i in range(empty_hearts):
                image_path = path_to_heart + "4" + ".png"
                image_of_heart = pygame.image.load(image_path).convert_alpha()
                image_of_heart = pygame.transform.scale(
                    image_of_heart, (kSizeOfHeart, kSizeOfHeart))
                display.blit(image_of_heart, (x, y))
                x += kSizeOfHeart * 5 // 4

    @staticmethod
    def personage_icon(self, display):
        display.blit(self.image_of_icon, (26, 10))

    def mp_icon(self, display):
        path_to_mp_icon = "src/tile_sets/tiles_for_chars/MP_icon.png"
        width = round(self.magic_points / self.max_magic * 215)
        pygame.draw.rect(display, (20, 160, 255), (93, 47, width, 20))
        image_of_mp_icon = pygame.image.load(path_to_mp_icon).convert_alpha()
        image_of_mp_icon = pygame.transform.scale(
            image_of_mp_icon, (240, 24))
        display.blit(image_of_mp_icon, (80, 45))

    def render(self, display, position, mappa):
        display.blit(self.image_of_character, position)
        self.staff.render(display, pygame.Rect(position[0], position[1], kSizeOfCharacter, kSizeOfCharacter))
        # self.ranged_attack(display, mappa)
        # self.melee_attack(display)
        self.health_icon(display)
        self.personage_icon(self, display)
        self.mp_icon(display)
        if self.magic_points <= self.max_magic - self.magic_recovery:
            self.magic_points += self.magic_recovery
        if self.health_points <= self.max_health - self.health_recovery:
            self.health_points += self.health_recovery
        if self.fires:
            for (i, fire) in enumerate(self.fires):
                if fire.render(display, position, (self.rect.x, self.rect.y), mappa):
                    self.fires.pop(i)

        if self.slash_animation.num_of_image > 0:
            image_of_slash = self.slash_animation.get_image()
            display.blit(image_of_slash, (position[0] - kSizeOfCharacter // 2, position[1] - kSizeOfCharacter // 2))

    def update(self, mappa, render, rivals=None):
        self.move(mappa, render)
        self.melee_attack(rivals)
        # self.ranged_attack(render.GetPlayerPositionOnTheScreen())
        if self.fires:
            for i, fire in enumerate(self.fires):
                if fire.update(mappa, rivals):
                    self.fires.pop(i)

    def is_alive(self):
        return self.health_points > 0

    def Hurt(self, damage):
        self.health_points -= damage
        pass
