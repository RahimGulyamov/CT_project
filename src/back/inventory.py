import pygame

from src.back.magic_crystal import crystals

pygame.init()


class Resource:
    def __init__(self, name, crystal):
        self.name = name
        self.crystal = crystal
        self.amount = 0
        self.image = None
        self.image = pygame.image.load(self.crystal.path_to_image).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (48, 48))

    def draw(self, display, x, y):
        font = pygame.font.SysFont('calibri', 20)
        label = font.render(str(self.amount), True, (0, 0, 0))
        display.blit(self.image, (x + 16, y + 16))
        display.blit(label, (x + 40, y + 75))


class Inventory:
    def __init__(self, crystals_from_player):
        self.resources = {
            "Fire Crystal": Resource("Fire Crystal", crystals[0]),
            "Light Crystal": Resource("Light Crystal", crystals[1]),
            "Blue Fire Crystal": Resource("Blue Fire Crystal", crystals[2]),
            "Purple Fire Crystal": Resource("Purple Fire Crystal", crystals[3]),
            "Blood Crystal": Resource("Blood Crystal", crystals[4]),
            "Ice Crystal": Resource("Ice Crystal", crystals[5])
        }

        self.resources_for_chest = {
            "Fire Crystal": Resource("Fire Crystal", crystals[0]),
            "Light Crystal": Resource("Light Crystal", crystals[1]),
            "Blue Fire Crystal": Resource("Blue Fire Crystal", crystals[2]),
            "Purple Fire Crystal": Resource("Purple Fire Crystal", crystals[3]),
            "Blood Crystal": Resource("Blood Crystal", crystals[4]),
            "Ice Crystal": Resource("Ice Crystal", crystals[5])
        }

        self.crystals_panel = [None] * 4
        self.whole_inventory = [None] * 6

        self.chest_inventory = [None] * 6

        self.update_panel(crystals_from_player)

        self.crystals_panel[3] = pygame.image.load(
            "src/tile_sets/tiles_for_chars/magic_crystals/inventary.png").convert_alpha()
        self.crystals_panel[3] = pygame.transform.scale(
            self.crystals_panel[3], (80, 80))

        self.crystals_panel_rects = [pygame.Rect(1800, 410, 80, 80), pygame.Rect(1800, 510, 80, 80),
                                     pygame.Rect(1800, 610, 80, 80), pygame.Rect(1800, 710, 80, 80)]

        self.whole_inventory_rects = [pygame.Rect(1500, 430, 80, 100), pygame.Rect(1600, 430, 80, 100),
                                      pygame.Rect(1500, 550, 80, 100), pygame.Rect(1600, 550, 80, 100),
                                      pygame.Rect(1500, 670, 80, 100), pygame.Rect(1600, 670, 80, 100)]

        self.chest_inventory_rects = [pygame.Rect(50, 430, 80, 100), pygame.Rect(150, 430, 80, 100),
                                      pygame.Rect(50, 550, 80, 100), pygame.Rect(150, 550, 80, 100),
                                      pygame.Rect(50, 670, 80, 100), pygame.Rect(150, 670, 80, 100)]

        self.is_open_whole = False

        self.is_open_chest_inventory = False

        self.chest = None

    def open_chest_inventory(self, chest):
        self.chest = chest
        if self.is_open_chest_inventory:
            self.close_chest_inventory()
        self.set_items_in_chest(chest.GetItems())
        self.is_open_chest_inventory = True

    def close_chest_inventory(self):
        self.is_open_chest_inventory = False
        self.clear_chest_items()

    def get_amount(self, name):
        try:
            return self.resources[name].amount
        except KeyError:
            return -1

    def increase(self, name):
        try:
            self.resources[name].amount += 1
            self.update_whole()
        except KeyError:
            print("Error increasing")

    def set_items_in_chest(self, list_with_names):
        for name in list_with_names:
            try:
                self.resources_for_chest[name].amount += 1
                self.update_chest_inventory()
            except KeyError:
                print("Error increasing")

    def clear_chest_items(self):
        for key in self.resources_for_chest:
            self.resources_for_chest[key].amount = 0
        self.update_chest_inventory()

    def decrease(self, name):
        try:
            self.resources[name].amount -= 1
            self.update_whole()
        except KeyError:
            print("Error increasing")

    def decrease_chest(self, name):
        try:
            self.resources_for_chest[name].amount -= 1
            self.update_chest_inventory()
            self.chest.PopItem(name)
        except KeyError:
            print("Error increasing")

    def update_whole(self):
        for name, resource in self.resources.items():
            if resource.amount != 0 and resource not in self.whole_inventory:
                self.whole_inventory.insert(self.whole_inventory.index(None), resource)
                self.whole_inventory.remove(None)
        for i, resource in enumerate(self.whole_inventory):
            if resource is not None and resource.amount == 0:
                self.whole_inventory[i] = None

    def update_chest_inventory(self):
        for name, resource in self.resources_for_chest.items():
            if resource.amount != 0 and resource not in self.chest_inventory:
                self.chest_inventory.insert(self.chest_inventory.index(None), resource)
                self.chest_inventory.remove(None)
        for i, resource in enumerate(self.chest_inventory):
            if resource is not None and resource.amount == 0:
                self.chest_inventory[i] = None

    def update_panel(self, crystals_from_player):
        for i, crystal in enumerate(crystals_from_player):
            if crystal is not None:
                self.crystals_panel[i] = Resource(crystal.name, crystal)
            else:
                self.crystals_panel[i] = None

    def draw_whole(self, display):
        pygame.draw.rect(display, (182, 195, 206), (1480, 410, 220, 380))
        for i, cell in enumerate(self.whole_inventory):
            pygame.draw.rect(display, (200, 215, 227), self.whole_inventory_rects[i])
            if cell is not None:
                cell.draw(display, self.whole_inventory_rects[i].x, self.whole_inventory_rects[i].y)

    def draw_chest(self, display):
        pygame.draw.rect(display, (182, 195, 206), (30, 410, 220, 380))
        for i, cell in enumerate(self.chest_inventory):
            pygame.draw.rect(display, (200, 215, 227), self.chest_inventory_rects[i])
            if cell is not None:
                cell.draw(display, self.chest_inventory_rects[i].x, self.chest_inventory_rects[i].y)

    def draw_crystals(self, display):
        pygame.draw.rect(display, (182, 195, 206), (1780, 390, 120, 420))
        for i, cell in enumerate(self.crystals_panel):
            if i < 3:
                pygame.draw.rect(display, (200, 215, 227), self.crystals_panel_rects[i])
                if cell is not None:
                    display.blit(cell.image, (self.crystals_panel_rects[i].x + 16, self.crystals_panel_rects[i].y + 16))
            else:
                pygame.draw.rect(display, (135, 95, 95), self.crystals_panel_rects[i])
                display.blit(cell, self.crystals_panel_rects[i])

    def draw(self, display):
        if self.is_open_whole:
            self.draw_whole(display)
        if self.is_open_chest_inventory:
            self.draw_chest(display)
        self.draw_crystals(display)

    def open_whole(self):
        self.is_open_whole = True

    def close_whole(self):
        self.is_open_whole = False
