import pygame.time

import src.back.Config
from src.back.Map.map_processor import MapProcessor
from src.back.Map.minimap import MiniMap
from src.back.Render import Render
from src.back.Window import Window
from src.back.controller import Controller
from src.back.enemy_processor import *
from src.back.in_game_eventor import Eventor
from src.back.input_processor import *
from src.back.inventory import Inventory
from src.back.player import Player
from src.back.processes import OnStartProcess


class Game:
    def __init__(self):
        self.window = Window()
        self.mini_map = None
        self.map_processor = None
        self.player = None
        self.enemy_processor = None
        self.inventory = None
        self.controller = None
        self.render = None
        self.clock = None
        self.in_game_eventor = None
        self.mouse_processor = None

    def StartGame(self):
        OnStartProcess(self.window.GetDisplay(), self)

    def ProcessMainLoop(self):
        self.map_processor.SpawnChestInCurrentRoom(self.render)
        while src.back.Config.RUNNING:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    src.back.Config.RUNNING = False
                self.mini_map.ProcessEvents(event=event)
            self.mouse_processor.Update()
            self.enemy_processor.Update(self.map_processor, self.player, self.render.GetPlayerPositionOnTheScreen())
            self.in_game_eventor.Update(self.render)
            self.controller.update(self.render.CenterOfPlayerPosition())
            self.controller.test_delete_enemies(self.enemy_processor.GetEnemies())
            self.player.update(self.map_processor, self.render, self.enemy_processor.GetEnemies())
            if not self.player.is_alive() and src.back.Config.RUNNING:
                self.StartGame()
            self.map_processor.UpdateCurrentRoom(self.player.GetStandPosition(), self.mini_map)
            self.render.Draw()

    def StartGameSession(self, character):
        self.mini_map = MiniMap()
        self.map_processor = MapProcessor(self.mini_map)
        self.player = Player(self.window.GetDisplay(), character, self.map_processor.GetSpawnPosition(self.mini_map))
        self.inventory = Inventory(self.player.staff.crystals)
        self.controller = Controller(self.player, self.inventory)
        self.EnterNewLevel()

    def EnterNewLevel(self):
        self.mini_map = MiniMap()
        self.map_processor = MapProcessor(self.mini_map)
        self.player.SetPosition(self.map_processor.GetSpawnPosition(self.mini_map))
        self.enemy_processor = EnemyProcessor(self.map_processor, self.player)
        self.render = Render(self.window.GetDisplay(), self.player, self.map_processor, self.mini_map,
                             self.enemy_processor, self.inventory)
        self.clock = pygame.time.Clock()
        self.in_game_eventor = Eventor(self.player, self.map_processor, self.mini_map, self.enemy_processor)
        self.mouse_processor = MouseEventProcessor(self.map_processor, self.player, self.render, self, self.inventory)
        self.ProcessMainLoop()
