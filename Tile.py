from Treasure import Treasure
from Player import Player

# construtor for the Tile object
class Tile:
    def __init__(self, treasure: Treasure = None, description: str = '.', player: Player = None):
        self.treasure = treasure
        self.description = description
        self.player = player

    def __str__(self):
        # basically if treasures doesnt equal non, then send treasure info, if player doesnt equal none 
        # send player name, other wise always print out '.'
            if self.treasure:
                return self.treasure.description
            elif self.player:
                return self.player.name
            else:
                return self.description

    #takes in a player and sets that player to the tile object 
    def add_player(self, player: Player):
        self.player = player

    def set_player_to_None(self):
        self.player = None
        
    def set_treasure_to_none(self):
        self.treasure = None
        
    def set_description_to_original(self):
        self.description = '.'
        
    def set_description_to_name(self, name: str):
        self.description = name
        
    def set_player_to_current_tile(self, player: Player):
        self.player = player

# string emthod where if treasure isnt None then you return the Treasure.description which isa $

