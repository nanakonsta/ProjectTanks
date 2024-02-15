
from tank import *
from tankEnum import * 
from enum import Enum



class TankFactory:
    
    def __init__(self):
        
        # Data to create the tanks
        self.p1BasePath = "Sprites/tankP1Base.png"
        self.p1TopPath = "Sprites/tankP1Top.png"
        self.p2BasePath = "Sprites/tankP2Base.png"
        self.p2TopPath = "Sprites/tankP2Top.png"
        self.e1BasePath = "Sprites/tankEnemy1Base.png"
        self.e1TopPath = "Sprites/tankEnemy1Top.png"
        self.e2BasePath = "Sprites/tankEnemy2Base.png"
        self.e2TopPath = "Sprites/tankEnemy2Top.png"
                
    def constructTank(self, tankType, tank_pos_x, tank_pos_y, distanceTostop = 0, fireRate = 200, health = 100, gameManager = None):
        match tankType:
            case tankType.P1:
                p1 = TankBase(tank_pos_x,tank_pos_y,self.p1BasePath,2, 3, tankType.P1, 0, health, gameManager)
                tank_turret = TankTurret(p1, self.p1TopPath, fireRate)
                p1.tank_turret = tank_turret
                p1.add_child(tank_turret)
                return p1  
            case tankType.P2:
                p2 = TankBase(tank_pos_x,tank_pos_y,self.p2BasePath,2, 3,tankType.P2, 0, health, gameManager)
                tank_turret = TankTurret(p2, self.p2TopPath, fireRate)
                p2.tank_turret = tank_turret
                p2.add_child(tank_turret)
                return p2  
            case tankType.E1:
                e1 = TankBase(tank_pos_x,tank_pos_y,self.e1BasePath,2, 3, tankType.E1, distanceTostop, health, gameManager)
                tank_turret = TankTurret(e1, self.e1TopPath, fireRate)
                e1.tank_turret = tank_turret
                e1.add_child(tank_turret)
                return e1 
             
            case tankType.E2:
                e2 = TankBase(tank_pos_x,tank_pos_y,self.e2BasePath,2, 3, tankType.E2,distanceTostop, health, gameManager)
                tank_turret = TankTurret(e2, self.e2TopPath, fireRate)
                e2.tank_turret = tank_turret
                e2.add_child(tank_turret)
                return e2 