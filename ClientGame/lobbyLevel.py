import pygame
import sys
from level import Level
from player import Player
import json
from gameLevel import GameLevel
class LobbyLevel(Level):
    
    def __init__(self, levelData, screen):
        super().__init__(levelData, screen)
        
        self.clientGameManager = None
        
        # Additional initialization for the derived class
        self.screen = pygame.display.set_mode((self.levelData["screen_width"], self.levelData["screen_height"]),pygame.RESIZABLE)        # Create the window
        pygame.display.set_caption("Aeroplane assault")
        self.background_image = pygame.image.load("Sprites/island.png").convert()
        
        
        # Load image
        self.tank_imageP1 = pygame.image.load("Sprites/tankP1.png")
        self.tank_rectP1 = self.tank_imageP1.get_rect(center=(275, 390))
        
        self.tank_imageP2 = pygame.image.load("Sprites/tankP2.png")
        self.tank_rectP2 = self.tank_imageP2.get_rect(center=(475, 390))
        
        self.font_error = pygame.font.SysFont("timesnewroman", 32)  
        self.error_text = self.font_error.render("", True, (255, 50, 50))
        self.locked_easy = False
        self.locked_medium = False
        self.locked_hard = False
        self.locked_vehicleA = False
        self.locked_vehicleB = False
        self.locked_ready = False
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        self.instruction = ""
        #Button
        # Set up fonts
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 36)
        self.input_text_username = ""
        self.input_text_password = ""
        # Set up font for title
        self.font_title = pygame.font.SysFont("timesnewroman", 50)  # Use Times New Roman font, size 72
        self.text_surface_title = self.font_title.render("Tanks!", True, (228, 228, 228))  
          
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.button_color = (50, 150, 255)  # Light blue
        self.button_color_locked = (142, 255, 114)  # selected button Color
        self.button_color_disabled = (130, 134, 142)  # disabled button color

        self.hasVehicleASelected = False
        self.hasVehicleBSelected = False

        self.button_color_hovered = (34, 128, 235)  # darker blue
        # Fonts
        #self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        self.button_font_select_button_fonts = pygame.font.Font(None, 32)

        
        self.ready_button_width = 200 
        self.ready_button_height = 50
        self.ready_button_x = 300
        self.ready_button_y = 450
                
        self.select_vehiclea_button_width = 150 
        self.select_vehiclea_button_height = 40
        self.select_vehiclea_x = 200
        self.select_vehiclea_y = 300
        
        self.select_vehicleb_button_width = self.select_vehiclea_button_width 
        self.select_vehicleb_button_height = self.select_vehiclea_button_height 
        self.select_vehicleb_x = 400
        self.select_vehicleb_y = 300
        
        self.select_difficulty_easy_button_width = 200 
        self.select_difficulty_easy_button_height = 50
        self.select_difficulty_easy_x = 100
        self.select_difficulty_easy_y = 150        
        
        self.select_difficulty_medium_button_width = 200 
        self.select_difficulty_medium_button_height = 50
        self.select_difficulty_medium_x = 300
        self.select_difficulty_medium_y = 150
        
        self.select_difficulty_hard_button_width = 200 
        self.select_difficulty_hard_button_height = 50
        self.select_difficulty_hard_x = 500
        self.select_difficulty_hard_y = 150
        
        self.statistics_button_width = 150 
        self.statistics_button_height = 30
        self.statistics_x = 600
        self.statistics_y = 50
        
        self.ready_button = pygame.Rect(self.ready_button_x,  self.ready_button_y, self.ready_button_width, self.ready_button_height)
        self.vehicleA_button = pygame.Rect(self.select_vehiclea_x,  self.select_vehiclea_y, self.select_vehiclea_button_width, self.select_vehiclea_button_height)
        self.vehicleB_button = pygame.Rect(self.select_vehicleb_x,  self.select_vehicleb_y, self.select_vehicleb_button_width, self.select_vehicleb_button_height)    
        self.difficulty_easy_button = pygame.Rect(self.select_difficulty_easy_x, self.select_difficulty_easy_y, self.select_difficulty_easy_button_width, self.select_difficulty_easy_button_height)
        self.difficulty_medium_button = pygame.Rect(self.select_difficulty_medium_x, self.select_difficulty_medium_y, self.select_difficulty_medium_button_width, self.select_difficulty_medium_button_height)
        self.difficulty_hard_button = pygame.Rect(self.select_difficulty_hard_x, self.select_difficulty_hard_y, self.select_difficulty_hard_button_width, self.select_difficulty_hard_button_height)
        self.statistics_button = pygame.Rect(self.statistics_x, self.statistics_y, self.statistics_button_width, self.statistics_button_height)

        #Sounds
        self.click_sound = pygame.mixer.Sound(self.levelData["click_sound_path"]) 
        self.type_sound = pygame.mixer.Sound(self.levelData["type_sound_path"])  

    def setClientGameManager(self, _clientGameManager):
        self.clientGameManager = _clientGameManager 
        
    def update(self, events):
               
        for event in events:
            self.instruction = "idle"
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
                     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.ready_button.collidepoint(event.pos) and self.locked_ready == False and self.hasLockedDifficulty() == True and self.hasLockedVehicle() == True:  
                    self.instruction = "lockPlayer"
                    self.locked_ready = True
                    self.click_sound.play()
                    
                if event.button == 1 and self.vehicleA_button.collidepoint(event.pos) and self.locked_vehicleA == False and self.hasLockedVehicle() == False:
                    self.instruction = "vehicleALock"
                    self.hasVehicleASelected = True
                    self.clientGameManager.player.vehicle = "Thunderbolt"
                    self.click_sound.play()
                if event.button == 1 and self.vehicleB_button.collidepoint(event.pos) and self.locked_vehicleB == False and self.hasLockedVehicle() == False: 
                    self.instruction = "vehicleBLock"
                    self.hasVehicleBSelected = True
                    self.clientGameManager.player.vehicle = "Vanguard"

                    self.click_sound.play()
                if event.button == 1 and self.difficulty_easy_button.collidepoint(event.pos) and self.locked_easy == False and self.hasLockedDifficulty() == False: 
                    self.instruction = "lockEasy"
                    self.click_sound.play()
                if event.button == 1 and self.difficulty_medium_button.collidepoint(event.pos) and self.locked_medium == False and self.hasLockedDifficulty() == False: 
                    self.instruction = "lockMedium"
                    self.click_sound.play()
                if event.button == 1 and self.difficulty_hard_button.collidepoint(event.pos) and self.locked_hard == False and self.hasLockedDifficulty() == False: 
                    self.instruction = "lockHard"
                    self.click_sound.play()
                if event.button == 1 and self.statistics_button.collidepoint(event.pos): 
                    # logic for statistics
                    self.click_sound.play()
                    
                
            if event.type == pygame.MOUSEMOTION:         
                self.mouse_position_x, self.mouse_position_y = event.pos      
                   
        self.screen.blit(self.background_image, (0, 0))
                    
        lobby_data = {
            "fetch_lobby_data" +"|" + str(self.clientGameManager.player.getPlayerStr()): {
                "instruction": {
                    self.instruction
                },

                "difficulty": {
                    "easyLocked": self.locked_easy,
                    "mediumLocked": self.locked_medium,
                    "hardLocked": self.locked_hard
                },
                "vehicles": {
                    "vehicleALocked": self.locked_vehicleA,
                    "vehicleBLocked": self.locked_vehicleB
                }
                    
            }
        }
        
        json_data = json.dumps(lobby_data, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o))
        self.clientGameManager.getNetworkManager().sendJSON(json_data)

        response = self.clientGameManager.getNetworkManager().receive()
        json_data_received = json.loads(response)

        self.locked_easy = json_data_received.get('difficulty', {}).get('easyLocked', None)
        self.locked_medium = json_data_received.get('difficulty', {}).get('mediumLocked', None)
        self.locked_hard = json_data_received.get('difficulty', {}).get('hardLocked', None)
        self.locked_vehicleA = json_data_received.get('vehicles', {}).get('vehicleALocked', None)
        self.locked_vehicleB = json_data_received.get('vehicles', {}).get('vehicleBLocked', None)
        
        bothPlayersReady = json_data_received.get('readyStatus', {}).get('ready_Player1Locked', None) == True and json_data_received.get('readyStatus', {}).get('ready_Player2Locked', None) == True
        if bothPlayersReady ==True:            
            level_data = ""
            with open("LevelsData/MainScene.json", "r") as file:
                level_data = json.load(file)
            newLevel = GameLevel(level_data, self.screen)
            self.clientGameManager.switchLevel(newLevel)
            
        if self.locked_ready == False:
            if self.hasLockedDifficulty() == True and self.hasLockedVehicle() == True:
                pygame.draw.rect(self.screen, self.button_color, self.ready_button)
                pygame.draw.rect(self.screen, self.black, self.ready_button, 2) 
                if self.ready_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                    pygame.draw.rect(self.screen, self.button_color_hovered, self.ready_button)
                    pygame.draw.rect(self.screen, self.black, self.ready_button, 2)
            else:
                pygame.draw.rect(self.screen, self.button_color_disabled, self.ready_button)
                pygame.draw.rect(self.screen, self.black, self.ready_button, 2) 
                
        else:
            pygame.draw.rect(self.screen, self.button_color_locked, self.ready_button)
            pygame.draw.rect(self.screen, self.black, self.ready_button, 2) 
            

        if self.hasLockedDifficulty() == False:
            
            pygame.draw.rect(self.screen, self.button_color, self.difficulty_easy_button)
            pygame.draw.rect(self.screen, self.black, self.difficulty_easy_button, 2)       
            if self.difficulty_easy_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                pygame.draw.rect(self.screen, self.button_color_hovered, self.difficulty_easy_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_easy_button, 2)
                
                
            pygame.draw.rect(self.screen, self.button_color, self.difficulty_medium_button)
            pygame.draw.rect(self.screen, self.black, self.difficulty_medium_button, 2)       
            if self.difficulty_medium_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                pygame.draw.rect(self.screen, self.button_color_hovered, self.difficulty_medium_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_medium_button, 2) 
                
            pygame.draw.rect(self.screen, self.button_color, self.difficulty_hard_button)
            pygame.draw.rect(self.screen, self.black, self.difficulty_hard_button, 2)       
            if self.difficulty_hard_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                pygame.draw.rect(self.screen, self.button_color_hovered, self.difficulty_hard_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_hard_button, 2)    
        
        else:
            if self.locked_easy == True:
                pygame.draw.rect(self.screen, self.button_color_locked, self.difficulty_easy_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_easy_button, 2)
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_medium_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_medium_button, 2)  
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_hard_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_hard_button, 2)                  
            elif self.locked_medium == True:
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_easy_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_easy_button, 2)
                pygame.draw.rect(self.screen, self.button_color_locked, self.difficulty_medium_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_medium_button, 2)  
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_hard_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_hard_button, 2)
            elif self.locked_hard == True:
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_easy_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_easy_button, 2)
                pygame.draw.rect(self.screen, self.button_color_disabled, self.difficulty_medium_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_medium_button, 2)  
                pygame.draw.rect(self.screen, self.button_color_locked, self.difficulty_hard_button)
                pygame.draw.rect(self.screen, self.black, self.difficulty_hard_button, 2)
                
        if self.hasLockedVehicle() == True:
                    
            if self.locked_vehicleA == True:
                
                if self.hasVehicleASelected == True:
                    pygame.draw.rect(self.screen, self.button_color_locked, self.vehicleA_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)
                    pygame.draw.rect(self.screen, self.button_color_disabled, self.vehicleB_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)    

            if self.locked_vehicleB == True:
                
                if self.hasVehicleBSelected == True:
                    pygame.draw.rect(self.screen, self.button_color_locked, self.vehicleB_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)     
                    pygame.draw.rect(self.screen, self.button_color_disabled, self.vehicleA_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)    
        
        else:
            if self.locked_vehicleA == False and self.locked_vehicleB == False:
                pygame.draw.rect(self.screen, self.button_color, self.vehicleB_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)       
                if self.vehicleB_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                    pygame.draw.rect(self.screen, self.button_color_hovered, self.vehicleB_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)                
                pygame.draw.rect(self.screen, self.button_color, self.vehicleA_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)       
                if self.vehicleA_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                    pygame.draw.rect(self.screen, self.button_color_hovered, self.vehicleA_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)                             
                
            if self.locked_vehicleA == True:
                pygame.draw.rect(self.screen, self.button_color_disabled, self.vehicleA_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)
                pygame.draw.rect(self.screen, self.button_color, self.vehicleB_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)       
                if self.vehicleB_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                    pygame.draw.rect(self.screen, self.button_color_hovered, self.vehicleB_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)

            if self.locked_vehicleB == True:
                pygame.draw.rect(self.screen, self.button_color_disabled, self.vehicleB_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleB_button, 2)
                pygame.draw.rect(self.screen, self.button_color, self.vehicleA_button)
                pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)       
                if self.vehicleA_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
                    pygame.draw.rect(self.screen, self.button_color_hovered, self.vehicleA_button)
                    pygame.draw.rect(self.screen, self.black, self.vehicleA_button, 2)                

            

                
        pygame.draw.rect(self.screen, self.button_color, self.statistics_button)
        pygame.draw.rect(self.screen, self.black, self.statistics_button, 2) 
        if self.statistics_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.statistics_button)
            pygame.draw.rect(self.screen, self.black, self.statistics_button, 2)
            
                        
        text_rect_title = self.text_surface_title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(self.text_surface_title, text_rect_title)
        
        button_text_ready = self.button_font.render("READY", True, self.black)
        text_rect_ready = button_text_ready.get_rect(center=self.ready_button.center)
        self.screen.blit(button_text_ready, text_rect_ready)
        
        button_text_vehicleA = self.button_font_select_button_fonts.render("Thunderbolt", True, self.black)
        text_rect_vehicleA = button_text_vehicleA.get_rect(center=self.vehicleA_button.center)
        self.screen.blit(button_text_vehicleA, text_rect_vehicleA)
        
        button_text_vehicleB = self.button_font_select_button_fonts.render("Vanguard", True, self.black)
        text_rect_vehicleB = button_text_vehicleA.get_rect(center=self.vehicleB_button.center)
        self.screen.blit(button_text_vehicleB, text_rect_vehicleB)
        
        button_text_easy = self.button_font.render("Easy", True, self.black)
        text_rect_easy = button_text_easy.get_rect(center=self.difficulty_easy_button.center)
        self.screen.blit(button_text_easy, text_rect_easy)
        
        button_text_medium = self.button_font.render("Medium", True, self.black)
        text_rect_medium = button_text_medium.get_rect(center=self.difficulty_medium_button.center)
        self.screen.blit(button_text_medium, text_rect_medium)
        
        button_text_hard = self.button_font.render("Hard", True, self.black)
        text_rect_hard = button_text_hard.get_rect(center=self.difficulty_hard_button.center)
        self.screen.blit(button_text_hard, text_rect_hard)
        
        button_text_statistics = self.button_font_select_button_fonts.render("Statistics", True, self.black)
        text_rect_statistics = button_text_statistics.get_rect(center=self.statistics_button.center)
        self.screen.blit(button_text_statistics, text_rect_statistics)
        
        self.screen.blit(self.tank_imageP1, self.tank_rectP1)
        self.screen.blit(self.tank_imageP2, self.tank_rectP2)

        # empty instruction to reassign in next Frame
        self.instruction = ""
        
    def draw(self):
         # Update the display
        pygame.display.flip()
        
    def hasLockedDifficulty(self):
        if self.locked_easy == True or self.locked_medium == True or self.locked_hard:
            return True
        else:
            return False

    def hasLockedVehicle(self):
        
        if self.hasVehicleASelected == True or self.hasVehicleBSelected == True:
            return True
        else:
            return False
