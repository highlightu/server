from django.shortcuts import render, redirect
from django.http import *
from dashboard.models import Video
from main.models import User
from .models import VideoUploadModel
from .forms import VideoUploadForm
import re, os
from django.conf import settings
import subprocess
from dashboard.views import getThumb
import threading


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

        user_name = request.session['owner']
        vid = request.session['videoNumber']
        date = re.sub('[.]', '', request.session['today'])
        request.session['path'] = os.path.join(settings.MEDIA_ROOT,str(user_name),str(date),str(vid))
        if not os.path.exists(request.session['path']):
            os.makedirs(request.session['path'])
        print(request.session['path'])

    # Redirect after POST
    return render(request, 'mypage/upload.html', {
        'form': VideoUploadForm(), 
        'thumb': getThumb(str(vid)), 
        })


def loading(request):
    return render(request, 'mypage/loading.html')

def getTwitchChat(videoID, savePath):
    # getTwitchChat("406987059","/home/moyak/") 이런식으로 사용
    #
    # tcd 를 사용하기 위해 셋팅이 필요
    #
    # python 3.7 이상으로 tcd를 설치(이전 버전에서는 동작하지 않음)
    # git clone https://github.com/PetterKraabol/Twitch-Chat-Downloader
    # cd Twtich-Chat-Downloader
    # python3 setup.py build
    # sudo python3 setup.py install
    #
    # chat log를 원하는 포멧으로 저장하기 위해 설정 수정
    #
    # ~/.config/tcd/setting.json
    # 파일에서
    # "capstone": {
    #    "comments": {
    #       "format": "{timestamp[relative]} {message[body]}",
    #       "ignore_new_messages": false,
    #       "timestamp": {
    #           "relative": "%X"
    #        }
    #   },
    #   "output": {
    #       "format": "{id}.txt",
    #       "timestamp": {
    #           "absolute": "%x"
    #       }
    #   }
    # },
    #
    # 추가.

    ############################# for Windows #############################
    if savePath[-1] != '\\':
        savePath = savePath + '\\'

    proc = ["tcd",
            "-v", videoID,
            "--output", savePath,
            "--format", "capstone",
            ]
    ############################# for Windows #############################


    ############################# for Linux #############################
    # if savePath[-1] != '/':
    #     savePath = savePath + '/'
    # proc = ["sudo", "tcd",
    #         "-v", videoID,
    #         "--output", savePath,
    #         "--format", "capstone",
    #         ]
    ############################# for Linux #############################
    subprocess.run(proc)

    print("twitch chat download finish!")
    print("this file downloaded in ", savePath)

    chatLogPath = savePath + videoID + ".txt"

    return chatLogPath

def uploadVideo(request):
    global delimiter
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})


    if request.method == "POST":
        print(request.POST)
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            date = re.sub('[.]', '', request.session['today'])

            # temp = settings.MEDIA_ROOT
            # settings.MEDIA_ROOT = request.session['videoFileURL']
            # print(request.session['videoFileURL'])
            user_instance = User.objects.filter(user_name=request.session['owner']).get()
            # print(type(user_instance))
            # print(user_instance)

            new_request=VideoUploadModel.objects.create(
                title=form.cleaned_data['title'],
                path=request.session['path'],
                videoFile=form.cleaned_data['videoFile'],
            )
            print('Upload object created.')

            new_video = Video.objects.create(
                owner=user_instance,
                videoNumber=request.session['videoNumber'],
                delay=request.session['delay'],
                face=request.session['face'],
                speech=request.session['speech'],
                chat=request.session['chat'],
                youtube=request.session['youtube'],
                date=date,
                videoFileURL=new_request.videoFile,
                title=form.cleaned_data['title'],
                rect_x=request.session['rect_x'],
                rect_y=request.session['rect_y'],
                rect_width=request.session['rect_width'],
                rect_height=request.session['rect_height'],
            )

            print('new video object created.')
            # settings.MEDIA_ROOT = temp

            print(request.session['videoNumber'],request.session['path'])
            #chat download!!!
            chat_download_thread = threading.Thread(target=getTwitchChat, args=(str(request.session['videoNumber']),str(request.session['path'])))
            chat_download_thread.start()


            for key in keys:
                if "auth" in key:
                    continue
                del request.session[key]
            return render(request, 'mypage/alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})
        return render(request, 'mypage/alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})


