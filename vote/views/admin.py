import json
from collections import Counter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import forms
from django.shortcuts import render, redirect

from vote.models import VOTE_CHOICE, VOTE_CHOICE_TEXT, Vote, Headline

VOTE_DICT = {}
for __k, __v in zip(VOTE_CHOICE, VOTE_CHOICE_TEXT):
    VOTE_DICT[__k] = __v


def admin_page(func):
    @login_required(login_url='login_page')
    def view_wrapper(req, *args, **kwargs):
        if not req.user.is_superuser:
            messages.warning(req, 'Insufficient Permissions! (You were trying to access an admin page)')
            return redirect('index')
        return func(req, *args, **kwargs)

    return view_wrapper


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
def purge_user_page(req):
    user_votes = []
    for user in User.objects.all():
        user_votes.append((user, Vote.objects.filter(user__id=user.id).order_by('-timestamp')))

    return render(req, 'vote/purge_user.html', {'user_votes': user_votes})


class FileForm(forms.Form):
    file = forms.FileField(allow_empty_file=False)


@admin_page
def admin_controls(req):
    return render(req, 'vote/admin_controls.html', {'form': FileForm()})


@admin_page
def purge_user(req, user_id):
    Vote.objects.filter(user__id=user_id).delete()
    return redirect('purge_user_page')


@admin_page
def import_headlines(req):
    content = str(req.FILES['file'].file.read(), 'utf-8')
    ext = req.FILES['file'].name.split('.')[-1]

    if ext == 'json':
        try:
            for line in json.loads(ext):
                headline = Headline(text=line.strip())
                headline.save()
        except json.JSONDecodeError as err:
            messages.warning(req, 'JSON Parse Error: ' + str(err))
            return redirect('admin_controls')

    for line in content.split('\n'):
        headline = Headline(text=line.strip())
        headline.save()

    return redirect('admin_controls')
