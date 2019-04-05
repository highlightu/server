from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect
from .models import User


def index(request):
    # print(request.user.username) 로그인하면 해당 아이디 뜸!
    if(len(request.user.username) > 0):
        createUser(request.user.username)

    return render(request, 'home/index.html')


def goHome(request):
    return HttpResponseRedirect('/home/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def social_login(request):
    return render(request, 'user_management/social_login.html')


def createUser(name):
    User.create(name)
    # test
    print(User.user_ID)
