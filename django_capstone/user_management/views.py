from django.shortcuts import render
from django.http import *
from django.contrib import auth


def social_login(request):
    return render(request, 'social_login.html')


def home(request):
    return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
