import json
import logging
import random
from datetime import datetime, timedelta

import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from keeper.models import Player, Game, Goal


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def get_names(count=5):
    # http://muffinlabs.com/content/namey-random-name-generator/
    url = 'http://namey.muffinlabs.com/name.json?with_surname=true&count=%d' % count

    r = requests.get(url)

    return json.loads(r.text) if r.ok else None


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def get_random_date(self, start=None, end=None):

        d1 = datetime.strptime('1/1/2012 0:00 AM', '%m/%d/%Y %H:%M %p') if start is None else start
        d2 = datetime.strptime('1/1/2013 0:00 AM', '%m/%d/%Y %H:%M %p') if end is None else end

        d1 = timezone.make_aware(d1, timezone.get_default_timezone())
        d2 = timezone.make_aware(d2, timezone.get_default_timezone())

        return random_date(d1, d2)

    def generate_players(self, count):

        for name in get_names(count):
            firstName, lastName = name.split(' ')

            while True:

                card_id = random.randint(1, 1000000)

                if Player.objects.filter(card_id=card_id).exists():
                    continue

                player = Player.objects.create(
                    first_name=firstName,
                    last_name=lastName,
                    card_id=card_id
                )

                break

            self.logger.info("Generated %s" % player)

    def generate_games_and_goals(self, games):

        for i in range(games):

            players = Player.objects.order_by('?')[:4]
            white_team, yellow_team = players[:2], players[2:]

            game = Game.objects.create()
            game.white_team = white_team
            game.yellow_team = yellow_team
            game_start = self.get_random_date()
            game_finished = game_start + timedelta(minutes=10)

            for i in range(10):

                players, colour = random.choice(((white_team, 'white'), (yellow_team, 'yellow')))

                goal_scorer = random.choice(players)

                goal = Goal.objects.create(
                    scorer=goal_scorer,
                    game=game)

                goal_time = self.get_random_date(game_start, game_finished)
                goal.save()

                # force update of 'time'
                Goal.objects.filter(id=goal.id).update(time=goal_time)

                if colour == 'white':
                    game.white_team_goals.add(goal)
                else:
                    game.yellow_team_goals.add(goal)

            game.save()

            # force 'start' 'finished' avoiding auto_add_now
            Game.objects.filter(id=game.id).update(started=game_start, finished=game_finished)

            self.logger.info("Generated game %s" % game)

    def handle(self, *args, **options):

        self.logger = logging.getLogger('django')
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("Generating DB Entries")

        self.generate_players(count=10)

        self.generate_games_and_goals(games=50)
