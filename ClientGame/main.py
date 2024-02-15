import json
import pygame
import sys
from player import Player
from clientGameManager import ClientGameManager
from entryLevel import EntryLevel

if __name__ == "__main__":
    # load entry level and to take parameters in to connect we need to load the data of the level 
    # there is not player yet the first level will be used to make the player to connect to the server and choose the player
    # so only the level and client game manager is loaded
    level_ldata = ""
    with open("LevelsData/EntryScene.json", "r") as file:
        level_data = json.load(file)
    
    pygame.init()
    pygame.mixer.init()
    
    screen = None
    currentLevel = EntryLevel(level_data, screen)
    clientgameManager = ClientGameManager(currentLevel)
    clientgameManager.runGame()
    
