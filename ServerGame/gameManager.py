from player import Player
from difficultyEnum import Difficulty
class GameManager:
    def __init__(self):
        self._player1 = Player()
        self._player2 = Player()
        self._difficulty = None
        self.castleHealth = 0
        self.enemiesHealth = 0
        self.enemiesFireRate = 0
        self.players = []
        self.enemies = []
        self.castle_rect = None
    @property
    def player1(self):
        return self._player1

    @property
    def player2(self):
        return self._player2
    
    @property
    def difficulty(self):
        match self._difficulty:
            case Difficulty.EASY:
                return "easy"
            case Difficulty.MEDIUM:
                return "medium"
            case Difficulty.HARD:
                return "hard"
        return "not yet Selected"
    
    @player1.setter
    def player1(self, value):
        self._player1 = value    
        
    
    @player2.setter
    def player2(self, value):
        self._player2 = value    
        
    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value
        match self._difficulty:
            case Difficulty.EASY:
                self.castleHealth = 1500
                self.player1.health = 300
                self.player2.health = 300
                self.enemiesHealth = 100
                self.player1.fireRate = 200
                self.player2.fireRate = 200
                self.enemiesFireRate = 1500
            case Difficulty.MEDIUM:
                self.castleHealth = 1000
                self.player1.health = 200
                self.player2.health = 200
                self.enemiesHealth = 150
                self.player1.fireRate = 300
                self.player2.fireRate = 300
                self.enemiesFireRate = 1000
            case Difficulty.HARD:
                self.castleHealth = 500
                self.player1.health = 100
                self.player2.health = 100
                self.enemiesHealth = 200
                self.player1.fireRate = 400
                self.player2.fireRate = 400
                self.enemiesFireRate = 1000
        
    def removeEnemy(self, reference):
        self.enemies.remove(reference)
    def removePlayer(self, reference):
        self.players.remove(reference)