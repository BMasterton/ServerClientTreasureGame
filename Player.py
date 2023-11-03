
class Player:
    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score

    # allows score to be changes and added
    def add_score(self, score: int):
        self.score += score

    # returns the players score
    def get_score(self):
        return self.score
    