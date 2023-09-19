
from Board import Board
from Treasure import Treasure
from Tile import Tile

def display(myBoard: Board):
    for row in myBoard.board:
        for tile in row:
            print(tile)
