from django.db import models


class Player(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def get_initials(self):
        return '.'.join(self.first_name[0], self.last_name[0])

    # when players want unique initials do something like
    #initials = models.CharField(max_length=5)
    # def save(self, *args, **kwargs):
    #
    #     if 'initials' not in kwargs:
    #         self.initials = self.get_initials()
    #     else:
    #         self.initials = kwargs['initials']
    #
    #     super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Player {first} {last} ({initials})".format(
            first=self.first_name,
            last=self.last_name,
            initials=self.get_initials())


class Game(models.Model):

    white_team = models.ManyToManyField(Player, related_name='white_team')
    yellow_team = models.ManyToManyField(Player, related_name='yellow_team')

    final_white_score = models.IntegerField(default=0)
    final_yellow_score = models.IntegerField(default=0)

    finished = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Game {time}".format(time=self.finished)
