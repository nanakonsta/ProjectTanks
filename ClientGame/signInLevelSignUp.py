
import pygame
import sys
from level import Level
from lobbyLevel import LobbyLevel

import json

class SignInLevel(Level):
    
    def __init__(self, levelData, screen):
        super().__init__(levelData, screen)

        # Additional initialization for the derived class
        self.clientGameManager = None
        self.screen = pygame.display.set_mode((self.levelData["screen_width"], self.levelData["screen_height"]),pygame.RESIZABLE)        # Create the window
        pygame.display.set_caption("Aeroplane assault")
        self.background_image = pygame.image.load("Sprites/island.png").convert() 
        #path tha mpei url arxeiou eikonas fontou pou thelw na valw gia fonto arxikh othoni
                
        self.font_error = pygame.font.SysFont("timesnewroman", 32)  
        self.error_text = self.font_error.render("", True, (255, 50, 50))
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        #Button
        # Set up fonts
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 36)
        self.input_text_username = ""
        self.input_text_password = ""
        # Set up font for title
        self.font_title = pygame.font.SysFont("timesnewroman", 50)  # Use Times New Roman font, size 72
        self.text_surface_title = self.font_title.render("Aeroplane Assault", True, (228, 228, 228))  
        #c:\Users\user\Desktop\island.jpg
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.button_color = (50, 150, 255)  # Light blue

        self.button_color_hovered = (34, 128, 235)  # darker blue
        # Fonts
        #self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        self.button_font_select_button_fonts = pygame.font.Font(None, 32)

        # Button properties
        # same properties as connect button
        self.active_username = True
        self.active_password = False
        
        self.sign_in_button_width = self.levelData["connect_btn_width"] 
        self.sign_in_button_height = self.levelData["connect_btn_height"] 
        self.sign_in_button_x = self.levelData["connect_btn_width_pos"] 
        self.sign_in_button_y = self.levelData["connect_btn_height_pos"] 
        
        self.sign_in_button = pygame.Rect(self.sign_in_button_x,  self.sign_in_button_y, self.sign_in_button_width, self.sign_in_button_height)
        self.sign_up_button = pygame.Rect(self.sign_in_button_x,  self.sign_in_button_y + 90, self.sign_in_button_width, self.sign_in_button_height)
        
        
        self.username_w = self.levelData["connect_btn_width" ] - 20
        self.password_H = self.levelData["connect_btn_height"] - 30
        self.username_x = (200, 250)
        self.password_y = (200, 310)
        
        self.username_select_button = pygame.Rect(500, 200,self.sign_in_button_width, self.sign_in_button_height -20)
        self.password_select_button = pygame.Rect(500 , 250, self.sign_in_button_width, self.sign_in_button_height -20)
        #Sounds
        self.click_sound = pygame.mixer.Sound(self.levelData["click_sound_path"]) 
        self.type_sound = pygame.mixer.Sound(self.levelData["type_sound_path"])  

    def setClientGameManager(self, _clientGameManager):
        self.clientGameManager = _clientGameManager 
    
    
    def update(self, events):
               
        for event in events:
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_username == True and self.active_password == False:                        
                        self.input_text_username = self.input_text_username[:-1]
                    elif self.active_username == False and self.active_password == True:
                        self.input_text_password = self.input_text_password[:-1]
                else:
                    if self.active_username == True and self.active_password == False:
                        if len(self.input_text_username) < 9:                                                  
                            self.input_text_username += event.unicode                        
                    elif self.active_username == False and self.active_password == True:
                        if len(self.input_text_password) < 9:
                            self.input_text_password += event.unicode   
                    self.type_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and  self.sign_in_button.collidepoint(event.pos):  # Left mouse button
                    level_data = ""
                    with open("LevelsData/EntryScene.json", "r") as file:
                        level_data = json.load(file)
                    username_input = self.input_text_username
                    password_Input = self.input_text_password
                    data_to_server = {
                        "cred_sign_in": {
                            "username": f"{username_input}",
                            "password": f"{password_Input}"
                        }
                    }
                    self.clientGameManager.getNetworkManager().send(data_to_server)
                    response = self.clientGameManager.getNetworkManager().receive()
                    response_values = str(response).split('|')
                    if response_values[0] == "200 OK":
                        if response_values[1] == "p1":
                            self.clientGameManager.player.is_P1 = True
                        elif response_values[1] == "p2":
                            self.clientGameManager.player.is_P2 = True
                        self.clientGameManager.player.username = username_input
                        newLevel = LobbyLevel(level_data, self.screen)
                        self.clientGameManager.switchLevel(newLevel)
                    else:
                        self.error_text = self.font_error.render(response, True, (250, 10, 10))  
                    self.click_sound.play()
                elif event.button == 1 and self.sign_up_button.collidepoint(event.pos):
                    level_data = ""
                    with open("LevelsData/EntryScene.json", "r") as file:
                        level_data = json.load(file)
                    newLevel = SignUpLevel(level_data, self.screen)
                    self.clientGameManager.switchLevel(newLevel)
                    self.click_sound.play()
                elif event.button == 1 and self.username_select_button.collidepoint(event.pos):    
                    self.active_username = True
                    self.active_password = False
                elif event.button == 1 and self.password_select_button.collidepoint(event.pos):    
                    self.active_username = False
                    self.active_password = True
            if event.type == pygame.MOUSEMOTION:         
                self.mouse_position_x, self.mouse_position_y = event.pos

        self.screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(self.screen, self.button_color, self.sign_in_button)
        pygame.draw.rect(self.screen, self.black, self.sign_in_button, 2) 
        # Draw the button
        if self.sign_in_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.sign_in_button)
            pygame.draw.rect(self.screen, self.black, self.sign_in_button, 2)
            
        pygame.draw.rect(self.screen, self.button_color, self.sign_up_button)
        pygame.draw.rect(self.screen, self.black, self.sign_up_button, 2) 
        # Draw the button
        if self.sign_up_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.sign_up_button)
            pygame.draw.rect(self.screen, self.black, self.sign_up_button, 2)
        
        pygame.draw.rect(self.screen, self.button_color, self.username_select_button)
        pygame.draw.rect(self.screen, self.black, self.username_select_button, 2) 
        # Draw the button
        if self.username_select_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):                     
           pygame.draw.rect(self.screen, self.button_color_hovered, self.username_select_button)
           pygame.draw.rect(self.screen, self.black, self.username_select_button, 2)    
        
        pygame.draw.rect(self.screen, self.button_color, self.password_select_button)
        pygame.draw.rect(self.screen, self.black, self.password_select_button, 2) 
        # Draw the button
        if self.password_select_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):                     
           pygame.draw.rect(self.screen, self.button_color_hovered, self.password_select_button)
           pygame.draw.rect(self.screen, self.black, self.password_select_button, 2)        
        # Draw the title
        text_rect_title = self.text_surface_title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(self.text_surface_title, text_rect_title)
        
        # Button text
        button_text = self.button_font.render("Sign in", True, self.black)
        text_rect = button_text.get_rect(center=self.sign_in_button.center)
        self.screen.blit(button_text, text_rect)

        # self.screen.blit(self.button_text, self.connect_button.topleft)
        button_text_sign_up = self.button_font.render("Sign up", True, self.black)
        text_rect_sign_up = button_text_sign_up.get_rect(center=self.sign_up_button.center)
        self.screen.blit(button_text_sign_up, text_rect_sign_up)
        
        
        button_text_select_username = self.button_font_select_button_fonts.render("fill in username", True, self.black)
        text_rect_select_username = button_text_select_username.get_rect(center=self.username_select_button.center)
        self.screen.blit(button_text_select_username, text_rect_select_username)
        
        button_text_select_password = self.button_font_select_button_fonts.render("fill in password", True, self.black)
        text_rect_select_password = button_text_select_password.get_rect(center=self.password_select_button.center)
        self.screen.blit(button_text_select_password, text_rect_select_password)
        # Render the input text+
        input_render = self.input_font.render("Username: " + self.input_text_username, True, (228, 228, 228))
        self.screen.blit(input_render, (210, 200))

        input_render1 = self.input_font.render("Password: " + self.input_text_password, True, (228, 228, 228))
        self.screen.blit(input_render1, (210, 250))
        
        self.screen.blit(self.error_text, (200, 500))
    def draw(self):
         # Update the display
        pygame.display.flip()




class SignUpLevel(Level):
    
    def __init__(self, levelData, screen):
        super().__init__(levelData, screen)

        # Additional initialization for the derived class
        self.clientGameManager = None
        self.screen = pygame.display.set_mode((self.levelData["screen_width"], self.levelData["screen_height"]), pygame.RESIZABLE)        # Create the window
        pygame.display.set_caption("Aeroplane assault")
        self.background_image = pygame.image.load("Sprites/island.png").convert()
                
        self.font_error = pygame.font.SysFont("timesnewroman", 32)  
        self.error_text = self.font_error.render("", True, (255, 50, 50))
        
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        #Button
        # Set up fonts
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 36)
        self.input_text_username = ""
        self.input_text_password = ""
        # Set up font for title
        self.font_title = pygame.font.SysFont("timesnewroman", 50)  # Use Times New Roman font, size 72
        self.text_surface_title = self.font_title.render("Aeroplane Assault", True, (228, 228, 228))  
          
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.button_color = (50, 150, 255)  # Light blue

        self.button_color_hovered = (34, 128, 235)  # darker blue
        # Fonts
        #self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        self.button_font_select_button_fonts = pygame.font.Font(None, 32)

        # Button properties
        # same properties as connect button
        self.active_username = True
        self.active_password = False
        
        self.sign_in_button_width = self.levelData["connect_btn_width"] 
        self.sign_in_button_height = self.levelData["connect_btn_height"] 
        self.sign_in_button_x = self.levelData["connect_btn_width_pos"] 
        self.sign_in_button_y = self.levelData["connect_btn_height_pos"] 
        
        self.sign_in_button = pygame.Rect(self.sign_in_button_x,  self.sign_in_button_y +90, self.sign_in_button_width, self.sign_in_button_height)
        self.sign_up_button = pygame.Rect(self.sign_in_button_x,  self.sign_in_button_y , self.sign_in_button_width, self.sign_in_button_height)
        
        
        self.username_w = self.levelData["connect_btn_width" ] - 20
        self.password_H = self.levelData["connect_btn_height"] - 30
        self.username_x = (200, 250)
        self.password_y = (200, 310)
        
        self.username_select_button = pygame.Rect(500, 200,self.sign_in_button_width, self.sign_in_button_height -20)
        self.password_select_button = pygame.Rect(500 , 250, self.sign_in_button_width, self.sign_in_button_height -20)
        #Sounds
        self.click_sound = pygame.mixer.Sound(self.levelData["click_sound_path"]) 
        self.type_sound = pygame.mixer.Sound(self.levelData["type_sound_path"])  

        

    def setClientGameManager(self, _clientGameManager):
        self.clientGameManager = _clientGameManager 
    
    
    def update(self, events):
               
        for event in events:
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_username == True and self.active_password == False:                        
                        self.input_text_username = self.input_text_username[:-1]
                    elif self.active_username == False and self.active_password == True:
                        self.input_text_password = self.input_text_password[:-1]
                else:
                    if self.active_username == True and self.active_password == False:
                        if len(self.input_text_username) < 9:                                                  
                            self.input_text_username += event.unicode                        
                    elif self.active_username == False and self.active_password == True:
                        if len(self.input_text_password) < 9:
                            self.input_text_password += event.unicode   
                    self.type_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and  self.sign_in_button.collidepoint(event.pos):  # Left mouse button
                    level_data = ""
                    with open("LevelsData/EntryScene.json", "r") as file:
                        level_data = json.load(file)

                        newLevel = SignInLevel(level_data, self.screen)
                        self.clientGameManager.switchLevel(newLevel)

                    self.click_sound.play()
                elif event.button == 1 and self.sign_up_button.collidepoint(event.pos):
                    level_data = ""
                    with open("LevelsData/EntryScene.json", "r") as file:
                        level_data = json.load(file)
                    username_input = self.input_text_username
                    password_Input = self.input_text_password
                    data_to_server = {
                        "cred_sign_up": {
                            "username": f"{username_input}",
                            "password": f"{password_Input}"
                        }
                    }
                    
                    self.clientGameManager.getNetworkManager().send(data_to_server)
                    
                    response = self.clientGameManager.getNetworkManager().receive()
                    if response == "200 OK":
                        newLevel = SignInLevel(level_data, self.screen)
                        self.clientGameManager.switchLevel(newLevel)
                    else:
                        self.error_text = self.font_error.render(response, True, (250, 10, 10))  
                    self.click_sound.play()
                elif event.button == 1 and self.username_select_button.collidepoint(event.pos):    
                    self.active_username = True
                    self.active_password = False
                elif event.button == 1 and self.password_select_button.collidepoint(event.pos):    
                    self.active_username = False
                    self.active_password = True
            if event.type == pygame.MOUSEMOTION:         
                self.mouse_position_x, self.mouse_position_y = event.pos

        self.screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(self.screen, self.button_color, self.sign_in_button)
        pygame.draw.rect(self.screen, self.black, self.sign_in_button, 2) 
        # Draw the button
        if self.sign_in_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.sign_in_button)
            pygame.draw.rect(self.screen, self.black, self.sign_in_button, 2)
            
        pygame.draw.rect(self.screen, self.button_color, self.sign_up_button)
        pygame.draw.rect(self.screen, self.black, self.sign_up_button, 2) 
        # Draw the button
        if self.sign_up_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.sign_up_button)
            pygame.draw.rect(self.screen, self.black, self.sign_up_button, 2)
        
        pygame.draw.rect(self.screen, self.button_color, self.username_select_button)
        pygame.draw.rect(self.screen, self.black, self.username_select_button, 2) 
        # Draw the button
        if self.username_select_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):                     
           pygame.draw.rect(self.screen, self.button_color_hovered, self.username_select_button)
           pygame.draw.rect(self.screen, self.black, self.username_select_button, 2)    
        
        pygame.draw.rect(self.screen, self.button_color, self.password_select_button)
        pygame.draw.rect(self.screen, self.black, self.password_select_button, 2) 
        # Draw the button
        if self.password_select_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):                     
           pygame.draw.rect(self.screen, self.button_color_hovered, self.password_select_button)
           pygame.draw.rect(self.screen, self.black, self.password_select_button, 2)        
        # Draw the title
        text_rect_title = self.text_surface_title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(self.text_surface_title, text_rect_title)
        
        # Button text
        button_text = self.button_font.render("Sign in", True, self.black)
        text_rect = button_text.get_rect(center=self.sign_in_button.center)
        self.screen.blit(button_text, text_rect)

        # self.screen.blit(self.button_text, self.connect_button.topleft)
        button_text_sign_up = self.button_font.render("register", True, self.black)
        text_rect_sign_up = button_text_sign_up.get_rect(center=self.sign_up_button.center)
        self.screen.blit(button_text_sign_up, text_rect_sign_up)
        
        
        button_text_select_username = self.button_font_select_button_fonts.render("fill in username", True, self.black)
        text_rect_select_username = button_text_select_username.get_rect(center=self.username_select_button.center)
        self.screen.blit(button_text_select_username, text_rect_select_username)
        
        button_text_select_password = self.button_font_select_button_fonts.render("fill in password", True, self.black)
        text_rect_select_password = button_text_select_password.get_rect(center=self.password_select_button.center)
        self.screen.blit(button_text_select_password, text_rect_select_password)
        # Render the input text+
        input_render = self.input_font.render("Username: " + self.input_text_username, True, (228, 228, 228))
        self.screen.blit(input_render, (210, 200))

        input_render1 = self.input_font.render("Password: " + self.input_text_password, True, (228, 228, 228))
        self.screen.blit(input_render1, (210, 250))
        
        self.screen.blit(self.error_text, (200, 500))
        
    def draw(self):
         # Update the display
        pygame.display.flip()

