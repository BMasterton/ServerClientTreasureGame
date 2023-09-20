# constructor for the Treasure object
class Treasure:
    def __init__(self, value, description: str = '$'):
        self.description = description
        self.value = value

    def __str__(self):
        return f'${self.value}'