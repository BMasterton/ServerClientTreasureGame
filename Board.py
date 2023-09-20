from Treasure import Treasure
from Tile import Tile
import random


class Board:
    def __init__(self, t, n, min_val, max_val):
        self.t = t
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        self.board = [[Tile() for _ in range(n)] for _ in range(n)]
        for x in range(5):
            randNumX = random.randrange(0,10)
            randNumY = random.randrange(0, 10)
            self.board[randNumX][randNumY].treasure = Treasure(5)
#         need to somehow add bloody Treasure to random spots in the board i think after its been created






