from View import display
from Board import Board
import random

newBoard = Board(1, 10, 5, 10, 2) # creating the new boar
randPlayerXPos = random.randrange(0, 10) # creating initial random x and y coords
randPlayerYPos = random.randrange(0, 10)
playerNames = ["1", "2"] # list of players that will be added
playerDirections = ['U' , 'D' , 'L' , 'R' , 'Q']

# goes over all the players in playerNames and looks at a random  x and y pos so it can add them, if that position is
# not a "." then it will try again until it can, if the spot is taken it will let the player know
for player in playerNames:
    randPlayerXPos = random.randrange(0, 10)
    randPlayerYPos = random.randrange(0, 10)
    # making sure that if the tile already has a player or a treaure, another player cant spawn on them
    while newBoard.board[randPlayerXPos][randPlayerYPos].treasure is not None:
        if newBoard.board[randPlayerXPos][randPlayerYPos].player is not None:
            randPlayerXPos = random.randrange(0, 10)
            randPlayerYPos = random.randrange(0, 10)
            raise ValueError("space already occupied")
    newBoard.add_player(player, randPlayerXPos, randPlayerYPos)

while True:
    try:
        display(newBoard)
        # get value from user and make sure its an allowed input if not tell them and repeat until proper input
        playerInputDirection = input("(U)p (D)own (L)eft (R)ight (Q)uit \n")
        if playerInputDirection.upper() not in playerDirections:
            raise Exception('Must give a valid direction or quit')
        # get player name input from user and depending on the player send that info to moveplayer 
        playerInputPlayer = str(input("Player 1 or 2 \n"))
        if playerInputPlayer not in playerNames:
            raise Exception('value must be 1 or 2')
        if playerInputPlayer == '1':
            newBoard.move_player(playerNames[0], playerInputDirection)
        elif playerInputPlayer == '2':
            newBoard.move_player(playerNames[1], playerInputDirection)
    except Exception as details:
        print(str(details))



