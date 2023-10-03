
class Player:
    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score

    def add_score(self, score: int):
            self.score += score
