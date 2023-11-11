from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='display'), # default path when people go to our site and look up 127.0.0.1/game/
    path('player/', views.get_all_players, name='players'),
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('player/update/<int:pk>/', views.PlayerUpdate.as_view(),name='player_update'),
    path('create/', views.CreateGame.as_view(), name='create' ),
   # path('display/<int:player_id>', views.displayPlayer),
]