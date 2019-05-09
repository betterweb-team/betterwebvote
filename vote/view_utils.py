from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def requires_login(func):
    def wrapper(req, *args, **kwargs):
        if not req.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return func(req, *args, **kwargs)
    return wrapper


def render_index(req, error=None):
    if error:
        return render(req, 'vote/index.html', {'user': req.user, 'error': error})
    return render(req, 'vote/index.html', {'user': req.user})
