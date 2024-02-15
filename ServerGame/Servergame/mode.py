import json
import pygame

class Mode:
    
    def __init__(self, screen):
        self.screen = screen
        self._dataP1 = None
        self._dataP2 = None
    def update(self):
        self.screen.fill((100, 10, 10))
    
    @property
    def dataP1(self):
        return self._dataP1

    @dataP1.setter
    def dataP1(self, json_input):
        try:
            self._dataP1 = json_input
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    @property
    def dataP2(self):
        return self._dataP2

    @dataP2.setter
    def dataP2(self, json_input):
        try:
            self._dataP2 = json_input
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
    def draw(self):
        pygame.display.flip()
        # Draw the level's elements to the screen
