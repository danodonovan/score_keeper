import operator
from django.views.generic.list import ListView

from keeper.models import Player, Goal, Game


class PlayerListView(ListView):

    model = Player
    template_name = 'keeper/player_list.html'
    context_object_name = 'player_list'

    queryset = sorted(Player.objects.all(), key=lambda a: a.aggregate_scored)[::-1]


class GoalListView(ListView):

    model = Goal


class GameListView(ListView):

    model = Game
