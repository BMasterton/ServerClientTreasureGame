from django.db import models

# a player object, contains a name, row, col, and score, row and col are used as matrix location points
class Player(models.Model):
    name = models.CharField(max_length=20)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} @ ({self.row}, {self.col}, {self.score})'


# A board location that can be seen as a cell, each cell in the matrix will hold nothing or a value, if it has
# a value then there is a treasure there
class Board(models.Model):
    label = models.CharField(max_length=20, default='.')
    row = models.IntegerField(default=10)
    col = models.IntegerField(default=10)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.label} @ ({self.row}, {self.col}, {self.value})'