#base klash olonwn twn level
#This is a simple base class for all levels, providing a structure 
# for updating game logic and drawing elements. If you need specific 
# behavior for a level, you can override the update and
# draw methods in the derived class.
import pygame
class Level:
    def __init__(self, levelData, screen):
        # Base class for all levels
        self.levelData = levelData
        self.screen = screen
        self.clientGameManager = None
        
    def update(self):
        # Update game logic for this level
        pass
        # Update game logic for this level
        
    def setClientGameManager(self, _clientGameManager):
        # Set the client game manager for this level
        self.clientGameManager = _clientGameManager 
        
    def draw(self):
        # Draw the level's elements to the screen
        pass
        # Draw the level's elements to the screen
