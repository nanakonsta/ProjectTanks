from mode import Mode
import json
class GameMode(Mode):
    
    def __init__(self, screen,gameManager, gameRunner):
        super().__init__(screen)
        self.game_manager = gameManager
        self.game_runner = gameRunner

        self.player1_spawned = False
        self.player2_spawned = False
        self
        self.game_data = {}
        self.player1_base_rect_x = 0
        self.player1_base_rect_y = 0
        self.player1_base_rect_height = 0
        self.player1_base_rect_width = 0
        self.player1_base_angle = 0
        self.player1_ect_x = 0
        self.player1_turret_rect_y = 0
        self.player1_turret_rect_height = 0
        self.player1_turret_rect_width = 0
        self.player1_turret_angle = 0
        
        self.player2_base_rect_x = 0
        self.player2_base_rect_y = 0
        self.player2_base_rect_height = 0
        self.player2_base_rect_width = 0
        self.player2_base_angle = 0
        self.player2_turret_rect_x = 0
        self.player2_turret_rect_y = 0
        self.player2_turret_rect_height = 0
        self.player2_turret_rect_width = 0
        self.player2_turret_angle = 0
    def update(self):
        self.screen.fill((255, 255, 255))
        
        if self.dataP1 is not None:
            if self.player1_spawned == False:
                self.player1_spawned = self.dataP1.get('player1', {}).get('spawned', None)
            self.player1_base_rect_x = self.dataP1.get('player1', {}).get('rect_base_x', None)
            self.player1_base_rect_y = self.dataP1.get('player1', {}).get('rect_base_y', None)
            self.player1_base_rect_height = self.dataP1.get('player1', {}).get('rect_base_height', None)
            self.player1_base_rect_width = self.dataP1.get('player1', {}).get('rect_base_width', None)
            self.player1_base_angle = self.dataP1.get('player1', {}).get('angle_base', None)
            self.player1_turret_rect_x = self.dataP1.get('player1', {}).get('rect_turret_x', None)
            self.player1_turret_rect_y = self.dataP1.get('player1', {}).get('rect_turret_y', None)
            self.player1_turret_rect_height = self.dataP1.get('player1', {}).get('rect_turret_height', None)
            self.player1_turret_rect_width = self.dataP1.get('player1', {}).get('rect_turret_width', None)
            self.player1_turret_angle = self.dataP1.get('player1', {}).get('angle_turret', None) 

        if self.dataP2 is not None: 
            if self.player2_spawned == False:
                self.player2_spawned = self.dataP2.get('player2', {}).get('spawned', None)
            self.player2_base_rect_x = self.dataP2.get('player2', {}).get('rect_base_x', None)
            self.player2_base_rect_y = self.dataP2.get('player2', {}).get('rect_base_y', None)
            self.player2_base_rect_height = self.dataP2.get('player2', {}).get('rect_base_height', None)
            self.player2_base_rect_width = self.dataP2.get('player2', {}).get('rect_base_width', None)
            self.player2_base_angle = self.dataP2.get('player2', {}).get('angle_base', None)
            self.player2_turret_rect_x = self.dataP2.get('player2', {}).get('rect_turret_x', None)
            self.player2_turret_rect_y = self.dataP2.get('player2', {}).get('rect_turret_y', None)
            self.player2_turret_rect_height = self.dataP2.get('player2', {}).get('rect_turret_height', None)
            self.player2_turret_rect_width = self.dataP2.get('player2', {}).get('rect_turret_width', None)
            self.player2_turret_angle = self.dataP2.get('player2', {}).get('angle_turret', None)    
            
        self.game_data = {
            "player1" :{
                "spawned": self.player1_spawned,
                "health": self.game_manager.player1.health,
                "fireRate": self.game_manager.player1.fireRate,
                "spawnX": 250,
                "spawnY": 200,
                "rect_base_x": self.player1_base_rect_x,
                "rect_base_y": self.player1_base_rect_y,
                "rect_base_height": self.player1_base_rect_height,
                "rect_base_width": self.player1_base_rect_width,
                "angle_base": self.player1_base_angle,
                "rect_turret_x": self.player1_turret_rect_x,
                "rect_turret_y": self.player1_turret_rect_y,
                "rect_turret_height": self.player1_turret_rect_height,
                "rect_turret_width": self.player1_turret_rect_width,
                "angle_turret": self.player1_turret_angle
            },
            "player2":{
                "spawned": self.player2_spawned,
                "health": self.game_manager.player2.health,
                "fireRate": self.game_manager.player2.fireRate,
                "spawnX": 500,
                "spawnY": 200,
                "rect_base_x": self.player2_base_rect_x,
                "rect_base_y": self.player2_base_rect_y,
                "rect_base_height": self.player2_base_rect_height,
                "rect_base_width": self.player2_base_rect_width,
                "angle_base": self.player2_base_angle,
                "rect_turret_x": self.player2_turret_rect_x,
                "rect_turret_y": self.player2_turret_rect_y,
                "rect_turret_height": self.player2_turret_rect_height,
                "rect_turret_width": self.player2_turret_rect_width,
                "angle_turret": self.player2_turret_angle
            }
        }

    def draw(self):
        super().draw()

    def getJSONgameModeData(self):
        json_data = json.dumps(self.game_data)

        return json_data