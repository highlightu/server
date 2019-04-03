from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect

# 썸네일 이미지를 얻기 위해 추가
import requests
import json


def index(request):
    return render(request, 'home/index.html')


def goHome(request):
    return HttpResponseRedirect('/home/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def social_login(request):
    return render(request, 'user_management/social_login.html')
