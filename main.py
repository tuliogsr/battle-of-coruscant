from Interface.interface import MainMenu
import pygame
from pygame.sprite import Group

from Auxiliar.settings import Settings
from Auxiliar.game_stats import GameStats
from Auxiliar.scoreboard import Scoreboard
from Auxiliar.button import Button
from Auxiliar.ship import Ship
import Auxiliar.game_functions as gf

# Instancia e executa o menu principal
if __name__ == "__main__":
    menu = MainMenu()
    menu.run()