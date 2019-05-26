from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect
from .models import User
# 썸네일 이미지를 얻기 위해 추가
import requests
import json




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
            new_user = User.objects.create(user_name=request.user.username,user_email=request.user.email)
            # print(new_user)
            # new_instance = deepcopy(new_user)
            # new_instance.id = None
            # getUserInstance(new_instance)

            new_user.save()
            print("new user")

    # User.objects.new.create(user_name=request.user.username)
        return render(request, 'home/index.html', {'newbie':not token})
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
