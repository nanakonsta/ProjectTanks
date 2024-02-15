# Import necessary modules
import pygame
import sys
from level import Level
from signInLevelSignUp import *
import json

# Class for the initial entry level, handling connection setup
# gia na kanei connect
class EntryLevel(Level):
    
    def __init__(self, levelData, screen):
         # Initialize the entry level with specific properties
        super().__init__(levelData, screen)

        # Additional initialization for the derived class
        
        self.screen = pygame.display.set_mode((self.levelData["screen_width"], self.levelData["screen_height"]), pygame.RESIZABLE)        # Create the window
        pygame.display.set_caption("Aeroplane assault")
        self.background_image = pygame.image.load("Sprites/islandsmall.png").convert()
       
       # Additional initialization for the derived class
        # Initialize UI elements and properties
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        
        #Button
        # Set up fonts and UI elements
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 36)
        self.input_text = "localhost"
        
        # Set up font for title
        self.font_title = pygame.font.SysFont("timesnewroman", 50)  
        self.text_surface_title = self.font_title.render("Tamks", True, (228, 228, 228))  
        
        #button colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.button_color = (50, 150, 255)  # Light blue
        self.button_color_hovered = (34, 128, 235)  # darker blue
        
         # Set up fonts and UI elements
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        self.button_font_select_button_fonts = pygame.font.Font(None, 32)

        # Set up button properties
        self.button_width = self.levelData["connect_btn_width"] 
        self.button_height = self.levelData["connect_btn_height"] 
        self.button_x = self.levelData["connect_btn_width_pos"] 
        self.button_y = self.levelData["connect_btn_height_pos"] 

        self.connect_button = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        
       # Load and initialize sounds
        self.click_sound = pygame.mixer.Sound(self.levelData["click_sound_path"]) 
        self.type_sound = pygame.mixer.Sound(self.levelData["type_sound_path"])  



        
    def update(self, events):
        # Handle user input and update UI elements
            # Handle events such as quitting, key presses, mouse clicks, etc
        for event in events:
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Handle key presses for entering server address
                 # Handle keyboard input events 
                 if event.key == pygame.K_RETURN:
                     input_active = False
                 elif event.key == pygame.K_BACKSPACE:
                     self.input_text = self.input_text[:-1]
                 else:
                     self.type_sound.play()
                     self.input_text += event.unicode
                     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse button down events
                 # Handle mouse clicks for connecting to the server
                if event.button == 1 and self.connect_button.collidepoint(event.pos):  # Left mouse button
                    # Handle the action when the connect button is clicked
                    self.clientGameManager.getNetworkManager().setHost(self.input_text)
                    result = self.clientGameManager.getNetworkManager().connect()   
                    if result == True:                                       
                        level_data = ""
                        with open("LevelsData/EntryScene.json", "r") as file:
                            level_data = json.load(file)
                        newLevel = SignInLevel(level_data, self.screen) 
                        self.clientGameManager.switchLevel(newLevel)
                    
                    else:
                        print(result)
                    self.click_sound.play()
            if event.type == pygame.MOUSEMOTION:  
                # Handle mouse motion events       
                self.mouse_position_x, self.mouse_position_y = event.pos
    # Draw UI elements on the screen # Other update code
        self.screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(self.screen, self.button_color, self.connect_button)
        pygame.draw.rect(self.screen, self.black, self.connect_button, 2) 
        # Draw the button
        if self.connect_button.collidepoint((self.mouse_position_x, self.mouse_position_y)):            
            pygame.draw.rect(self.screen, self.button_color_hovered, self.connect_button)
            pygame.draw.rect(self.screen, self.black, self.connect_button, 2)
            
        # Draw the title
        text_rect_title = self.text_surface_title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(self.text_surface_title, text_rect_title)
        
        # Button text
        button_text = self.button_font.render("Connect", True, self.black)
        text_rect = button_text.get_rect(center=self.connect_button.center)
        self.screen.blit(button_text, text_rect)
        
        # self.screen.blit(self.button_text, self.connect_button.topleft)

        # Render the input text
        self.input_render = self.input_font.render("Enter server to connect: " + self.input_text, True, (228, 228, 228))
        self.screen.blit(self.input_render, (150, 260))

    def draw(self):
         # Update the display # Draw the UI elements on the screen
        pygame.display.flip()

