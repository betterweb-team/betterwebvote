from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

LOGIN_MSGS = {
    'badcred': 'Invalid Username/Password!',
    'nocred': 'Missing Username/Password!'
}


def login_page(req, message=None):
    if message:
        return render(req, 'vote/login.html', {'message': LOGIN_MSGS[message]})
    return render(req, 'vote/login.html')


def login_user(req):
    user = authenticate(req, username=req.POST['username'], password=req.POST['password'])
    if user:
        login(req, user)
        return redirect('index')
    return redirect('login_page', 'badcred')


def logout_user(req):
    logout(req)
    return redirect('index')
