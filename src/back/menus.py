"""File contains menu"""
from abc import ABC

import pygame_menu

import src.back.Config as Config


class Menu(ABC):
    """abstract class for menus"""

    def __init__(self, display):
        self.display = display
        self.menu = None

    def ProcessMenu(self):
        """this method process menu"""

        self.menu.mainloop(self.display)

    def Close(self):
        """this method close the menu"""

        self.menu.close()

    @staticmethod
    def ReturnOnlyValue(key, value):
        """this method returns only value for callback"""

        return value


class StartMenu(Menu):
    """class for start menu"""

    def __init__(self, display, start_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button(Config.CHARACTER_SELECTION_STRING, start_process.MoveToCharacterSelection)
        self.menu.add.button(Config.QUIT_CONDITION_STRING, pygame_menu.events.EXIT)


class CharacterSelectionMenu(Menu):
    """class for server selection menu"""

    def __init__(self, display, character_selection_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)

        def SetCharacter(key, value):
            character_selection_process.SetCharacter(value)

        SetCharacter(1, Config.CHARACTERS[0][1])

        self.menu.add.selector(title=Config.CHARACTER_SELECTION_STRING, items=Config.CHARACTERS,
                               onchange=SetCharacter)
        self.menu.add.button(Config.PLAY_CONDITION_STRING, character_selection_process.StartGameSession)
        self.menu.add.button(Config.BACK_CONDITION_STRING, character_selection_process.MoveToOnStartProcess)
        self.menu.add.button(Config.QUIT_CONDITION_STRING, pygame_menu.events.EXIT)
