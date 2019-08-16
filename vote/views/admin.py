import json
import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from vote.models import VOTE_CHOICES, Vote, Headline, VOTE_CHOICES_TEXT_SHORT

"""
ADMIN PAGE DECORATOR
"""


def admin_page(func):
    @login_required(login_url='login')
    def view_wrapper(req, *args, **kwargs):
        if not req.user.is_superuser:
            messages.warning(req, 'Insufficient Permissions! (You were trying to access an admin page)')
            return redirect('index')
        return func(req, *args, **kwargs)

    return view_wrapper


"""
CHECK VOTES PAGE
"""


@admin_page
def check_votes(req):
    votes = []
    for headline in Headline.objects.all():
        vote_dist = [headline.vote_count(choice) for choice in VOTE_CHOICES]
        votes.append((headline, vote_dist, sum(vote_dist)))

    votes.sort(key=lambda x: (-x[2], x[0].text))

    return render(req, 'vote/check_votes.html', {'votes': votes, 'choices_text': VOTE_CHOICES_TEXT_SHORT})


"""
PURGE USER PAGE
"""


@admin_page
def purge_user_page(req):
    user_votes = []
    for user in User.objects.all():
        vote_query = Vote.objects.filter(user__id=user.id)
        user_votes.append((user, vote_query.order_by('-timestamp'), vote_query.count()))
    return render(req, 'vote/purge_user.html', {'user_votes': user_votes})


@admin_page
def purge_user(req, user_id):
    Vote.objects.filter(user__id=user_id).delete()
    messages.success(req, 'Success!')

    return redirect('purge_user_page')


"""
IMPORT HEADLINES PAGE
"""

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
    file = forms.FileField(allow_empty_file=False, required=False)
    encoding = forms.ChoiceField(choices=ENCODINGS + [('other', 'Other')], required=True)
    encoding_other = forms.CharField(label='Other', required=False)

    def clean(self):
        cleaned_data = super().clean()

        encoding = cleaned_data.get('encoding_other') if cleaned_data.get('encoding') == 'other' else cleaned_data.get(
            'encoding')
        if not encoding:
            self.add_error('encoding_other', 'This field is required.')
        cleaned_data['encoding'] = encoding

        try:
            file = self.files.get('file')
            if file is None:
                # It doesn't matter what kind of error (as long as it's being caught by the try block)
                raise LookupError('This field is required.')

            content = str(file.read(), encoding)

            _, ext = os.path.splitext(self.files.get('file').name)
            if ext == '.json':
                try:
                    headlines = json.loads(content)

                    # Validate that JSON data is proper
                    if type(headlines) != list:
                        self.add_error('file', 'Data must be list of strings! (Object is not list)')
                    else:
                        if any([type(headline) != str for headline in headlines]):
                            self.add_error('file', 'Data must be list of strings! (List element are not all strings)')
                        else:
                            cleaned_data['file'] = headlines

                except json.JSONDecodeError as e:
                    self.add_error('file', 'JSON Parse Error: ' + str(e))
            elif ext == '.txt':
                # Process text files
                cleaned_data['file'] = [headline.strip() for headline in content.split('\n')]
            else:
                self.add_error('file', f'Unsupported Extension: \'{ext}\'')
        except (LookupError, UnicodeDecodeError) as e:
            self.add_error('file', str(e))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('file', css_class='is-invalid form-group ml-4')
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
    form = ImportFileForm(req.POST or None, req.FILES or None)

    # print(form.is_valid())
    if form.is_valid():
        # print('is valid!')
        headlines = form.cleaned_data['file']

        Headline.objects.bulk_create([Headline(text=headline) for headline in headlines])
        messages.success(req, 'Success!')

    return render(req, 'vote/import_export_headlines.html', {'form': form})


"""
EXPORT HEADLINES PAGE
"""


@admin_page
def export_headlines(req):
    headlines = {}
    for headline in Headline.objects.all():
        qu = Vote.objects.filter(headline__id=headline.id)
        headlines[headline.text] = dict(((k, qu.filter(choice=k).count()) for k in VOTE_CHOICES))

    return render(req, 'raw_text.html', {'text': json.dumps(headlines, indent=4, sort_keys=True)})
