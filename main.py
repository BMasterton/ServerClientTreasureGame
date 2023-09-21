from View import display
from Board import Board
import random

newBoard = Board(5, 10, 5, 10, 2)
randPlayerXPos = random.randrange(0, 10)
randPlayerYPos = random.randrange(0, 10)


while newBoard.board[random.randrange(0, 10)][random.randrange(0, 10)].description != ".":
    randPlayerXPos = random.randrange(0, 10)
    randPlayerYPos = random.randrange(0, 10)
newBoard.add_player("tom", random.randrange(0, 10), random.randrange(0, 10))
newBoard.add_player("Bob", random.randrange(0, 10),random.randrange(0, 10) )

display(newBoard)
