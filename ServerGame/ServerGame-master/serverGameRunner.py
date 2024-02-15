from mode import Mode
import pygame
import sys

class ServerGameRunner:
    def __init__(self):

        self.mode = None
        self.screen = None
        self.lobby_mode_initiated = False
        self.game_mode_initiated = False
        
    def preRunServerWindow(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.mode = Mode(self.screen)
        self.lobby_mode_initiated = False
        self.game_mode_initiated = False
        
        self.runServerWindow()
        
    def runServerWindow(self):
        fps = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(fps)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            self.mode.update() #polymorphism
            self.mode.draw() #polymorphism
        