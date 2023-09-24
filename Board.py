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
       self.board[xCord][yCord].add_player(Player(name, 0))
       self.players[name] = [xCord, yCord]
    #    print(self.players[name])
       name = list(self.players.keys())[list(self.players.values()).index(self.players[name])]
    #    print(name)
    #    currLocation = self.players[name][0]
    #    print(currLocation)


       #put this made player and coords into its own dictionary

    def move_player(self, name, direction):
        # need to check the location of the current player by name via the dictironary
        # this is the x and y coord of a player the value of the key value players dict

        # print(list(self.players.keys())[list(self.players.values()).index(self.players[name])])
        # this is the name of the player the key of the dict, based on the coords value
        name = list(self.players.keys())[list(self.players.values()).index(self.players[name])]
        # print(name)

        try:
            match direction:
                case 'u' | 'U':
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newXLocation = initialXLocation -1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialXLocation == 0 :
                        raise ValueError('Cant go out out bounds')
                    elif self.board[newXLocation][initialYLocation].player is not None:
                        raise Exception('Token already taken')
                    elif self.board[newXLocation][initialYLocation].treasure is not None:
                        self.board[newXLocation][initialYLocation].player.score += self.board[newXLocation][initialYLocation].treasure.value
                        self.board[newXLocation][initialYLocation].treasure = None
                        print(self.board[newXLocation][initialYLocation].player.score)
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][0] = newXLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    print( self.board[initialXLocation][initialYLocation].player.name)
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[newXLocation][initialYLocation].description = name
                    self.board[newXLocation][initialYLocation].player = self.board[initialXLocation][initialYLocation].player
                    self.board[initialXLocation][initialYLocation].player = None
                    print( self.board[newXLocation][initialYLocation].player.name)
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'd' | 'D':
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newXLocation = initialXLocation +1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialXLocation == 9 :
                        raise ValueError('Cant go out out bounds')
                    elif self.board[newXLocation][initialYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][0] = newXLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    print( self.board[initialXLocation][initialYLocation].player.name)
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[newXLocation][initialYLocation].description = name
                    self.board[newXLocation][initialYLocation].player = self.board[initialXLocation][initialYLocation].player
                    self.board[initialXLocation][initialYLocation].player = None
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'l' | 'L':
                    # current location of the active players x and y location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation -1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialYLocation == 0 :
                        raise ValueError('Cant go out out bounds')
                    elif self.board[initialXLocation][newYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][1] = newYLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    print( self.board[initialXLocation][initialYLocation].player.name)
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[initialXLocation][newYLocation].description = name
                    self.board[initialXLocation][newYLocation].player = self.board[initialXLocation][initialYLocation].player
                    self.board[initialXLocation][initialYLocation].player = None
                    print(self.board[initialXLocation][newYLocation].player.name)
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'r' | 'R':
                    # current location of the active players x and y location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation + 1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialYLocation == 9 :
                        raise ValueError('Cant go out out bounds')
                    elif self.board[initialXLocation][newYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][1] = newYLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    print( self.board[initialXLocation][initialYLocation].player.name)
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[initialXLocation][newYLocation].description = name
                    self.board[initialXLocation][newYLocation].player = self.board[initialXLocation][initialYLocation].player
                    self.board[initialXLocation][initialYLocation].player = None
                    print(self.board[initialXLocation][newYLocation].player)
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'q' | 'Q':
                    exit()
                case _:
                    print()
        except ValueError as details:
            print(str(details))
        except Exception as details:
            print(str(details))
        return 0










