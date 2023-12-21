from django.urls import path
from . import views
#for us there is game behind all the player/ stuff, and the empty one is just game/
urlpatterns = [
    path('', views.display, name='display'), # default path when people go to our site and look up 127.0.0.1/game/
    path('player/', views.get_all_players, name='players'), # url path to see all players at once
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'), # url path to create players
    path('player/update/<int:pk>/', views.PlayerUpdate.as_view(),name='player_update'), # url path to update players
    path('create/', views.createGame, name='create' ), # url path to create the game
    path('display/<int:player_number>', views.displayPlayer, name='display_player'), # url path to display the board and each unique players movement options

]