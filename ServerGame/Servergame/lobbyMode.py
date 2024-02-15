#handles the data chosen in the lobby
from mode import Mode
from lobby import Lobby
import pygame
from gameManager import GameManager
from difficultyEnum import Difficulty
class LobbyMode(Mode):
    
    def __init__(self, screen, gameManager, gameRunner):
        super().__init__(screen)
        # Additional initialization for LobbyMode if needed
        self.lobby = Lobby()
        self.lobby_data = None
        self.game_manager = gameManager
        self.game_runner = gameRunner
        
    def update(self):
        self.screen.fill((100, 100, 10))
        if self.dataP1 is not None:

            instructionP1 = self.dataP1["fetch_lobby_data|p1"]["instruction"]
            match instructionP1:
                case "{'idle'}":
                    pass
                case "{'lockPlayer'}":
                    self.lobby.lockPlayer("p1")
                case "{'vehicleALock'}":
                    if self.lobby.lockVehicleA() == True:
                        self.lockVehicle("Thunderbolt", "p1")
                case "{'vehicleBLock'}":
                    if self.lobby.lockVehicleB() == True:
                        self.lockVehicle("Vanguard", "p1")
                case "{'lockEasy'}":
                    self.lobby.lockEasy()
                    self.game_manager.difficulty = Difficulty.EASY
                case "{'lockMedium'}":
                    self.lobby.lockMedium()
                    self.game_manager.difficulty = Difficulty.MEDIUM
                case "{'lockHard'}":
                    self.lobby.lockHard()
                    self.game_manager.difficulty = Difficulty.HARD
                                                                  
        if self.dataP2 is not None:
            instructionP2 = self.dataP2["fetch_lobby_data|p2"]["instruction"]

            match instructionP2:
                case "{'idle'}":
                    pass
                case "{'lockPlayer'}":
                    self.lobby.lockPlayer("p2")
                case "{'vehicleALock'}":
                    if self.lobby.lockVehicleA() == True:
                        self.lockVehicle("Thunderbolt", "p2")
                case "{'vehicleBLock'}":
                    if self.lobby.lockVehicleB() == True:
                        self.lockVehicle("Vanguard", "p2")
                case "{'lockEasy'}":
                    self.lobby.lockEasy()
                case "{'lockMedium'}":
                    self.lobby.lockMedium()
                case "{'lockHard'}":
                    self.lobby.lockHard()                       
                 

    def draw(self):
        super().draw()
        

    def lockVehicle(self, vehicle, p):
        if p == "p1":
            self.game_manager.player1.vehicle = vehicle
        if p == "p2":
            self.game_manager.player2.vehicle = vehicle        
        