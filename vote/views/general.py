from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from vote.models import *

INDEX_ARTICLE_COUNT = 20  # Number of Headlines displayed per page


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


# Form to select political bias
class VoteChoicesForm(forms.Form):
    choice = forms.ChoiceField(choices=[('', 'Select')] + list(zip(VOTE_CHOICES, VOTE_CHOICES_TEXT)),
                               label='Political Bias')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('choice', css_class='form-group ml-4'),
                css_class='form-row'
            ),
            Submit('submit', 'Vote!')
        )


@login_required(login_url='login')
def vote(req, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    if Vote.objects.filter(headline__id=headline_id, user__id=req.user.id).count() > 0:
        messages.error(req, 'Duplicate vote!')
        return redirect('index', headline_id)

    form = VoteChoicesForm(req.POST or None)

    if form.is_valid():
        choice = form.cleaned_data['choice']
        vote_entry = Vote(headline=headline, user=req.user, choice=choice, timestamp=datetime.now())
        vote_entry.save()

        messages.success(req, 'Success!')
        return redirect('index')

    return render(req, 'vote/vote.html',
                  {'headline': headline, 'form': form})
