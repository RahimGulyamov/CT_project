import pygame
from src.back.player import Player
from src.back.inventory import Inventory
import time


class Controller:
    def __init__(self, player: Player, inventory: Inventory):
        self.player = player
        self.inventory = inventory
        self.mouse_position = None
        self.left_mouse_down = False
        self.left_mouse_up = False
        # self.list_of_rects = []
        self.last_hit = time.time()

    def update(self, player_on_screen_pos):
        self.left_mouse_up = not pygame.mouse.get_pressed()[0]
        is_collide_with_rects = False
        if self.left_mouse_down and self.left_mouse_up:
            is_open_whole = False
            # self.left_mouse_up = False
            if self.inventory.is_open_whole:
                for i, rect in enumerate(self.inventory.whole_inventory_rects):
                    if rect.collidepoint(self.mouse_position):
                        is_collide_with_rects = True
                        is_open_whole = True
                        if self.inventory.whole_inventory[i] is not None and self.player.staff.num_of_crystals < 3:
                            self.player.staff.add_crystal(self.inventory.whole_inventory[i].crystal)
                            self.inventory.decrease(self.inventory.whole_inventory[i].name)
                            self.inventory.update_panel(self.player.staff.crystals)

            for i, rect in enumerate(self.inventory.crystals_panel_rects):
                if rect.collidepoint(self.mouse_position):
                    is_collide_with_rects = True
                    if i == 3:
                        is_open_whole = not self.inventory.is_open_whole
                    if i < 3 and self.player.staff.crystals[i] is not None:
                        is_open_whole = self.inventory.is_open_whole
                        name = self.player.staff.crystals[i].name
                        self.player.staff.delete_crystal(i)
                        self.inventory.increase(name)
                        self.inventory.update_panel(self.player.staff.crystals)

            if self.inventory.is_open_chest_inventory:
                for i, rect in enumerate(self.inventory.chest_inventory_rects):
                    if rect.collidepoint(self.mouse_position):
                        is_collide_with_rects = True
                        if self.inventory.chest_inventory[i] is not None:
                            self.inventory.increase(self.inventory.chest_inventory[i].name)
                            self.inventory.decrease_chest(self.inventory.chest_inventory[i].name)


            if not is_collide_with_rects:
                self.player.ranged_attack(player_on_screen_pos, self.mouse_position)
            self.inventory.is_open_whole = is_open_whole

        self.left_mouse_down = pygame.mouse.get_pressed()[0]
        self.mouse_position = pygame.mouse.get_pos()

        # self.test_hearts_for_health()

    def test_hearts_for_health(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_h] and time.time() - self.last_hit > 0.1:
            self.player.health_points -= 50
            self.last_hit = time.time()

    def test_delete_enemies(self, enemies):
        key = pygame.key.get_pressed()
        if key[pygame.K_h] and time.time() - self.last_hit > 0.1:
            try:
                enemies.pop()
            except:
                pass
            self.last_hit = time.time()
