import json
class Player: 
    def __init__(self):
        self._username = None
        self._vehicle = None
        self._is_P1 = False
        self._is_P2 = False

    
    @property
    def is_P1(self):
        return self._is_P1

    @is_P1.setter
    def is_P1(self, value):
        self._is_P1 = value    
        
    
    @property
    def is_P2(self):
        return self._is_P2

    @is_P2.setter
    def is_P2(self, value):
        self._is_P2 = value    
        
    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value    
        
    
    @property
    def vehicle(self):
        return self._vehicle

    @vehicle.setter
    def vehicle(self, value):
        self._vehicle = value    
        
    def getPlayerStr(self):
        if self._is_P1:
            return "p1"
        elif self._is_P2:
            return "p2"
   