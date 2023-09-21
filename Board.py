from Treasure import Treasure
from Tile import Tile
from Player import Player

import random

# constructor for the board object
class Board:
    def __init__(self, t, n, min_val, max_val, max_players):
        self.t = t
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        self.board = [[Tile() for _ in range(n)] for _ in range(n)]
        if max_players < 0 or max_players > n:
            raise ValueError('Number must be above 0 and below n ')
        else:
            self.max_players = max_players
        # this code below is to create 5 treasures, each treasure will be given
        # a random x and y variable for a spot in the 100 and then we take the board
        # object we created and add treasure to that coordinate by assigning it a treasure value
        for x in range(5):
            randNumX = random.randrange(0, 10)
            randNumY = random.randrange(0, 10)
            treasureValue = random.randrange(5, 10)
            while self.board[randNumX][randNumY].treasure: # if the space is already a treasure, find another spot
                randNumX = random.randrange(0, 10)
                randNumY = random.randrange(0, 10)
            self.board[randNumX][randNumY].treasure = Treasure(treasureValue)

    def add_player(self, name, xCord, yCord):
       self.board[xCord][yCord].add_player(Player(name))








