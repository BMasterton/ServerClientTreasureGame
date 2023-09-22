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
    # as an example bob would be the key and the values would be the x and y coords
    players = {
        "name": None,
    }

    def add_player(self, name, xCord, yCord):
       self.board[xCord][yCord].add_player(Player(name))
       self.players[name] = xCord, yCord
       print(self.players[name])


        #put this made player and coords into its own dictionary

    def move_player(self, name, direction: char):
        # need to check the location of the current player by name via the dictironary
        # this is the x and y coord of a player the value of the key value players dict
        currLocation = self.players[name]
        print(list(self.players.keys())[list(self.players.values()).index(self.players[name])])
        # this is the name of the player the key of the dict, based on the coords value
        name = list(self.players.keys())[list(self.players.values()).index(self.players[name])]
        print(name)

        try:
            match direction:
                case 'u' | 'P':
                    # move y coord up 1 +=1
                # if the y coord is at the edge so 10 then you cannot go up
                #throw valueError
                case 'd' | 'D':
                    # move y coors down 1 -=1
                # throw valueError
                    # if the y coord is at the edge so 0, then you cannot run that command
                case 'l' | 'L':
                    # move x coords down 1 -= 1
                    # throw valueError
                    # if the x coor is at the edge so 0, then you cannot run the command
                case 'r' | 'R':
                    # move x coords up 1 += 1
                # throw valueError
                    # if the x coord is at the edge so 10, then you cannot run the coomand
                case 'q' | 'Q':
                    # exit the program
                case _:
                    print()
        except valueError as details:
            print(str(details))


        # need to have a if else nightmare with u d l r
        # need to have a check for the sides of the map, if they are
        # larger than 10 on the x and y and less than 1 on the x and y, you need to throw
        # when moving player icon, it has to override the one its going too, and then rewrite the one it came from
        # as a "." again
        # a ValueError saying no, and dont do the move.


        return 0










