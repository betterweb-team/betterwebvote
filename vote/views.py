from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from vote.view_utils import render_index, requires_login
from .models import *


def index(req):
    return render_index(req)


def login_user(req):
    if 'username' not in req.POST or 'password' not in req.POST:
        return render_index(req, 'Missing Username/Password!')

    user = authenticate(req, username=req.POST['username'], password=req.POST['password'])
    if user:
        login(req, user)
        return render_index(req)
    return render_index(req, 'Invalid Username/Password!')


def logout_user(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))


VOTE_CHOICE_OPTIONS = list(zip(VOTE_CHOICE_TEXT, VOTE_CHOICE))


@requires_login
def detail(req, headline_id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    headline = get_object_or_404(Headline, pk=headline_id)
    return render(req, 'vote/detail.html',
                  {'headline': headline, 'choices': VOTE_CHOICE_OPTIONS})


@requires_login
def vote(req, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    try:
        if 'choice' not in req.POST:
            raise ValueError('Choice not specified!')
        choice = int(req.POST['choice'])

        return HttpResponseRedirect(reverse('index'))
    except ValueError as error:
        return render(req, 'vote/detail.html',
                      {'headline': headline, 'choices': VOTE_CHOICE_OPTIONS, 'error': error})
