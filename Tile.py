from Treasure import Treasure


class Tile:
    def __init__(self, treasure: Treasure = None, description: str = '.'):
        self.treasure = treasure
        self.description = description

    def __str__(self):
        if self.treasure:
            return self.treasure.description
        else:
            return self.description
