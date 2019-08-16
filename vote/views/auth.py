from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.req = kwargs.pop('req', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group ml-3')
            ),
            Row(
                Column('password', css_class='form-group ml-3')
            ),
            Submit('submit', 'Login')
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if (username and password) and not authenticate(self.req, username=username, password=password):
            self.add_error('username', 'Invalid Credentials!')
            self.add_error('password', 'Invalid Credentials!')

        return cleaned_data


def login_user(req):
    form = LoginForm(req.POST or None, req=req)

    if form.is_valid():
        user = authenticate(req, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(req, user)
        return redirect('index')

    return render(req, 'vote/login.html', {'form': form})


def logout_user(req):
    logout(req)
    return redirect('login')
