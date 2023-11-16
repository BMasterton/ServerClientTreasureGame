from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=20)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} @ ({self.row}, {self.col}, {self.score})'



class Board(models.Model):
    label = models.CharField(max_length=20, default='.')
    row = models.IntegerField(default=10)
    col = models.IntegerField(default=10)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.label} @ ({self.row}, {self.col}, {self.value})'