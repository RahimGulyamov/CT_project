import random
from abc import ABC
from math import dist

from src.back.Config import *
from src.back.Map.constants_for_map import *
from src.back.magic_crystal import *


class MapObject(ABC):
    def __init__(self, position_on_the_map, size):
        self.position = position_on_the_map
        self.size = size

    def GetPosition(self):
        return self.position

    def GetCenter(self):
        return self.position[0] + self.size // 2, self.position[1] + self.size // 2

    def IsThere(self, position):
        return dist(self.GetCenter(), position) <= self.size // 2


class Chest(MapObject):
    def __init__(self, position_on_the_map, size_of_chest):
        super().__init__(position_on_the_map, size_of_chest)
        self.list_with_items = []
        self.is_open = False

    def GetItems(self):
        return self.list_with_items

    def AddNewItem(self, item):
        self.list_with_items.append(item)

    def PopItem(self, item):
        self.list_with_items.pop(self.list_with_items.index(item))

    def Open(self):
        self.is_open = True

    def Close(self):
        self.is_open = False


class BasicChest(Chest):
    def __init__(self, position_on_the_map):
        super().__init__(position_on_the_map, SIZE_OF_BASIC_CHEST)
        crystal = random.choice(crystals)
        self.AddNewItem(crystal.name)


class Exit(MapObject):
    def __init__(self, position_on_the_map):
        super().__init__(position_on_the_map, SIZE_OF_TILE)
