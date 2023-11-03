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

    # sets player to None
    def set_player_to_None(self):
        self.player = None

    # Sets treasure to None
    def set_treasure_to_None(self):
        self.treasure = None

    # sets the description back to its original form of '.'
    def set_description_to_original(self):
        self.description = '.'

    # sets the description to input string
    def set_description_to_name(self, name: str):
        self.description = name

    # sets player to the current tile when moving around
    def set_player_to_current_tile(self, player: Player):
        self.player = player

    # grabs the player from the current tile to do work on
    def get_player_from_current_tile(self):
        return self.player

    # returns the treasure
    def get_treasure(self):
        return self.treasure

    # Sets the treasure to wanted value
    def set_treasure(self, treasure: Treasure):
        self.treasure = treasure

    # returns description
    def get_description(self):
        return self.description

