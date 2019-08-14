import json
from collections import Counter

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from vote.models import VOTE_CHOICE, VOTE_CHOICE_TEXT, Vote, Headline

VOTE_DICT = {}
for __k, __v in zip(VOTE_CHOICE, VOTE_CHOICE_TEXT):
    VOTE_DICT[__k] = __v


def admin_page(func):
    @login_required(login_url='login')
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


ENCODINGS = list(map(lambda x: (x, x), [
    'ascii',
    'utf_8',
    'utf_16',
    'utf_32',
    'iso-8859-1',
    'cp1251',
    'cp1252'
]))


class ImportFileForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True)
    encoding = forms.ChoiceField(choices=ENCODINGS + [('other', 'Other')], required=False)
    encoding_other = forms.CharField(label='Other', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('file', css_class='form-group ml-4')
            ),
            Row(
                Column('encoding', css_class='form-group ml-4')
            ),
            Row(
                Column('encoding_other', css_class='form-group ml-4')
            ),
            Submit('submit', 'Import Headlines')
        )


@admin_page
def import_export_headlines(req):
    return render(req, 'vote/import_export_headlines.html', {'form': ImportFileForm()})


@admin_page
def export_headlines(req):
    return redirect('import_votes')


@admin_page
def purge_user(req, user_id):
    Vote.objects.filter(user__id=user_id).delete()
    return redirect('purge_user_page')


@admin_page
def import_headlines(req):
    encoding = req.POST['encoding']
    if encoding == 'other':
        encoding = req.POST['encoding_other']
    print(encoding)

    # Try to parse content, if fail return
    try:
        content = str(req.FILES['file'].file.read(), encoding)
    except (LookupError, UnicodeDecodeError) as e:
        messages.error(req, str(e))
        return redirect('admin_controls')

    ext = req.FILES['file'].name.split('.')[-1]

    print(content, type(content))

    if ext == 'json':
        try:
            for line in json.loads(content):
                headline = Headline(text=line.strip())
                headline.save()

            messages.success(req, 'Success!')
        except json.JSONDecodeError as err:
            messages.error(req, 'JSON Parse Error: ' + str(err))
            return redirect('admin_controls')
    elif ext == 'txt':
        for line in content.split('\n'):
            headline = Headline(text=line.strip())
            headline.save()

        messages.success(req, 'Success!')
    else:
        messages.error(req, f'Unsupported Extension: \'.{ext}\'')

    return redirect('admin_controls')
