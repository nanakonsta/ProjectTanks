class Player: 
    def __init__(self):
        self._username = None
        self._vehicle = None
        self.isPlayer1 = False
        self.isPlayer2 = False
        self.health = 0
        self.fireRate = 0
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
        
        