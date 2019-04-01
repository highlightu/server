from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.shortcuts import redirect
from .forms import RequestForm

def index(request):
    return render(request,'home/index.html')

def goHome(request):
    return HttpResponseRedirect('/home/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def dashboard(request):
    return render(request, 'mypage/dashboard.html')


def history(request):
    return render(request, 'mypage/history.html')

def social_login(request):
    return render(request, 'user_management/social_login.html')




def videoRequest(request):
    if request.method == 'POST': # 폼이 제출되었을 경우...
        form = RequestForm(request.POST) # 폼은 POST 데이터에 바인드됨
        if form.is_valid(): # 모든 유효성 검증 규칙을 통과
            # form.cleaned_data에 있는 데이터를 처리
            url = form.cleaned_data['url']
            return render(request, 'mypage/dashboard.html',{'url':url}) # Redirect after POST
    else:
        form = RequestForm() # An unbound form

    return render_to_response('dashboard.html', {
        'url': "https://www.twitch.tv/videos/402913218",
    })


