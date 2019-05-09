from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from bisect import bisect_left


class Headline(models.Model):
    text = models.CharField(max_length=512, verbose_name='Text')
    pub_time = models.DateTimeField(verbose_name='Time Published', default=datetime.now)

    def __str__(self):
        return self.text

    @property
    def vote_count(self):
        return Vote.objects.filter(headline__id=self.id).count()


VOTE_CHOICE = [-2, -1, 0, 1, 2]
VOTE_CHOICE_TEXT = ['Far Left', 'Left', 'Center', 'Right', 'Far Right']


class Vote(models.Model):
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE, verbose_name='Headline')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    choice = models.IntegerField(verbose_name='Choice')
    timestamp = models.DateTimeField(verbose_name='Timestamp', default=datetime.now)

    @property
    def choice_str(self):
        return VOTE_CHOICE_TEXT[bisect_left(VOTE_CHOICE, self.choice)]

    def __str__(self):
        return 'Vote for "%s": %s' % (self.headline, self.choice_str)


DB_MODELS = [Headline, Vote]
