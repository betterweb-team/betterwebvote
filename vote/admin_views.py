from django.contrib.auth.models import User
from django.shortcuts import render

from util.view_util import admin_page
from vote.models import VOTE_CHOICE, VOTE_CHOICE_TEXT, Vote, Headline
from collections import Counter

VOTE_DICT = {}
for __k, __v in zip(VOTE_CHOICE, VOTE_CHOICE_TEXT):
    VOTE_DICT[__k] = __v


@admin_page
def check_votes(req):
    votes = []
    for headline in Headline.objects.all():
        # Vote Distribution
        vote_ctr = Counter()
        for vote in Vote.objects.filter(headline__id=headline.id).all():
            vote_ctr[vote.choice] += 1

        vote_dist = []
        for k, v in vote_ctr.items():
            vote_dist.append((VOTE_DICT[k], v))

        votes.append((headline, vote_dist, headline.vote_count))
        votes.sort(key=lambda x: x[0].text)

    return render(req, 'vote/check_votes.html', {'votes': votes})


@admin_page
def purge_user(req):
    user_votes = []
    for user in User.objects.all():
        user_votes.append((user, Vote.objects.filter(user__id=user.id).order_by('-timestamp')))

    return render(req, 'vote/purge_user.html', {'user_votes': user_votes})


@admin_page
def admin_controls(req):
    return render(req, 'vote/admin_controls.html')


@admin_page
def purge_user_process(req, user_id):
    pass