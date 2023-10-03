
from Board import Board
from Treasure import Treasure
from Tile import Tile

#loops through the entire 2D array Matrix and will print out each index point
def display(myBoard: Board):
    for row in myBoard.board:
        for tile in row:
            print(tile, end = " " )
        print('\n')
