import os
import pygame
import webbrowser


def get_parent_dir(path):
    return os.path.sep.join(path.split(os.path.sep)[:-1])


webbrowser.open(f'{get_parent_dir(pygame.__file__)}{os.path.sep}docs{os.path.sep}generated{os.path.sep}index.html')