from Treasure import Treasure
from Tile import Tile


class Board:
    def __init__(self, t, n, min_val, max_val):
        self.t = t
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        self.board = [[Tile() for _ in range(n)]for _ in range(n)]




