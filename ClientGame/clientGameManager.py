#This file defines the ClientGameManager class, which manages
# the game flow and network communication. The manager is 
# initialized with a level and a player, and it sets itself as the 
# client game manager for the level. The switchLevel method allows changing the 
# current level, and the getNetworkManager method returns 
# the network manager for network communication.

# Import necessary modules

import pygame
from clientNetworkManager import ClientNetworkManager
from player import Player
#import pygame.mixer.music
# Class for managing the client-side game
class ClientGameManager:
    
    def __init__(self, level):
        # Initialize the client network manager, current level, and player with network manager and player
        self.clientNetworkManagerObj = ClientNetworkManager()
        self.currentLevel = level
        self.player = Player()
        self.currentLevel.setClientGameManager(self) # The level sets the client game manager
        
    def switchLevel(self, levelToTransition):
        # Change the level and the mode# gia na allaksoume to level kai sunepws to mode
        #  # Switch to a new game level and set the client game manager
        self.currentLevel = levelToTransition
        self.currentLevel.setClientGameManager(self)
    
    def getNetworkManager(self):
        # Get the client's network manager
        # Get the network manager instance
        return self.clientNetworkManagerObj
            
    def runGame(self):
        # Run the game loop
       
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)   #60 frames per second
             # Update and draw the current game level
            # Fill the screen with a white background.
             # Update the current level with events, draw, and handle collisions       
            # Fill the screen with a white background
            self.currentLevel.update(pygame.event.get())
            self.currentLevel.draw()
            # Update the display
        # Quit pygame when the game loop exits 
            
        pygame.quit()
               
        
        
