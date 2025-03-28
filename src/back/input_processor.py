import pygame

from src.back.Map.Objects.map_objects import *


class MouseEventProcessor:
    def __init__(self, map_processor, player, render, game, inventory):
        self.map_processor = map_processor
        self.player = player
        self.render = render
        self.game = game
        self.inventory = inventory
        self.actions = {Exit: self.ExitAction, BasicChest: self.ChestAction}

    def ExitAction(self, obj):
        self.game.EnterNewLevel()

    def ChestAction(self, obj):
        self.inventory.open_chest_inventory(obj)

    @staticmethod
    def CheckIfChestClose(mouse_position):

        return mouse_position[0] >= 30 and mouse_position[0] <= 250 and mouse_position[1] >= 410 and mouse_position[
            1] <= 790

    def CloseChestAction(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.CheckIfChestClose(pygame.mouse.get_pos()):
                self.inventory.close_chest_inventory()

    def ActionWithMapObjects(self):
        mouse_position = self.GetMousePositionOnTheMap()
        if self.inventory.is_open_chest_inventory:
            self.CloseChestAction()
        if pygame.mouse.get_pressed()[0]:
            for obj in self.map_processor.GetObjects():
                if self.map_processor.IsInCurrentRoom(mouse_position) and dist(self.player.GetCenterPosition(),
                                                                               obj.GetCenter()) <= DISTANCE_OF_ACTION:
                    if obj.IsThere(mouse_position):
                        self.actions[type(obj)](obj)


    def Update(self):
        self.ActionWithMapObjects()

    def GetMousePositionOnTheMap(self):
        return self.player.GetPosition()[0] - self.render.GetPlayerPositionOnTheScreen()[0] + pygame.mouse.get_pos()[0], \
               self.player.GetPosition()[1] - self.render.GetPlayerPositionOnTheScreen()[1] + pygame.mouse.get_pos()[1]
