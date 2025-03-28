from abc import ABC, abstractmethod

from src.back.enemy_personages import EnemyPersonage, enemy_personages
from src.back.Config import *
from src.back.animation import Animation
import time
import math
from src.back.projectile import Projectile
from src.back.images_of_proj import projectiles
from src.back.player import kSizeOfCharacter, path_to_slash


class Enemy:
    def __init__(self, position, enemy_personage: EnemyPersonage):
        self.spawn_position = position
        self.direction_of_movement = None
        self.num_of_frames_with_movement = 0

        self.enemy_personage = enemy_personage.personage
        self.health = enemy_personage.health
        self.size = enemy_personage.size
        self.image_stat = Animation(enemy_personage.personage.path_stat, enemy_personage.personage.num_stat,
                                    (enemy_personage.size, enemy_personage.size), enemy_personage.personage.frequency)
        self.image_stat_left = Animation(enemy_personage.personage.path_stat_left, enemy_personage.personage.num_stat,
                                         (enemy_personage.size, enemy_personage.size),
                                         enemy_personage.personage.frequency)
        self.image_down = Animation(enemy_personage.personage.path_down, enemy_personage.personage.num_down,
                                    (enemy_personage.size, enemy_personage.size), enemy_personage.personage.frequency)
        self.image_up = Animation(enemy_personage.personage.path_up, enemy_personage.personage.num_up,
                                  (enemy_personage.size, enemy_personage.size), enemy_personage.personage.frequency)
        self.image_right = Animation(enemy_personage.personage.path_right, enemy_personage.personage.num_right,
                                     (enemy_personage.size, enemy_personage.size), enemy_personage.personage.frequency)
        self.image_left = Animation(enemy_personage.personage.path_left, enemy_personage.personage.num_left,
                                    (enemy_personage.size, enemy_personage.size), enemy_personage.personage.frequency)
        self.image_death_right = Animation(enemy_personage.personage.path_death_right,
                                           enemy_personage.personage.num_death,
                                           (enemy_personage.size, enemy_personage.size),
                                           enemy_personage.personage.frequency)
        self.image_death_left = Animation(enemy_personage.personage.path_death_left,
                                          enemy_personage.personage.num_death,
                                          (enemy_personage.size, enemy_personage.size),
                                          enemy_personage.personage.frequency)

        self.last_move_was_left = False

        self.image_of_character = self.image_stat.get_image()

        self.rect = self.image_of_character.get_rect(topleft=position)

        self.speed = 2
        self.sleep_speed = 1

    def SleepMove(self):
        if self.num_of_frames_with_movement > 0:
            self.rect[0] += self.direction_of_movement[0]
            self.rect[1] += self.direction_of_movement[1]
            self.num_of_frames_with_movement = max(self.num_of_frames_with_movement - 1, 0)
            self.SetImage()

    def SetImage(self):
        if self.direction_of_movement == [0, 0]:
            if self.last_move_was_left:
                self.image_of_character = self.image_stat_left.get_image()
            else:
                self.image_of_character = self.image_stat.get_image()

        elif self.direction_of_movement[0] > 0:
            self.image_of_character = self.image_right.get_image()
            self.last_move_was_left = False

        elif self.direction_of_movement[0] < 0:
            self.image_of_character = self.image_left.get_image()
            self.last_move_was_left = True

        elif self.direction_of_movement[1] > 0:
            self.image_of_character = self.image_down.get_image()

        elif self.direction_of_movement[1] < 0:
            self.image_of_character = self.image_up.get_image()

    def StopMovement(self):
        self.num_of_frames_with_movement = 0

    def GetDirectionOfMovement(self):
        return self.direction_of_movement

    def IsMove(self):
        return self.num_of_frames_with_movement > 0

    def SetDirectionOfMovement(self, direction, num_of_frames):
        self.num_of_frames_with_movement = num_of_frames
        self.direction_of_movement = direction

    def GetCenter(self):
        return self.rect[0] + self.size // 2, self.rect[1] + self.size // 2

    def GetPosition(self):
        return self.rect[0], self.rect[1]

    def SetPosition(self, position):
        self.rect[0], self.rect[1] = position

    def GetPointsOfMovement(self):
        lst = [[self.rect[0], self.rect[1] + self.size // 2],
               [self.rect[0] + self.size, self.rect[1] + self.size],
               [self.rect[0], self.rect[1] + self.size],
               [self.rect[0] + self.size, self.rect[1] + self.size // 2]]
        return lst

    def render(self, display, screen_position, map_position, mappa):
        display.blit(self.image_of_character, (
            self.rect[0] - map_position[0] + screen_position[0],
            self.rect[1] - map_position[1] + screen_position[1]))

    def Hurt(self, damage):
        self.health -= damage

    def IsAlive(self):
        return self.health > 0

    @abstractmethod
    def Attack(self, *args):
        pass


class MeleeEnemy(Enemy):
    def __init__(self, position, enemy_personage: EnemyPersonage):
        super().__init__(position, enemy_personage)
        self.last_fire_slash = 0
        self.slash_animation = Animation(path_to_slash, 15, (2 * self.size, 2 * self.size), 1)
        self.melee_attack_damage = 50

    def Attack(self, player):
        distance = math.sqrt(
            (self.rect[0] - player.rect[0]) ** 2 + (self.rect[1] - player.rect[1]) ** 2)
        if self.slash_animation.num_of_image == 0 and (time.time() - self.last_fire_slash) > 0.3 and distance < 2 * kSizeOfCharacter:
            self.last_fire_slash = time.time()

            image_of_slash = self.slash_animation.get_image()
            slash_rect = image_of_slash.get_rect(
                topleft=(self.rect[0] - self.size // 2, self.rect[1] - self.size // 2))
            # display.blit(image_of_slash, slash_rect)

            if slash_rect.colliderect(player.rect):
                # тут будет передаваться урон мобу
                player.Hurt(self.melee_attack_damage)

    def render(self, display, player_pos_on_screen, player_pos, mappa):
        super().render(display, player_pos_on_screen, player_pos, mappa)
        if self.slash_animation.num_of_image > 0:
            image_of_slash = self.slash_animation.get_image()
            position = (self.rect[0] - player_pos[0] + player_pos_on_screen[0],
                        self.rect[1] - player_pos[1] + player_pos_on_screen[1])
            display.blit(image_of_slash, (position[0] - self.size // 2, position[1] - self.size // 2))

    def update(self, mappa, player, player_pos_on_screen):
        self.Attack(player)


class RangeEnemy(Enemy, ABC):
    def __init__(self, position, enemy_personage: EnemyPersonage):
        super().__init__(position, enemy_personage)
        self.max_magic = 100
        self.magic_points = self.max_magic
        self.last_fire_time = 1
        self.cool_down = 3  # скорострельность оружия
        self.max_distance = 300  # расстояние, где противник может стрелять
        self.ranged_attack_damage = 50
        self.fires = []
        self.dist = 300  # Рандомное число

    def Attack(self, player_position, players_pos_on_screen):
        if time.time() - self.last_fire_time >= 1.5:  # проверяем прошло ли уже 1.5 секунды с прошлого выстрела
            distance = math.sqrt(
                (self.rect[0] - player_position[0]) ** 2 + (self.rect[1] - player_position[1]) ** 2)
            if distance <= self.max_distance:
                direction = [player_position[0] - self.rect.x, player_position[1] - self.rect.y]
                enemy_pos_on_screen = (self.rect[0] - player_position[0] + players_pos_on_screen[0],
                                       self.rect[1] - player_position[1] + players_pos_on_screen[1])
                fireball = Projectile(self.ranged_attack_damage, (self.rect.x, self.rect.y), enemy_pos_on_screen,
                                      players_pos_on_screen, distance, 0, 1, projectiles[0])
                self.fires.append(fireball)
                self.magic_points -= 10
                self.last_fire_time = time.time()

    def render(self, display, player_pos_on_screen, player_pos, mappa):
        super().render(display, player_pos_on_screen, player_pos, mappa)

        if self.fires:
            for (i, fire) in enumerate(self.fires):
                if fire.render(display, player_pos_on_screen, player_pos, mappa):
                    self.fires.pop(i)

    def update(self, mappa, player, player_pos_on_screen):
        # self.ChasePlayer(mappa, player_position)
        self.Attack((player.rect[0], player.rect[1]), player_pos_on_screen)
        if self.fires:
            for (i, fire) in enumerate(self.fires):
                if fire.update(mappa, [player]):
                    self.fires.pop(i)

        # if self.rect.colliderect(player.rect):
        #     player.health_points -= self.ranged_attack_damage
