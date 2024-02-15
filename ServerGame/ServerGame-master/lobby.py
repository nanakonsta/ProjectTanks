import json
class Lobby: #diaxeirizetai to json arxeio to opoio sunxronizei data se server kai client
    def __init__(self):

        self.lobby_data = {
            "difficulty": {
                "easyLocked": False,
                "mediumLocked": False,
                "hardLocked": False
            },
            "vehicles": {
                "vehicleALocked": False,
                "vehicleBLocked": False
            },
            "readyStatus": {
                "ready_Player1Locked": False,
                "ready_Player2Locked": False
            }
        }
        
    
    
    def idDifficultyLocked(self):
        
        if self.lobby_data["difficulty"]["easyLocked"] == True or self.lobby_data["difficulty"]["mediumLocked"] == True or self.difficulty_levels["difficulty"]["hardLocked"] == True:
            return True
        else :
            False 
    
    def lockVehicleA(self):
        if self.isVehicleLocked("vehicleALocked") == False:
            self.lobby_data["vehicles"]["vehicleALocked"] = True
            return True
        else:
            return False            
    
    def lockVehicleB(self):
        if self.isVehicleLocked("vehicleBLocked") == False:
            self.lobby_data["vehicles"]["vehicleBLocked"] = True
            return True
        else:
            return False                  
                      
    def lockEasy(self):
        if self.lobby_data["difficulty"]["easyLocked"] == False and self.lobby_data["difficulty"]["mediumLocked"] == False and self.lobby_data["difficulty"]["hardLocked"] == False:
           self.lobby_data["difficulty"]["easyLocked"] = True           

    
    def lockMedium(self):
        if self.lobby_data["difficulty"]["easyLocked"] == False and self.lobby_data["difficulty"]["mediumLocked"] == False and self.lobby_data["difficulty"]["hardLocked"] == False:
           self.lobby_data["difficulty"]["mediumLocked"] = True
                     
    def lockHard(self):
        if self.lobby_data["difficulty"]["easyLocked"] == False and self.lobby_data["difficulty"]["mediumLocked"] == False and self.lobby_data["difficulty"]["hardLocked"] == False:
           self.lobby_data["difficulty"]["hardLocked"] = True          
            
    def isVehicleLocked(self, vehicle):
        
        if self.lobby_data["vehicles"][vehicle] == True:
            return True
        else :
            return False 
    
    def lockPlayer(self, p):
        if p == "p1" and self.lobby_data["readyStatus"]["ready_Player1Locked"] == False:
            self.lobby_data["readyStatus"]["ready_Player1Locked"] = True
        if p == "p2" and self.lobby_data["readyStatus"]["ready_Player2Locked"] == False:
            self.lobby_data["readyStatus"]["ready_Player2Locked"] = True
                
    def isPlayerReadyLocked(self, ready_Player):
        
        if self.lobby_data["readyStatus"][ready_Player] == True:
            return True
        else:
            False  
    
    def bothPlayersLocked(self):
        if self.lobby_data["readyStatus"]["ready_Player1Locked"] == True and self.lobby_data["readyStatus"]["ready_Player2Locked"] == True:
            return True
        else: 
            return False
            
    def getJSONLobbyData(self):
        json_data = json.dumps(self.lobby_data)
        return json_data
    
