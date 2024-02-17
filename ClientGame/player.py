import json
class Player: 
    def __init__(self):
        # Attributes
        self._username = None
        self._vehicle = None
        self._is_P1 = False
        self._is_P2 = False

    # Property for checking if the player is Player 1

    @property
    def is_P1(self):
        return self._is_P1

  # Setter for the is_P1 property
    @is_P1.setter
    @is_P1.setter
    def is_P1(self, value):
        self._is_P1 = value    
        
     # Property for checking if the player is Player 2
    @property
    def is_P2(self):
        return self._is_P2

   # Setter for the is_P2 property
    @is_P2.setter
    def is_P2(self, value):
        self._is_P2 = value    
        
      # Property for accessing the player's username
    @property
    def username(self):
        return self._username

 # Setter for the username property
    @username.setter
    def username(self, value):
        self._username = value    
        
    
    # Property for accessing the player's chosen vehicle
    @property
    def vehicle(self):
        return self._vehicle

   # Setter for the vehicle property
    @vehicle.setter
    def vehicle(self, value):
        self._vehicle = value    
        
         # Method to get a string identifier for the player (e.g., "p1" or "p2")
    def getPlayerStr(self):
        if self._is_P1:
            return "p1"
        elif self._is_P2:
            return "p2"
   