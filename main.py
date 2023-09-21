from View import display
from Board import Board
import random

newBoard = Board(5, 10, 5, 10, 2) # creating the new board
randPlayerXPos = random.randrange(0, 10) # creating initial random x and y coords
randPlayerYPos = random.randrange(0, 10)
playerNames = ["tom", "bob"] # list of players that will be added

# goes over all the players in playerNames and looks at a random  x and y pos so it can add them, if that position is
# not a "." then it will try again until it can, if the spot is taken it will let the player know
for player in playerNames:
    randPlayerXPos = random.randrange(0, 10)
    randPlayerYPos = random.randrange(0, 10)
    while newBoard.board[randPlayerXPos][randPlayerYPos].description != ".":
        randPlayerXPos = random.randrange(0, 10)
        randPlayerYPos = random.randrange(0, 10)
        raise ValueError("space already occupied")
    newBoard.add_player(player, randPlayerXPos, randPlayerYPos)


display(newBoard)
