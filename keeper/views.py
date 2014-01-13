from django.shortcuts import render
from django.views.generic.list import ListView

from keeper.models import Player, Goal, Game


class PlayerListView(ListView):

    model = Player
    context_object_name = 'player_list'


class GoalListView(ListView):

    model = Goal
    context_object_name = 'goal_list'


class GameListView(ListView):

    model = Game
    context_object_name = 'game_list'
