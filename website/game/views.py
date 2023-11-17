from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Player, Board
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import random
from django.db import transaction

#checking is a cell doesnt exist if there is a value in that cell then we return false else the oposite
def doesCellNotExist(row, col): #so we know what is at a given table location
    value = Board.objects.filter(row = row, col = col).first()
    if value:
        return False
    else:
        return True

# Will be adding 5 treasures, we grab random locations and a value, and we check to see if the random spot exists
# if there is nothing in that spot then we add the new treaure value and we set the label to be a $ indicating something is there
def addTreasure():
    counter = 0
    while counter < 5:
        row = random.randint(0,9)
        column = random.randint(0,9)
        value = random.randint(1,10)
        if doesCellNotExist(row, column): # if that cell is free
            new_cell = Board() # creating a new board model
            new_cell.col = column
            new_cell.row = row
            new_cell.label = "$"
            new_cell.value = value
            new_cell.save() # save all changes made
            counter += 1
        else:
            continue

#adding a player just like treausure but only 2 thing time
def addPlayer():
    counter = 0
    while counter < 2:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        if doesCellNotExist(row, column):
            new_cell = Player() # creating a new player model
            new_cell.col = column
            new_cell.row = row
            new_cell.name = str(counter+1)
            new_cell.score = 0
            new_cell.save() # making sure we save all changes made
            counter += 1
        else:
            continue


#this displays the board through the board_form.html.
def display(request):
    #the request here will get the info from sumbitted form in the html, then enter that data
    context = getLabelContext() # all data in the board is returned from this, anything that has a value
    return render(request, "board_form.html", context)

# creates the game, so we delete all the old objects we created before, and we make the board model, we then 'fill'
#the board with treasures and players
class CreateGame(CreateView):
    Board.objects.all().delete()
    Player.objects.all().delete()
    model = Board
    fields = '__all__'
    addTreasure()
    addPlayer()
    success_url = reverse_lazy('create')

#Creates the player model
class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('players')

#can be used to update the player model
class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    success_url = reverse_lazy('players')

# returns an httpresponse with all player names and prints them to the screen to see
def get_all_players(request):
    players = Player.objects.all()
    result = ''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse(result)

# used just like get_all_players, but only returns the value of the requested player
def get_player(request, player_id):
    players = Player.objects.filter(pk=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse(f'Player {player.tag} is at row {player.row} and col {player.col}')
    else:
        return HttpResponse('No such player')


def addIfTreasure(playerRow, playerColumn):
    cell = Board.objects.filter(row=playerRow, col=playerColumn).first()
    player = Player.objects.filter(row=playerRow, col=playerColumn).first()
    if cell and cell.value > 0 : # if there is a call meaning a treasure is there
        print(f"Before: Player {player.name} Score: {player.score}")
        player.score += cell.value # score goes back to zero each time
        player.save()
        print(f"After: Player {player.name} Score: {player.score}")
        cell.value = 0 # this is happening
        cell.save()


def isPlayer(playerRow, playerColumn):
    player = Player.objects.filter(row=playerRow, col=playerColumn).first()
    if player:
        return True
    else:
        return False

# this function gets all board and player data makes a matrix out of them, and then sets values to the matrix based on
#row and col positions. This creates the board visual object
def getLabelContext():
    board_data = Board.objects.all()
    player_data = Player.objects.all()

    labels = [['.' for _ in range(10)] for _ in range(10)] # creating a 10 x 10 matrix //either add the '.' here
    for data in board_data:
        row, col = data.row , data.col 
        labels[row][col] = data.label if data.value else '.' #or maybe here
    for data in player_data:
        row, col = data.row , data.col 
        labels[row][col] = data.name if data.name else '.'
    context = {'labels': labels}
    return context

#moves the players depending on direction checked, does check for players and treasure
@transaction.atomic
def playerMove(player_direction, player_number):
    player = Player.objects.filter(name=player_number).first()

    if player:
        # Update player position based on the direction
        if player_direction == 'U' and player.row > 0:
            if not isPlayer(player.row -1, player.col): # stops players from going out of bounds
                player.row -= 1 # move player
                player.save() # save the change
                addIfTreasure(player.row, player.col) # runs add treasure with the current tile
        elif player_direction == 'D' and player.row < 9:
            if not isPlayer(player.row + 1, player.col):
                player.row += 1
                player.save()
                addIfTreasure(player.row, player.col)
        elif player_direction == 'L' and player.col > 0:
            if not isPlayer(player.row , player.col- 1):
                player.col -= 1
                player.save()
                addIfTreasure(player.row, player.col)
        elif player_direction == 'R' and player.col < 9:
            if not isPlayer(player.row ,player.col + 1):
                player.col += 1
                player.save()
                addIfTreasure(player.row, player.col)


# main function that gets the post request from the html form, and gets a player direction which it
#will then try to move that player, and printing the string matrix so a player can see whats happening
def displayPlayer(request, player_number):
    if request.method == 'POST':
        if request.POST.get('player_direction'):
            player_direction = request.POST.get('player_direction')
        playerMove(player_direction, player_number)


    context = getLabelContext()
    context['player1_score'] = Player.objects.filter(name=1).first().score # probably need to fix this.
    context['player2_score'] = Player.objects.filter(name=2).first().score
    if player_number == 1: # if its player one then display player1's unique html
        return render(request, 'Player1Display.html', context)
    if player_number == 2:
        return render(request, 'Player2Display.html', context)
