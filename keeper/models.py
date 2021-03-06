import operator
from django.db import models


class PlayerManager(models.Manager):

    def get_query_set(self):
        return sorted(super(PlayerManager, self).get_query_set().all(), key=operator.attrgetter('aggregate_scored'))[::-1]

    #     pms = super(PlayerManager, self).get_query_set().all()
    #     # return auths
    #     # ordered = sorted(pms, key=operator.attrgetter('aggregate_scored'))
    #     ordered = sorted(pms)
    #     return ordered
    pass

class Player(models.Model):

    card_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # sorted = PlayerManager()
    # score_objects = PlayerManager()

    def get_initials(self):
        return '.'.join([self.first_name[0], self.last_name[0]])

    @property
    def aggregate_scored(self):
        return Goal.objects.filter(scorer_id=self.id).count()

    def __unicode__(self):
        return "{first} {last} ({initials})".format(
            first=self.first_name,
            last=self.last_name,
            initials=self.get_initials())


class Game(models.Model):

    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)

    white_team = models.ManyToManyField('Player', related_name='white_team')
    yellow_team = models.ManyToManyField('Player', related_name='yellow_team    ')

    white_team_goals = models.ManyToManyField('Goal', related_name='white_team_goal')
    yellow_team_goals = models.ManyToManyField('Goal', related_name='yellow_team_goal')

    class Meta:
        ordering = ['-finished',]

    def yellow_team_text(self):
        return ", ".join([str(p) for p in self.yellow_team.all()])

    def white_team_text(self):
        return ", ".join([str(p) for p in self.white_team.all()])

    def __unicode__(self):
        return "{w_score}:{y_score} ({time})".format(
            time=self.finished.strftime("%d/%m/%y %H:%M"),
            w_score=self.white_team_goals.count(),
            y_score=self.yellow_team_goals.count())


class Goal(models.Model):

    scorer = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{scorer} {time}".format(
            scorer=self.scorer.get_initials(), time=self.time)
