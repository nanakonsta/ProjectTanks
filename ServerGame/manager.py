
#half implemented feature
class GameManager:

    def __init__(self, castleRect):
        self.players = []
        self.enemies = []
        self.castle_rect = castleRect
    def removeEnemy(self, reference):
        self.enemies.remove(reference)
    def removePlayer(self, reference):
        self.players.remove(reference)