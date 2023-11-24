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

    # making sure that 2 players so actually populate when the game is created
    def test_players_populated(self):
        #runnign the create command via the url
        self.client.post('/game/create/')
        #making sure both players are on the board on creation
        self.assertEquals(2, len(Player.objects.all()))

        # testing to make sure we can actually move and the correct page is loaded
    def test_move(self):
        # creating game
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        p1 = Player.objects.get(name='1')
        Board.objects.all().delete() #removing so we dont cause undefined behavior
        Player.objects.get(name='2').delete() #removing player 2 and placing it where we want
        p2 = Player()
        p2.name = '2'
        p2.row = 9
        p2.col = 9
        p2.score = 0
        p2.save()
        # settig player one to a corner
        p1.row = 0
        p1.col = 0
        p1.save()
        # moving the player
        response = self.client.post(reverse('display_player', args = [1]),
                                    {'player_direction': 'D'})
        #making sure the command went through
        self.assertEqual(response.status_code, 200)
        p1.refresh_from_db()
        #making sure the player actually moved
        self.assertTrue(p1.row== 1)

    # testing all 4 boundary directions to make sure we dont go out of bounds
    def test_player_boundary(self):
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        p1 = Player.objects.get(name='1')
        p2 = Player.objects.get(name='2')
        # player 1 will be used to check boundaries and so player 2 needs to be in the center to avoid interactions
        p2.row = 5
        p2.col = 5
        #putting player one in the corner so it can test U and R directiosn
        p1.row = 0
        p1.col = 0
        p1.save()
        #testing Up and Right direction movement and boundaries
        self.client.post(reverse('display_player', args=[1]),
                         {'player_direction': 'U'})
        self.assertTrue(Player.objects.get(name='1').row == 0)
        self.client.post(reverse('display_player', args=[1]),
                         {'player_direction': 'R'})
        self.assertTrue(Player.objects.get(name='1').row == 0)
        # putting player 1 in the other corner
        p1.row = 9
        p1.col = 9
        p1.save()
        # testing Down and Left directions and asserting they didnt move d
        self.client.post(reverse('display_player', args=[1]),
                         {'player_direction': 'D'})
        self.assertTrue(Player.objects.get(name='1').row == 9)
        self.client.post(reverse('display_player', args=[1]),
                         {'player_direction': 'L'})
        self.assertTrue(Player.objects.get(name='1').row == 9)


    def test_player_collision(self):
        # creating the game
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        #find player locations
        p1 = Player.objects.get(name='1')
        p2 = Player.objects.get(name='2')
        #setting the location of player 1 and two to be next to each other
        p1.row = 0
        p1.col = 0
        p1.save()
        p2.row = 1
        p2.col = 0
        p2.save()
        #moving the player into the other
        self.client.post(reverse('display_player', args=[2]),
                         {'player_direction': 'U'})
        #making sure player hasnt moved on top of other player
        self.assertTrue(Player.objects.get(name='2').row == 1) # shouldnt have moved

    def test_player_score(self):
        # creating the game
        response_create_game = self.client.post(reverse('create'))
        self.assertTrue(response_create_game.status_code, 302)
        p1 = Player.objects.get(name='1')
        #removing everything from the board to set in particular spots
        Board.objects.all().delete()
        Player.objects.get(name='2').delete()
        # adding player 2 back in an unintrusive spot as its needed for score printing
        p2 = Player()
        p2.name = '2'
        p2.row = 9
        p2.col = 9
        p2.score = 0
        p2.save()
        #changing p1s location
        p1.row = 0
        p1.col = 0
        p1.save()

        # creating and placing a particular treasure
        treasure = Board()
        treasure.label ="$"
        treasure.row = 0
        treasure.col = 1
        treasure.value = 5
        treasure.save()

        # moving the player to the treasure spot
        self.client.post(reverse('display_player', args=[1]),
                         {'player_direction': 'R'})
        #refreshing so we know where p1 is now
        p1.refresh_from_db()
        self.assertEqual(p1.score, 5)



class BoardTestCase(TestCase):
    def test_board_populates(self):
        self.client.post('/game/create/')
        self.assertEquals(5, len(Board.objects.all()))

        for b in Board.objects.all():
            self.assertTrue(b.value > 0)

