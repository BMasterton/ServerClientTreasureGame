from Treasure import Treasure
from Tile import Tile
from Player import Player
import random
import os


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
            while self.board[randNumX][randNumY].get_treasure() is not None or self.board[randNumX][randNumY].get_player_from_current_tile() is not None: # if the space is already a treasure, find another spot
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

    def treasureCheck(self):
        if self.treasureCount < 0:
            for row in self.board:
                for tile in row:
                    if tile.get_player_from_current_tile() is not None:
                        print("Player ", tile, " collected a total of: ", tile.player.score, " points")
            exit(0)

    def printScore(self):
        for row in self.board:
            for tile in row:
                if tile.get_player_from_current_tile() is not None:
                    print("Player ", tile, " collected a total of: ", tile.player.score, " points")

    def printPlayerScore(self, name):
        for row in self.board:
            for tile in row:
                if tile.get_player_from_current_tile() is not None and tile.get_player_from_current_tile().name == name:
                    return tile.get_player_from_current_tile().get_score()

    def boardString(self):
        boardView = ""
        for row in self.board:
            index = 0
            for tile in row:
                if tile.get_player_from_current_tile() is not None:
                    if index != 9:
                        boardView += tile.get_player_from_current_tile().name + ' '
                        index += 1
                    else:
                        boardView += tile.get_player_from_current_tile().name
                elif tile.get_treasure() is not None:
                    if index != 9:
                        boardView += tile.get_treasure().description + ' '
                        index += 1
                    else:
                        boardView  += tile.get_treasure().description
                else:
                    if index != 9:
                        boardView += tile.get_description() + ' '
                        index += 1
                    else:
                        boardView += tile.get_description()
            boardView += '\n'
        return boardView

    #Takes in the new and old board locations, the name, and what direction and changes all values
    def change_tile_values(self, initialx, initialy, changesxory, name, positioning, direction):
        #picking if its up or down direction
        if positioning == 'vertical':
            # up and down have different out of bounds exceptions
            if direction == 'U':
                if initialx == 0 :
                    raise ValueError('Cant go out of bounds')
                elif self.board[changesxory][initialy].get_player_from_current_tile() is not None: # change to another value 
                    raise Exception('Tile already occupied by player')
            elif direction == 'D':
                if initialx == 9 :
                    raise ValueError('Cant go out of bounds')
                elif self.board[changesxory][initialy].get_player_from_current_tile() is not None: # change to another value 
                    raise Exception('Tile already occupied by player')
            self.players[name][0] = changesxory
            # change new tile location to the correct name description
            self.board[changesxory][initialy].set_description_to_name(name)
            # set the old tile desc to the original '.'
            self.board[initialx][initialy].set_description_to_original()
            # moving the player object to the new tile from the old one 
            self.board[changesxory][initialy].set_player_to_current_tile(self.board[initialx][initialy].get_player_from_current_tile())
            # if there is a treasure in the tile they want to go too, give the player points, remove treasure
            # print what they got, and decrement the treasure counter 
            if self.board[changesxory][initialy].get_treasure() is not None:
                self.board[changesxory][initialy].player.add_score(int(self.board[changesxory][initialy].treasure.get_treasure_value()))
                print("Player ", name, " collected ", int(self.board[changesxory][initialy].treasure.get_treasure_value()), "points")
                self.board[changesxory][initialy].set_treasure_to_None()
                self.treasureCount -=1
            # remove the player object from the initial location before move
            self.board[initialx][initialy].set_player_to_None()
        # picking a left and right direction
        elif positioning == 'horizontal':
            if direction == 'L':
                if initialy == 0 :
                    raise ValueError('Cant go out of bounds')
                elif self.board[initialx][changesxory].get_player_from_current_tile() is not None:
                    raise Exception('Tile already occupied by player')
            elif direction == 'R':
                if initialy == 9 :
                    raise ValueError('Cant go out of bounds')
                elif self.board[initialx][changesxory].get_player_from_current_tile() is not None:
                    raise Exception('Tile already occupied by player')
            self.players[name][1] = changesxory
            #change the location of the player icon, by changing the . to a player name icon
            self.board[initialx][initialy].set_description_to_original()
            self.board[initialx][changesxory].set_description_to_name(name) 
            self.board[initialx][changesxory].set_player_to_current_tile(self.board[initialx][initialy].player)
            if self.board[initialx][changesxory].get_treasure() is not None:
                self.board[initialx][changesxory].player.add_score(int(self.board[initialx][changesxory].treasure.get_treasure_value()))
                print("Player ", name, " collected ", int(self.board[initialx][changesxory].treasure.get_treasure_value()))
                self.board[initialx][changesxory].set_treasure_to_None()
                self.treasureCount -=1
            self.board[initialx][initialy].set_player_to_None()
            
            
    # move the player and check what is in the place they are moving, sets a bunch of values based on 
    # if the tile is a player or treasure 
    def move_player(self, name, direction):
        # this is the name of the player the key of the dict, based on the coords value
        name = list(self.players.keys())[list(self.players.values()).index(self.players[name])]

        try:
            match direction:
                case 'u' | 'U':
                    positioning = 'vertical'
                    direction = 'U'
                    #grab initial player location
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    #new location value based on direction picked
                    newXLocation = initialXLocation -1
                    self.change_tile_values(initialXLocation, initialYLocation, newXLocation, name, positioning, direction) 
                    self.treasureCheck()
                case 'd' | 'D':
                    positioning = 'vertical'
                    direction ='D'
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newXLocation = initialXLocation +1
                    self.change_tile_values(initialXLocation, initialYLocation, newXLocation, name, positioning, direction)
                    self.treasureCheck()
                case 'l' | 'L':
                    positioning = 'horizontal'
                    direction = 'L'
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation -1
                    self.change_tile_values(initialXLocation,initialYLocation, newYLocation, name, positioning, direction)
                    self.treasureCheck()
                case 'r' | 'R':
                    positioning = 'horizontal'
                    direction = 'R'
                    initialXLocation = self.players[name][0]
                    initialYLocation = self.players[name][1]
                    newYLocation = initialYLocation + 1
                    self.change_tile_values(initialXLocation,initialYLocation, newYLocation, name, positioning, direction)
                    self.treasureCheck()
                case 'q' | 'Q':
                    self.printScore()
                    exit()
                case _:
                    print()
        except ValueError as details:
            print(str(details))
        except Exception as details:
            print(str(details))
        return 0










