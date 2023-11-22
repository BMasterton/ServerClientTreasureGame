from django.test import TestCase
from django.urls import reverse

from .models import Player, Board

from .views import displayPlayer, display, createGame, playerMove


# class InitialTestSuite(TestCase):
#     def test_game_init(self):
#         response = self.client.get('/game/create')
#         response = self.client.post('/game/create')
#         self.assertEquals(5, len(Board.objects.all()))
#         self.assertEquals(2, len(Player.objects.all()))
#
#         for b in Board.objects.all():
#             self.assertTrue(b.value > 0)
#
#         for b in Board.objects.all():
#             self.assertTre(MIN_TREAUSER <= b.value <= MAX_TREASURE)

#
#
class PlayerTestCase(TestCase):
    # def test_players_populated(self):
    #     self.client.post('/game/create/')
    #     self.assertEquals(2, len(Player.objects.all()))
    def test_move_1(self):
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        p1 = Player.objects.get(name='1')
        p1OriginalRow = p1.row
        response = self.client.post(reverse('display_player', args = [1]),
                                    {'player_direction': 'U'})
        self.assertEqual(response.status_code, 200)
        p1.refresh_from_db()
        self.assertEqual(p1.row, (p1OriginalRow -1))

    def test_add_player(self):
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        p1 = Player.objects.get(name='1')
        p1.row = 0
        p1.col = 0
        response = self.client.post(reverse('display_player', args=[1]),
                                    {'player_direction': 'U'})
        self.assertFormError(response, 'form', 'row', 'Row out of range')


    # def test_player_move(self):
    #     self.client.post('/game/create/')
    #     player1 = Player.objects.filter(name='1')
    #     print(player1.row, player1.col)
    #     player1OGRow = player1.row
    #     player1OGCol = player1.col
    #     playerMove('U', 1)
    #
    #     self.assertEquals(player1.row == player1OGRow-1)
#     def test_create(self):
#         self.client.post('/game/player/create', {'name': '1', 'row': 3, 'col': 7, 'score': 0})
#         p = Player.objects.get(name='1')
#         self.assertEquals(p.name, '1')
#         self.assertEquals(p.row, 3)
#         self.assertEquals(p.col, 7)
#         self.assertEquals(p.value, 0)
#
#     def test_out_of_bounds_row(self):
#         response = self.client.post('/game/player/create', {'name': '1', 'row': -8, 'col': 7, 'score': 0})
#         self.assertFormError(response, 'form', 'row', 'Row out of range')
#         try:
#             Player.objects.get(label='1')
#             self.fail()
#         except Player.DoesNotExist:
#             pass
#
#     def test_out_of_bounds_col(self):
#         response = self.client.post('/game/player/create', {'name': '1', 'row': 8, 'col': -7, 'score': 0})
#         self.assertFormError(response, 'form', 'col', 'Column out of range')
#         try:
#             Player.objects.get(label='1')
#             self.fail()
#         except Player.DoesNotExist:
#             pass

# # no idea if this will work
#     def test_unique_name(self):
#         pass

    # test for unqiue name, score in range forboard, board creation, board bounds, player label, palyer score
    # board cell name, are there 2 players, are there 5 treasures

# class BoardTestCase(TestCase):
#     def test_board_populates(self):
#         self.client.post('/game/create/')
#         print(Board.objects.all())
#         self.assertEquals(5, len(Board.objects.all()))
#
#         for b in Board.objects.all():
#             self.assertTrue(b.value > 0)

    # def test_create_blank(self):
    #     self.client.post('/game/create', {'label': '', 'row': 1, 'col': 2, 'score': 0})
    #     b = Board.objects.get(label='')
    #     self.assertEquals(b.label, '.')
    #     self.assertEquals(b.row, 1)
    #     self.assertEquals(b.col, 2)
    #     self.assertEquals(b.score, 0)

# # no idea if this will work
#     def test_create_treasure(self):
#         self.client.post('/game/create', {'label': '$', 'row': 2, 'col': 3, 'score': 5})
#         b = Board.objects.get(label='$')
#         self.assertEquals(b.label, '$')
#         self.assertEquals(b.row, 2)
#         self.assertEquals(b.col, 3)
#         self.assertEquals(b.score, 5)
#
# # no idea if this will work
#     def test_update_player(self):
#         self.client.post('/game/create', {'label': '$', 'row': 2, 'col': 3, 'score': 5}) # trying to create board cell with treasure
#         self.client.post('/game/player/update/1', {'row': 0, 'col': 0}) #overriding it and having player now be there
#         b = Board.objects.get(label='1')
#         self.assertEquals(b.label, '1')
#         self.assertEquals(b.row, 0)
#         self.assertEquals(b.col, 0)
#         self.assertEquals(b.score, 0) # not sure if needs to be value after player takes points or no