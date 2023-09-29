from Treasure import Treasure
from Board import Board
from Player import Player
from Tile import Tile
import pytest


def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, description='%')

    assert t1.value == 10
    assert t1.description == '$'
    assert t2.value == 20
    assert t2.description == '%'


def test_Player():
    p1 = Player('bob')
    p2 = Player('tom', 50)

    assert p1.name == 'bob'
    assert p1.score == 0
    assert p2.name =='tom'
    assert p2.score == 50


def test_board():
    with pytest.raises(ValueError, match='n must not be less than 2'):
        b = Board(1,1,5,10,5)
    with pytest.raises(ValueError, match='Number must be above 0 and below n '):
        b = Board(1,5,5,10, -1)
    with pytest.raises(ValueError, match='Must have at least one treasure '):
        b = Board(0, 5, 5, 10,5)
    with pytest.raises(ValueError, match='Max value must be higher than Min value'):
        b = Board(1,5,25,5,3)

    b1 = Board(5, 10, 5, 10, 2)
    p1 = Player('bob')
    p2 = Player('tim')
    b1.add_player(str(p1.name), 9, 9)
    b1.add_player(str(p2.name), 9,7)
    b1.move_player(str(p1.name), 'U')
    assert b1.board[8][9].player is not None
    b1.move_player(str(p1.name), 'D')
    assert b1.board[9][9].player is not None
    b1.move_player(str(p1.name), 'L')
    assert b1.board[9][8].player is not None
    b1.move_player(str(p1.name), 'R')
    assert b1.board[9][9].player is not None
    b1.move_player(str(p2.name), 'R')
    with pytest.raises(Exception, match='Tile already occupied by player'):
        b1.move_player(str(p2.name), 'R') #not sure why not working

    #directly add a treasure and collect it, should have a value apepar

    #check the edges ad their errors

    #check the tile class


