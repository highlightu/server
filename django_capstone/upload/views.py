from django.shortcuts import render, redirect
from django.http import *
from dashboard.models import Video
from main.models import User
from .forms import VideoUploadForm
import re
from django.conf import settings


def upload(request):
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})

    if request.method == 'POST':  # if form is send by POST...
        request.session['delay'] = request.POST.get('delay', '')
        request.session['face'] = request.POST.get('face', '') == 'on'
        request.session['speech'] = request.POST.get('speech', '') == 'on'
        request.session['chat'] = request.POST.get('chat', '') == 'on'
        request.session['youtube'] = request.POST.get('youtube', '') == 'on'
        request.session['rect_x'] = request.POST.get('rect_x', '')
        request.session['rect_y'] = request.POST.get('rect_y', '')
        request.session['rect_width'] = request.POST.get('rect_width', '')
        request.session['rect_height'] = request.POST.get('rect_height', '')

    # Redirect after POST
    return render(request, 'mypage/upload.html', {'form': VideoUploadForm()})


def loading(request):
    return render(request, 'mypage/loading.html')


def uploadVideo(request):
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})

    user_name = request.session['owner']
    vid = request.session['videoNumber']
    date = re.sub('[.]', '', request.session['today'])

    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['videoFileURL'] = settings.MEDIA_ROOT + '\\' + str(user_name) + '\\' + str(
                date) + '\\' + str(vid) + '\\'
            temp = settings.MEDIA_ROOT
            settings.MEDIA_ROOT = request.session['videoFileURL']
            # print(request.session['videoFileURL'])
            user_instance = User.objects.filter(user_name=request.session['owner']).get()
            # print(type(user_instance))
            # print(user_instance)

            new_video = Video.objects.create(
                owner=user_instance,
                videoNumber=request.session['videoNumber'],
                delay=request.session['delay'],
                face=request.session['face'],
                speech=request.session['speech'],
                chat=request.session['chat'],
                youtube=request.session['youtube'],
                date=date,
                videoFileURL=request.session['videoFileURL']
            )
            print('new video object created.')

            form.save()
            settings.MEDIA_ROOT = temp

    for key in keys:
        del request.session[key]
    return redirect("/home/")
