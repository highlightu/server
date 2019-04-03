from django.shortcuts import render
from django.http import *
from .forms import RequestForm


def upload(request):
    return render(request, 'mypage/upload.html')


def loading(request):
    return render(request, 'mypage/loading.html')
