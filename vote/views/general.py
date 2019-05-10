from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from vote.models import *


VOTE_CHOICE_OPTIONS = list(zip(VOTE_CHOICE_TEXT, VOTE_CHOICE))
INDEX_ARTICLE_COUNT = 20


@login_required(login_url='login')
def index(req):
    context = {'user': req.user}
    voted_already = Vote.objects.filter(user__id=req.user.id).values_list('headline')
    headlines = Headline.objects.order_by('-pub_time').exclude(id__in=voted_already)
    size = headlines.count()

    if size:
        context['headlines'] = headlines[:INDEX_ARTICLE_COUNT]
    else:
        context['headlines'] = None
    if size > INDEX_ARTICLE_COUNT:
        context['more'] = size - INDEX_ARTICLE_COUNT
    context['headlines_size'] = size

    return render(req, 'vote/index.html', context)


@login_required(login_url='login')
def detail(req, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    return render(req, 'vote/detail.html',
                  {'headline': headline, 'choices': VOTE_CHOICE_OPTIONS})


@login_required(login_url='login')
def vote(req, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    if Vote.objects.filter(headline__id=headline_id, user__id=req.user.id).count() > 0:
        messages.warning(req, 'Duplicate vote!')
        return redirect('index')

    try:
        if 'choice' not in req.POST:
            raise ValueError('Choice not specified!')
        choice = int(req.POST['choice'])
        vote_entry = Vote(headline=headline, user=req.user, choice=choice, timestamp=datetime.now())
        vote_entry.save()

        messages.info(req, 'Success!')
        return redirect('index')
    except ValueError as err:
        messages.warning(req, str(err))
        return redirect('detail', headline_id)
