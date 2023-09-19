from View import View
from Board import Board

# we need to create a board and pass it on to view, as board creates the tile
# matrix with the randomly placed treasures and then view will iterate through it
# and display them

newBoard = Board(5, 10, )
display(newBoard)

