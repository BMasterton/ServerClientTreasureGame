from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Player, Board
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import random

def doesCellNotExist(row, col): #so we know what is at a given table location
    value = Board.objects.filter(row = row, col = col).first()
    if value:
        return False
    else:
        return True

def addTreasure(): #randomly grab values, and put them in table value based on row and colum, check first for if tht spot has a value
    counter = 0
    while counter < 5:
        row = random.randint(0,9)
        column = random.randint(0,9)
        value = random.randint(1,10)
        if doesCellNotExist(row, column):
            new_cell = Board()
            new_cell.col = column
            new_cell.row = row
            new_cell.label = "$"
            new_cell.value = value
            new_cell.save()
            counter += 1
        else:
            continue


def addPlayer():
    counter = 0
    while counter < 2:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        if doesCellNotExist(row, column):
            new_cell = Player()
            new_cell.col = column
            new_cell.row = row
            new_cell.name = str(counter+1)
            new_cell.score = 0
            new_cell.save()
            counter += 1
        else:
            continue


def display(request):
    #the request here will get the info from sumbitted form in the html, then enter that data
    context = getLabelContext()
    return render(request, "board_form.html", context)


class CreateGame(CreateView):
    Board.objects.all().delete()
    Player.objects.all().delete()
    model = Board
    fields = '__all__'
    addTreasure()
    addPlayer()
    success_url = reverse_lazy('create')

class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('players')

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    success_url = reverse_lazy('players')



def get_all_players(request): #probably gonna hav to use with score at some point 
    players = Player.objects.all()
    result = ''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse(result)

def index(request):
    return HttpResponse('Hello World1!')

def get_player(request, player_id):
    players = Player.objects.filter(pk=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse(f'Player {player.tag} is at row {player.row} and col {player.col}')
    else:
        return HttpResponse('No such player')

def get_player_Score(request, player_number ):
    player = Player.objects.filter(name=player_number).first()

    if player:
        playerScore = player.score
    return HttpResponse(str(playerScore))

def getLabelContext():
    board_data = Board.objects.all()
    player_data = Player.objects.all()

    labels = [['' for _ in range(10)] for _ in range(10)]
    for data in board_data:
        row, col = data.row - 1, data.col - 1
        labels[row][col] = data.label if data.value else ''
    for data in player_data:
        row, col = data.row - 1, data.col - 1
        labels[row][col] = data.name if data.name else ''
    context = {'labels': labels}
    return context

def playerMove(player_direction, player_number):
    player = Player.objects.filter(name=player_number).first()

    if player:
        playerRow = player.row
        playerCol = player.col

        # Update player position based on the direction
        if player_direction == 'U':
            if playerRow > 0:
                player.row -= 1
        elif player_direction == 'D':
            if playerRow < 9:
                player.row += 1
        elif player_direction == 'L':
            if playerCol > 0:
                player.col -= 1
        elif player_direction == 'R':
            if playerCol < 9:
                player.col += 1

        # Save the updated player object
        player.save()

        # Redirect or render a response as needed
        # return redirect('display_player', player_number=player.name)


def displayPlayer(request):
    if request.method == 'POST':
        if request.POST.get('player_number'):
            player_number = request.POST.get('player_number')
        elif request.POST.get('player_direction'):
            player_direction = request.POST.get('player_direction')

    playerMove(player_direction, player_number)


    context = getLabelContext()
    if player_number == 1:
        return render(request, 'Player1Display.html', context)
    if player_number == 2:
        return render(request, 'Player2Display.html', context)
        