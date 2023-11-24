from django.db import models
from django.core.exceptions import ValidationError


def validate_col_range(value):
    if value < 1 or value > 10:
        raise ValidationError('Column out of range', code='col_value')


def validate_row_range(value):
    if value < 1 or value > 10:
        raise ValidationError('Row out of range', code='row_value')

#could be wrong
def validate_unique_name(value):
    players = Player.objects.filter(name=value)
    if len(players) != 0:
        raise ValidationError('Name already taken', code="duplicate")

#could be wrong
def validate_cell_name(value):
    cell = Board.objects.filter(label=value)
    if cell not in ['.', '$', '1', '2']:
        raise ValidationError('Cell label incorrect', code='incorrect_cell_value')

#could be wrong
def validate_value_amount(value):
    value = Board.objects.filter(value=value)
    if value < 1 or value > 10:
        raise ValidationError('Value has been set incorrectly', code='incorrect_cell_value')


# a player object, contains a name, row, col, and score, row and col are used as matrix location points
class Player(models.Model):
    # name = models.CharField(max_length=20, validators=[validate_unique_name])
    name = models.CharField(max_length=20)
    row = models.IntegerField(default=0, validators=[validate_row_range])
    col = models.IntegerField(default=0, validators=[validate_col_range])
    score = models.IntegerField(default=0)

    # def clean(self):
    #     prev = Player.objects.filter(pk=self.pk)
    #     if len(prev) > 0:
    #         if abs((int(self.row) - int(prev[0].row))> 1 ):
    #             raise ValidationError('Row too far', code='row_distance')
    #     if abs(int(self.col) - int(prev[0].col)) > 1:
    #         raise ValidationError('Column too far', code='col_distance')

    def __str__(self):
        return f'{self.name} @ ({self.row}, {self.col}, {self.score})'


# A board location that can be seen as a cell, each cell in the matrix will hold nothing or a value, if it has
# a value then there is a treasure there
class Board(models.Model):
    label = models.CharField(max_length=20, validators=[validate_cell_name])
    #label = models.CharField(max_length=20, default='.')
    row = models.IntegerField(default=10, validators=[validate_row_range])
    col = models.IntegerField(default=10, validators=[validate_col_range])
    value = models.IntegerField(default=0, validators=[validate_value_amount])
    # value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.label} @ ({self.row}, {self.col}, {self.value})'