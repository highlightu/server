from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect

def index(request):
    return render(request, 'home/index.html')


def goHome(request):
    return HttpResponseRedirect('/home/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def social_login(request):
    return render(request, 'user_management/social_login.html')
