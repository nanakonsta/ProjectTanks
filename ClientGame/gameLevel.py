#ta panta zwgrafizei

import pygame
import sys
from level import Level
from player import Player
from tankEnum import TankEnum
import json
from tankFactory import *
# h kentrikh pista
class GameLevel(Level):
    
    def __init__(self, levelData, screen):
        super().__init__(levelData, screen)
        self.clientGameManager = None
        self.width, self.height = (800, 400)
        self.screen = pygame.display.set_mode((self.width, self.height))
    #initialization code
        self.background_image = pygame.image.load("Sprites/Martian_Soil.png").convert()
        self.castle = pygame.image.load("Sprites/castle_4.png").convert_alpha()
        self.castle_rect = pygame.Rect(0, 0, self.castle.get_width(), self.castle.get_height())

        # Calculate the position to center the castle image
        self.castle_rect.center = ( self.width // 2, self.height // 2)
        self.is_p1 = False
        self.is_p2 = False
        self.p = ""
        self.post_player_data_set = False
        self.font = pygame.font.Font(None, 36)
        self.castle_health = ""
        
        self.player1Tank = None
        self.player1_health = ""
        self.player1_score = ""
                
        self.player2Tank = None
        self.player2_health = ""
        self.player2_score = ""
        # Initialize empty rectangles
        self.p1_rect_base = pygame.Rect(0,0,0,0)
        self.p1_rect_turret = pygame.Rect(0,0,0,0)
        self.p1_angle_base = 0
        self.p1_angle_turret = 0
        self.p2_rect_base = pygame.Rect(0,0,0,0)
        self.p2_rect_turret = pygame.Rect(0,0,0,0)
        self.p2_angle_turret_base = 0
        self.p2_angle_turret_turret = 0
        
                
        self.player1hasSpawned, self.player2hasSpawned  = False, False
        self.tankFactory = TankFactory()
        self.players = []
        self.enemies = []
        self.networkBullets = []
        self.playerBullets = []
        
    def update(self, events):
    
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
                
        # Draw the background        
        self.screen.blit(self.background_image, (0, 0))
        
        # Set up player data if not already done
        if self.clientGameManager is not None and self.post_player_data_set == False:
            self.setPlayerData()
        # Update player data based on the client's tank type
        player1 = next((obj for obj in self.players if obj.p1orp2 == "p1"), None)
        if player1 is not None and self.is_p1 == True:
            self.updatePlayerData(player1)

        player2 = next((obj for obj in self.players if obj.p1orp2 == "p2"), None)
        if player2 is not None and self.is_p2 == True:
            self.updatePlayerData(player2)
    

       # Sending data to the server       
        json_data = json.dumps(self.constructGameData(player1, player2), default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o))
        self.clientGameManager.getNetworkManager().sendJSON(json_data)
        
        
        # Receiving and updating data from the server
        response = self.clientGameManager.getNetworkManager().receive()
        
        json_data_received = json.loads(response)
        
        
        if len(self.players) < 2:
            self.spawnPlayers(json_data_received)
        
        self.updateNetworkGameObjects(json_data_received)         
        self.drawUIElements()
        self.screen.blit(self.castle, self.castle_rect)

    def draw(self):
        pygame.display.flip()
    
    def updateNetworkBullets(self):
        for networkBullet in self.networkBullets:
            networkBullet.updateState()
            networkBullet.drawTank(self.screen)
            
    # Handling player input (movement) based on tank type        
    def handlePlayerInput(self, ws_input, ad_input):
        if self.is_p1:
            # Update the position of the tank for player 1
            movement_speed = 5
            self.tankP1_pos_x += ad_input * movement_speed
            self.tankP1_pos_y += ws_input * movement_speed
            # Update the tank's rect to reflect the new position
            self.tank_baseP1_rect = pygame.Rect(self.tank_baseP1.get_rect(center=(self.tankP1_pos_x, self.tankP1_pos_y)))
        elif self.is_p2:
            # Handle input for player 2 if needed
            pass
        
    def setPlayerData(self):
        # Set player data based on client's tank type
        self.post_player_data_set = True
        self.is_p1 = self.clientGameManager.player.is_P1
        self.is_p2 = self.clientGameManager.player.is_P2

        if self.is_p1:
            self.p = "p1"
        elif self.is_p2:
            self.p = "p2"

    def updateNetworkGameObjects(self, json_data_received):
        if self.is_p1 == False:
            rect_base_x = json_data_received.get('player1', {}).get('rect_base_x', 0)
            rect_base_y = json_data_received.get('player1', {}).get('rect_base_y', 0)
            rect_base_height = json_data_received.get('player1', {}).get('rect_base_height', 0)
            rect_base_width = json_data_received.get('player1', {}).get('rect_base_width', 0)
            angle_base = json_data_received.get('player1', {}).get('angle_base', 0)
            rect_turret_x = json_data_received.get('player1', {}).get('rect_turret_x', 0)
            rect_turret_y = json_data_received.get('player1', {}).get('rect_turret_y', 0)
            rect_turret_height = json_data_received.get('player1', {}).get('rect_turret_height', 0)
            rect_turret_width = json_data_received.get('player1', {}).get('rect_turret_width', 0)
            angle_turret = json_data_received.get('player1', {}).get('angle_turret', 0)
            
            
            
            self.p1_rect_base.x = rect_base_x
            self.p1_rect_base.y = rect_base_y
            self.p1_rect_base.height = rect_base_height
            self.p1_rect_base.width = rect_base_width            
            self.p1_angle_base = angle_base
            self.p1_rect_turret.x = rect_turret_x
            self.p1_rect_turret.y = rect_turret_y
            self.p1_rect_turret.width = rect_turret_width
            self.p1_rect_turret.height = rect_turret_height
            self.p1_angle_turret = angle_turret

            player1 = next((obj for obj in self.players if obj.p1orp2 == "p1"), None)
            if player1 is not None:
                player1.updateNetworkData(self.p1_angle_base, self.p1_angle_turret, self.p1_rect_base, self.p1_rect_turret)            
                player1.drawTankNetwork(self.screen, self.p1_rect_base, self.p1_rect_turret)           
                player1.drawTank(self.screen)


            
        elif self.is_p2 == False:
            rect_base_x = json_data_received.get('player2', {}).get('rect_base_x', 0)
            rect_base_y = json_data_received.get('player2', {}).get('rect_base_y', 0)
            rect_base_height = json_data_received.get('player2', {}).get('rect_base_height', 0)
            rect_base_width = json_data_received.get('player2', {}).get('rect_base_width', 0)
            angle_base = json_data_received.get('player2', {}).get('angle_base', 0)
            rect_turret_x = json_data_received.get('player2', {}).get('rect_turret_x', 0)
            rect_turret_y = json_data_received.get('player2', {}).get('rect_turret_y', 0)
            rect_turret_height = json_data_received.get('player2', {}).get('rect_turret_height', 0)
            rect_turret_width = json_data_received.get('player2', {}).get('rect_turret_width', 0)
            angle_turret = json_data_received.get('player2', {}).get('angle_turret', 0)
            self.p2_rect_base.x = rect_base_x
            self.p2_rect_base.y = rect_base_y
            self.p2_rect_base.height = rect_base_height
            self.p2_rect_base.width = rect_base_width            
            self.p2_angle_base = angle_base
            self.p2_rect_turret.x = rect_turret_x
            self.p2_rect_turret.y = rect_turret_y
            self.p2_rect_turret.width = rect_turret_width
            self.p2_rect_turret.height = rect_turret_height
            self.p2_angle_turret = angle_turret
            
            player2 = next((obj for obj in self.players if obj.p1orp2 == "p2"), None)
            if player2 is not None:
                player2.updateNetworkData(self.p2_angle_base, self.p2_angle_turret, self.p2_rect_base, self.p2_rect_turret) 
                player2.drawTankNetwork(self.screen, self.p2_rect_base, self.p2_rect_turret)
                player2.drawTank(self.screen)
        
        
        #self.addBulletstoList(json_data_received.get('network_bullets', {}))
        self.updateNetworkBullets()
    
    
    def addBulletstoList(self, bullets):
        # Add bullets from the server to the local list
        print(type(bullets))
        for bullet in bullets:
            bullet_id = bullet["id"]
            bullet = next((obj for obj in self.players if obj.id == bullet_id), None)
            if bullet is None:
                continue
            self.networkBullets.append(NetworkBullet(bullet["rect_x"], bullet["rect_y"],bullet["height"],bullet["width"],bullet["id"]))
                
    def constructGameData(self, player1, player2):
        game_data = {}
        

        if self.is_p1:
            game_data = {
                "player1": {
                    "spawned": self.player1hasSpawned,
                    "rect_base_x": getattr(player1, 'base_net_rect_x', 0),
                    "rect_base_y": getattr(player1, 'base_net_rect_y', 0),
                    "rect_base_width": getattr(player1, 'base_net_rect_width', 0),
                    "rect_base_height": getattr(player1, 'base_net_rect_height', 0),
                    "angle_base": getattr(player1, 'base_net_angle', 0),
                    "rect_turret_x": getattr(player1.tank_turret, 'turret_net_rect_x', 0) if player1 is not None else 0,
                    "rect_turret_y": getattr(player1.tank_turret, 'turret_net_rect_y', 0) if player1 is not None else 0,
                    "rect_turret_height": getattr(player1.tank_turret, 'turret_net_rect_height', 0) if player1 is not None else 0,
                    "rect_turret_width": getattr(player1.tank_turret, 'turret_net_rect_width', 0) if player1 is not None else 0,
                    "angle_turret": getattr(player1.tank_turret, 'turret_net_angle', 0) if player1 is not None else 0,
                    "networkBullets": [bullet.__dict__ for bullet in self.playerBullets]
                }
            }
        elif self.is_p2:
            game_data = {
                "player2": {
                    "spawned": self.player2hasSpawned,
                    "rect_base_x": getattr(player2, 'base_net_rect_x', 0),
                    "rect_base_y": getattr(player2, 'base_net_rect_y', 0),
                    "rect_base_width": getattr(player2, 'base_net_rect_width', 0),
                    "rect_base_height": getattr(player2, 'base_net_rect_height', 0),
                    "angle_base": getattr(player2, 'base_net_angle', 0),
                    "rect_turret_x": getattr(player2.tank_turret, 'turret_net_rect_x', 0) if player2 is not None else 0,
                    "rect_turret_y": getattr(player2.tank_turret, 'turret_net_rect_y', 0) if player2 is not None else 0,
                    "rect_turret_height": getattr(player2.tank_turret, 'turret_net_rect_height', 0) if player2 is not None else 0,
                    "rect_turret_width": getattr(player2.tank_turret, 'turret_net_rect_width', 0) if player2 is not None else 0,
                    "angle_turret": getattr(player2.tank_turret, 'turret_net_angle', 0) if player2 is not None else 0,
                    "networkBullets": [bullet.__dict__ for bullet in self.playerBullets]
                }
            }

        return game_data
    
    def drawUIElements(self):
        player_health, player_score = 0, 0
        
        if self.is_p1 ==True:
            player_health = self.player1_health
            player_score = self.player1_score
        elif self.is_p2 == True:
           player_health = self.player2_health 
           player_score = self.player2_score
        
        player_health_text = self.font.render(f"Player Health: {player_health}", True, (255, 255, 255))
        self.screen.blit(player_health_text, (self.width - player_health_text.get_width() - 50, self.height - player_health_text.get_height() - 20))

        player_score_text = self.font.render(f"Player Score: {player_score}", True, (255, 255, 255))
        self.screen.blit(player_score_text, (self.width - player_score_text.get_width() - 50, 10))

        castle_health_text = self.font.render(f"Castle Health: {self.castle_health}", True, (255, 255, 255))
        self.screen.blit(castle_health_text, (10, self.height - castle_health_text.get_height() - 10))
        
    def spawnPlayer(self, tankType, playerHealth, playerFireRate, spawnX, spawnY):
        # Spawn a player based on tank type
        if self.is_p1 == True and tankType == TankEnum.P1:
            self.players.append(self.tankFactory.constructTank(tankType,spawnX,spawnY, 0, playerFireRate, playerHealth, None, "p1"))
        elif self.is_p1 == True and tankType == TankEnum.P2:
            self.players.append(self.tankFactory.constructTank(tankType,spawnX,spawnY, 0, playerFireRate, playerHealth, None, "p2"))
        if self.is_p2 == True and tankType == TankEnum.P2:
            self.players.append(self.tankFactory.constructTank(tankType,spawnX,spawnY, 0, playerFireRate, playerHealth, None, "p2"))
        elif self.is_p2 == True and tankType == TankEnum.P1:
            self.players.append(self.tankFactory.constructTank(tankType,spawnX,spawnY, 0, playerFireRate, playerHealth, None, "p1"))
            
    def spawnPlayers(self, json_data_received):
        # Spawn players based on data received from the server
        
        player1 = next((obj for obj in self.players if obj.p1orp2 == "p1"), None)
        player2 = next((obj for obj in self.players if obj.p1orp2 == "p2"), None)

        if json_data_received.get('player1', {}).get('spawned', None) is not None and json_data_received.get('player2', {}).get('spawned', None)  is not None:
            if len(self.players) < 2:
                if player1 is None:
                    self.player1_health = json_data_received.get('player1', {}).get('health', None)
                    player1FireRate = json_data_received.get('player1', {}).get('fireRate', None)            
                    spawnX = json_data_received.get('player1', {}).get('spawnX', None)
                    spawnY = json_data_received.get('player1', {}).get('spawnY', None)
                    self.spawnPlayer(TankEnum.P1, self.player1_health, player1FireRate, spawnX, spawnY)
                    self.player1hasSpawned = True
                                        
                if player2 is None:
                    self.player2_health = json_data_received.get('player2', {}).get('health', None)
                    player2FireRate = json_data_received.get('player2', {}).get('fireRate', None)        
                    spawnX = json_data_received.get('player2', {}).get('spawnX', None)
                    spawnY = json_data_received.get('player2', {}).get('spawnY', None)            
                    self.spawnPlayer(TankEnum.P2, self.player2_health, player2FireRate, spawnX, spawnY)
                    self.player2hasSpawned = True
                 

    def updateNetWorkData(self, json_data_received):
         # Update network data if needed
        if self.is_p1 == True:
            player2 = next((obj for obj in self.players if obj.p1orp2 == "p2"), None)
        if self.is_p2 == True:    
            player1 = next((obj for obj in self.players if obj.p1orp2 == "p1"), None)

                
    def updatePlayerData(self, player):
        # Update player data based on input and draw the tank
        keys = pygame.key.get_pressed()
        rotatingClockwise, rotatingAntiClockwise = False, False
        if keys[pygame.K_a]:
            rotatingClockwise = True
        if keys[pygame.K_d]:
            rotatingAntiClockwise = True        
        playerMoveForwards, playerMoveBackwards = False, False
        if keys[pygame.K_w]:
            playerMoveForwards = True        
        if keys[pygame.K_s]:
            playerMoveBackwards = True
            
                 
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:
            if player.tank_turret.bulletInstatiatedTimer == False:
                player.tank_turret.fireCannon()
        
        player.updateState(playerMoveForwards, playerMoveBackwards, rotatingClockwise, rotatingAntiClockwise)
        player.drawTank(self.screen)  
              
