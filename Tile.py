from Treasure import Treasure
from Player import Player

# construtor for the Tile object
class Tile:
    def __init__(self, treasure: Treasure = None, description: str = '.', player: Player = None):
        self.treasure = treasure
        self.description = description
        self.player = player

    def __str__(self):
            if self.treasure:
                return self.treasure.description
            elif self.player:
                return self.player.name
            else:
                return self.description

    def add_player(self, player: Player):
        self.player = player



# string emthod where if treasure isnt None then you return the Treasure.description which isa $

