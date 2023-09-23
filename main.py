from View import display
from Board import Board
import random

newBoard = Board(5, 10, 5, 10, 2) # creating the new boar
randPlayerXPos = random.randrange(0, 10) # creating initial random x and y coords
randPlayerYPos = random.randrange(0, 10)
playerNames = ["1", "2"] # list of players that will be added

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


#
for i in range(5):
    display(newBoard)
    # need error checking for this one
    playerInputDirection = input("(U)p (D)own (L)eft (R)ight (Q)uit \n")
    playerInputPlayer = str(input("Player 1 or 2 \n"))
    #match may be better here
    if playerInputPlayer == '1':
        newBoard.move_player(playerNames[0], playerInputDirection)
    else:
        newBoard.move_player(playerNames[1], playerInputDirection)




