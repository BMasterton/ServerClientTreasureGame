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
        self.treasureCount = t
        self.score = 0
        if n < 2:
            raise ValueError('n must not be less than 2')
        if max_players <= 0 or max_players > n:
            raise ValueError('Number must be above 0 and below n ')
        else:
            self.max_players = max_players
        if t < 1:
            raise ValueError('Must have at least one treasure ')
        if max_val < min_val:
            raise ValueError('Max value must be higher than Min value')


        # this code below is to create 5 treasures, each treasure will be given
        # a random x and y variable for a spot in the 100 and then we take the board
        # object we created and add treasure to that coordinate by assigning it a treasure value
        for x in range(t):
            randNumX = random.randrange(0, self.n)
            randNumY = random.randrange(0, self.n)
            treasureValue = random.randrange(5, 10)
            while self.board[randNumX][randNumY].treasure: # if the space is already a treasure, find another spot
                randNumX = random.randrange(0, self.n)
                randNumY = random.randrange(0, self.n)
            self.board[randNumX][randNumY].treasure = Treasure(treasureValue)
    # as an example bob would be the key and the values would be the x and y coords
    players = {
        "name": None,
    }
    # adds / creates a player object to the board at a random coord, and sets the dictionary that 
    # holds name and coord info 
    def add_player(self, name, xCord, yCord):
       self.board[xCord][yCord].add_player(Player(name, 0))
       self.players[name] = [xCord, yCord]

    # move the player and check what is in the place they are moving, sets a bunch of values based on 
    # if the tile is a player or treasure 
    def move_player(self, name, direction):
        # this is the name of the player the key of the dict, based on the coords value
        name = list(self.players.keys())[list(self.players.values()).index(self.players[name])]

        try:
            match direction:
                case 'u' | 'U':
                    #grab initial player location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    #new location value based on direction picked
                    newXLocation = initialXLocation -1
                    #checking if the user is out of bounds or if the spot is occupied by a player
                    if initialXLocation == 0 :
                        raise ValueError('Cant go out of bounds')
                    elif self.board[newXLocation][initialYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][0] = newXLocation
                    # change new tile location to the correct name description
                    self.board[newXLocation][initialYLocation].description = name
                    # set the old tile desc to the original '.'
                    self.board[initialXLocation][initialYLocation].description = '.'
                    # moving the player object to the new tile from the old one 
                    self.board[newXLocation][initialYLocation].player = self.board[initialXLocation][initialYLocation].player
                    # if there is a treasure in the tile they want to go too, give the player points, remove treasure
                    # print what they got, and decrement the treasure counter 
                    if self.board[newXLocation][initialYLocation].treasure is not None:
                        # ------------------------------------------TESTING THIS -------------------------------------
                        self.board[newXLocation][initialYLocation].player.add_score(int(self.board[newXLocation][initialYLocation].treasure.value))

                        # self.board[newXLocation][initialYLocation].player.score += int(self.board[newXLocation][initialYLocation].treasure.value)
                        print("Player ", name, " collected ", int(self.board[newXLocation][initialYLocation].treasure.value), "points")
                        self.treasureCount -=1
                        self.board[newXLocation][initialYLocation].treasure = None
                    # remove the player object from the initial location before move 
                    self.board[initialXLocation][initialYLocation].player = None
                    #Check so that if there are no treasures left we look through all the tiles to find the locations of the 
                    #players and print out their totals, then ends program
                    if self.treasureCount == 0:
                        for row in self.board:
                            for tile in row:
                                if tile.player is not None:
                                    print("Player ", tile, " collected a total of: ", tile.player.score, " points")
                        exit(0)
                            
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'd' | 'D':
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newXLocation = initialXLocation +1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialXLocation == 9 :
                        raise ValueError('Cant go out of bounds')
                    elif self.board[newXLocation][initialYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][0] = newXLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[newXLocation][initialYLocation].description = name
                    self.board[newXLocation][initialYLocation].player = self.board[initialXLocation][initialYLocation].player
                    if self.board[newXLocation][initialYLocation].treasure is not None:
                        # ------------------------------------------TESTING THIS -------------------------------------
                        self.board[newXLocation][initialYLocation].player.add_score(int(self.board[newXLocation][initialYLocation].treasure.value))
                        print("Player ", name, " collected ", int(self.board[newXLocation][initialYLocation].treasure.value))
                        self.treasureCount -=1
                        self.board[newXLocation][initialYLocation].treasure = None
                    self.board[initialXLocation][initialYLocation].player = None
                    if self.treasureCount == 0:
                        for row in self.board:
                            for tile in row:
                                if tile.player is not None:
                                    print("Player ", tile, " collected a total of: ", tile.player.score, " points")
                        exit(0)
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'l' | 'L':
                    # current location of the active players x and y location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation -1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialYLocation == 0 :
                        raise ValueError('Cant go out of bounds')
                    elif self.board[initialXLocation][newYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][1] = newYLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[initialXLocation][newYLocation].description = name
                    self.board[initialXLocation][newYLocation].player = self.board[initialXLocation][initialYLocation].player
                    if self.board[initialXLocation][newYLocation].treasure is not None:
                        # ------------------------------------------TESTING THIS -------------------------------------
                        self.board[initialXLocation][newYLocation].player.add_score(int(self.board[initialXLocation][newYLocation].treasure.value))
                        print("Player ", name, " collected ", int(self.board[initialXLocation][newYLocation].treasure.value))
                        self.treasureCount -=1
                        self.board[initialXLocation][newYLocation].treasure = None
                    self.board[initialXLocation][initialYLocation].player = None
                    if self.treasureCount == 0:
                        for row in self.board:
                            for tile in row:
                                if tile.player is not None:
                                    print("Player ", tile, " collected a total of: ", tile.player.score, " points")
                        exit(0)
                    # since the player has gone over the old spot it can only be a '.' so we can change it back
                case 'r' | 'R':
                    # current location of the active players x and y location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation + 1
                    #checking if the user is out of bounds or if the spot is occupies by anything else
                    if initialYLocation == 9 :
                        raise ValueError('Cant go out of bounds')
                    elif self.board[initialXLocation][newYLocation].player is not None:
                        raise Exception('Tile already occupied by player')
                    # new player location based on up command
                    #setting the dictionaries value to the new changed location value
                    self.players[name][1] = newYLocation
                    #change the location of the player icon, by changing the . to a player name icon
                    self.board[initialXLocation][initialYLocation].description = '.'
                    self.board[initialXLocation][newYLocation].description = name
                    self.board[initialXLocation][newYLocation].player = self.board[initialXLocation][initialYLocation].player
                    if self.board[initialXLocation][newYLocation].treasure is not None:
                        # ------------------------------------------TESTING THIS -------------------------------------
                        self.board[initialXLocation][newYLocation].player.add_score(int(self.board[initialXLocation][newYLocation].treasure.value))
                        print("Player ", name, " collected ", int(self.board[initialXLocation][newYLocation].treasure.value))
                        self.treasureCount -=1
                        self.board[initialXLocation][newYLocation].treasure = None
                    self.board[initialXLocation][initialYLocation].player = None
                    if self.treasureCount == 0:
                        for row in self.board:
                            for tile in row:
                                if tile.player is not None:
                                    print("Player ", tile, " collected a total of: ", tile.player.score, " points")
                        exit(0)
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










