from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect
from .models import User
# 썸네일 이미지를 얻기 위해 추가
import requests
import json
from django.utils import timezone
import re

dateDict = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec',
}


def index(request):
    if (len(request.user.username) > 0):
        print(User.objects.values('user_name'))
        checklist = list(User.objects.values('user_name'))
        token = False

        # check if the account is already created or not.
        for element in checklist:
            if element['user_name'] == request.user.username:
                # 이미 생성된 계정임.
                print("it is detected")
                token = True
                break
        if (token is False):
            new_user = User.objects.create(user_name=request.user.username)
            # print(new_user)
            # new_instance = deepcopy(new_user)
            # new_instance.id = None
            # getUserInstance(new_instance)

            new_user.save()
            print("new user")

    # User.objects.new.create(user_name=request.user.username)
    # date
    date = str(timezone.localtime())
    date = re.split('[ ]', date)[0]
    date = re.sub('[-]', '.', date)
    request.session['today'] = date

    date = re.split("[.]", date)
    year = date[0]
    month = dateDict[date[1]]
    day = date[2]

    request.session['year'] = year
    request.session['month'] = month
    request.session['day'] = day
    return render(request, 'home/index.html')


# def getUserInstance(new_instance):
#     return new_instance


def goHome(request):
    return HttpResponseRedirect('/home/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def social_login(request):
    return render(request, 'user_management/social_login.html')
