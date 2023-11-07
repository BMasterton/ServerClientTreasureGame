from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/', views.get_all_players, name='players'),
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('player/update/<int:pk>/', views.PlayerUpdate.as_view(),name='player_update'),
]