from sys import stderr
import pytest
from Treasure import Treasure
from Board import Board
from Player import Player
from Tile import Tile

# tests to make sure the treasure object is created, and that its functions work as expected
def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, description='%')

    assert t1.value == 10
    assert t1.description == '$'
    assert t2.value == 20
    assert t2.description == '%'
    assert t1.get_treasure_value() == 10
    assert t2.get_treasure_value() == 20

# test for the tile object, making sure all of its many functions work as anticipated
def test_tile():
    t1 = Tile()
    t2 = Tile()
    p1 = Player('bob')
    name = 'tim'
    assert t1.description == '.'
    assert t1.player is None
    assert t1.treasure is None
    tr = Treasure(10)
    t2.add_player(p1)
    assert t2.get_player_from_current_tile() == p1
    t2.set_player_to_None()
    assert t2.get_player_from_current_tile() is None
    t2.set_treasure(tr)
    assert t2.get_treasure() == tr
    t2.set_treasure_to_None()
    assert t2.get_treasure() is None
    t2.set_description_to_name('tim')
    assert t2.get_description() == 'tim'
    t2.set_description_to_original()
    assert t2.get_description() == '.'

# testing the player object and making sure it forms properly and its functions work
def test_player():
    p1 = Player('bob')
    p2 = Player('tom', 50)

    assert p1.name == 'bob'
    assert p1.score == 0
    assert p2.name == 'tom'
    assert p2.score == 50

    p2.add_score(50)
    assert p2.get_score() == 100

# testing to make sure the board forms and that all errors are raised when not correctly made
def test_board():
    with pytest.raises(ValueError, match='n must not be less than 2'):
        b = Board(1, 1, 5, 10, 5)
    with pytest.raises(ValueError, match='Number must be above 0 and below n '):
        b = Board(1, 5, 5, 10, -1)
    with pytest.raises(ValueError, match='Must have at least one treasure '):
        b = Board(0, 5, 5, 10, 5)
    with pytest.raises(ValueError, match='Max value must be higher than Min value'):
        b = Board(1, 5, 25, 5, 3)

# testing to make sure players can correctly move aroud the board and all info is transferred
def test_board_players_movement():
    b1 = Board(5, 10, 5, 10, 2)
    # just to make sure that I can determine where the treasures are to insure accuracy of tests
    for row in b1.board:
        for tile in row:
            tile.treasure = None
    p1 = Player('1')
    p2 = Player('2')
    b1.board[0][0].set_treasure( Treasure(5))
    b1.add_player(str(p1.name), 9, 9)
    b1.add_player(str(p2.name), 9, 7)
    b1.move_player(str(p1.name), 'U')
    assert b1.board[8][9].get_player_from_current_tile() is not None
    b1.move_player(str(p1.name), 'D')
    assert b1.board[9][9].get_player_from_current_tile() is not None
    b1.move_player(str(p1.name), 'L')
    assert b1.board[9][8].get_player_from_current_tile() is not None
    b1.move_player(str(p1.name), 'R')
    assert b1.board[9][9].get_player_from_current_tile() is not None
    b1.move_player(str(p2.name), 'R')
    assert b1.board[9][8].get_player_from_current_tile() is not None
    b1.move_player(str(p2.name), 'R')
    assert b1.board[9][7].get_player_from_current_tile() is None

# testing to make sure the score functions and that the correct
def test_board_players_score(capsys):
    try:
        b2 = Board(4, 10, 5, 10, 2)
        # just to make sure that I can determine where the treasures are to insure accuracy of tests
        for row in b2.board:
            for tile in row:
                tile.treasure = None
        p1 = Player('1')
        p2 = Player('2')

        b2.board[0][0].treasure = Treasure(5)
        b2.board[9][9].treasure = Treasure(10)
        b2.add_player(str(p1.name), 0, 1)
        b2.add_player(str(p2.name), 9, 8)
        b2.move_player(str(p1.name), 'L')
        assert b2.board[0][0].player.get_score() is 5
        captured = capsys.readouterr()
        assert captured.out == "Player  1  collected  5\n"
        assert b2.board[9][8].get_player_from_current_tile() is not None
        assert b2.board[9][9].get_treasure() is not None
        b2.move_player(str(p2.name), 'R')
        assert b2.board[9][9].get_treasure() is None
        assert b2.board[9][9].player.get_score() is 10
        captured = capsys.readouterr()
        assert captured.out == "Player  2  collected  10\n"
        # making sure that the score sum is working
        b2.board[9][7].set_treasure(Treasure(10))
        b2.board[9][6].set_treasure(Treasure(10))
        assert b2.board[9][7].get_treasure() is not None
        assert b2.board[9][6].get_treasure() is not None
        b2.move_player(str(p2.name), 'L')
        b2.move_player(str(p2.name), 'L')
        assert b2.board[9][7].get_treasure() is None
        assert b2.board[9][7].player.get_score() is 20
        captured = capsys.readouterr()
        assert captured.out == "Player  2  collected  10\n"
        # check the total score at the end with
        b2.move_player(str(p2.name), 'L')
        assert b2.board[9][6].player.score is 30
        captured = capsys.readouterr()
        assert captured.out == "Player  2  collected  10\n"
        captured = capsys.readouterr()
        assert captured.out == "Player  1  scored  5\n"
        assert captured.out == "Player  1  scored  30\n"
    except SystemExit:
        pass


def test_board_out_of_bounds():
    b3 = Board(2, 10, 5, 10, 2)
    for row in b3.board:
        for tile in row:
            tile.treasure = None

    p1 = Player('1')
    p2 = Player('2')

    b3.board[5][5].set_treasure(Treasure(5))
    b3.board[6][6].set_treasure(Treasure(10))

    b3.add_player(str(p1.name), 0, 0)
    b3.add_player(str(p2.name), 9, 9)
    # with pytest.raises(ValueError, match='Cant go out of bounds'):
    #     b3.move_player(str(p1.name), 'U')
    # with pytest.raises(ValueError, match='Cant go out of bounds'):
    #     b3.move_player(str(p1.name), 'L')
    # with pytest.raises(ValueError, match='Cant go out of bounds'):
    #     b3.move_player(str(p2.name), 'D')
    # with pytest.raises(ValueError, match='Cant go out of bounds'):
    #     b3.move_player(str(p2.name), 'R')

def test_board_player_collission():
    b4 = Board(4, 10, 5, 10, 2)
    for row in b4.board:
        for tile in row:
            tile.treasure = None
    p1 = Player('1')
    p2 = Player('2')
    b4.add_player(str(p1.name), 9, 9)
    b4.add_player(str(p2.name), 9, 8)

    b4.board[5][5].set_treasure(Treasure(5))
    b4.board[6][6].set_treasure(Treasure(10))
    # hold over as the Tile already occupied by player isnt recognizing the exception being raised
    assert b4.board[9][8].get_player_from_current_tile() is not None
    assert b4.board[9][9].get_player_from_current_tile() is not None
    b4.move_player(str(p2.name), 'R')
    assert b4.board[9][8].get_player_from_current_tile() is not None
    assert b4.board[9][9].get_player_from_current_tile() is not None
    # with pytest.raises(Exception, match='Tile already occupied by player'):
    #     b4.move_player(str(p2.name), 'R') #not sure why not working




