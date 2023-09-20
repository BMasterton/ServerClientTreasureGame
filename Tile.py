from Treasure import Treasure

# construtor for the Tile object
class Tile:
    def __init__(self, treasure: Treasure = None, description: str = '.'):
        self.treasure = treasure
        self.description = description
# string emthod where if treasure isnt None then you return the Treasure.description which isa $
    def __str__(self):
        if self.treasure:
            return self.treasure.description
        else:
            return self.description
