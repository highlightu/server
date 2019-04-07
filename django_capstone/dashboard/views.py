from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from django.db.models import F
from django.contrib import auth

from .forms import RequestForm  # , VideoForm
from dashboard.models import Video
from main.models import User

import requests
import re

import subprocess

thSize = {'width': '1168', 'height': '657'}


def dashboard(request):
    if request.method == 'POST':  # if form is send by POST...
        form = RequestForm(request.POST)  # bind it to the request form
        if form.is_valid():  # if it has all attributes
            fullURL = form.cleaned_data['url']
            sender = form.cleaned_data['sender']
            senderlist = sender.split('@')

            vid = re.split("[/]", fullURL)[-1]
            url = "https://player.twitch.tv/?autoplay=false&video=v" + vid

            # Add video object
            print("in dashboard")

            user_instance = User.objects.filter(user_name=senderlist[0]).get()
            print(type(user_instance))
            print(user_instance)

            # 이부분에서 getTwitchChat 호출 후 DB에 등록
            # chat 다운로드가 오래걸리기 때문에
            # 쓰래드로 처리를 시키고 랜더링을 시켜주는게 더 좋을 것이라고생각됨.
            # chatPath = getTwitchChat(vid, "Path") // Path는chat이 저장될 위치

            new_video = Video.objects.create(
                owner=user_instance, Video_Number=vid)

            print(new_video.owner, new_video.Video_Number)
            print("new video")

            # Redirect after POST
            return render(request, 'mypage/dashboard.html', {'url': url, 'thumb': getThumb(vid)})
    return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})


# def findUserInstance(user_name):
#     user_intance = User.objects.filter(user_name=F(user_name))
#     print('in FUI ' + user_intance)
#     return user_intance


def history(request):
    return render(request, 'mypage/history.html')


def getVideoId(url):
    VideoId = url.split("/")[-1]
    return VideoId


def getThumb(videoId):

    # API요청을 보내기 위한 헤더
    TWITCH_CLIENT_ID = "37v97169hnj8kaoq8fs3hzz8v6jezdj"
    TWITCH_CLIENT_ID_HEADER = "Client-ID"
    TWITCH_V5_ACCEPT = "application/vnd.twitchtv.v5+json"
    TWITCH_V5_ACCEPT_HEADER = "Accept"
    TWITCH_AUTHORIZATION_HEADER = "Authorization"

    VIDEO_URL = "https://api.twitch.tv/kraken/videos/" + videoId

    headers = {TWITCH_CLIENT_ID_HEADER: TWITCH_CLIENT_ID,
               TWITCH_V5_ACCEPT_HEADER: TWITCH_V5_ACCEPT}

    # API 요청을 보낸다.
    video_request = requests.get(VIDEO_URL, headers=headers)
    video_request_json = video_request.json()

    # 썸네일 템플릿 url 획득
    thumb_template_url = str(video_request_json['preview']['template'])

    # 1920x1080크기의 썸네일 이미지를 얻는다.
    size = thSize

    return thumb_template_url.format(**size)


def getTwitchChat(videoID, savePath):
    # getTwitchChat("406987059","/home/moyak/") 이런식으로 사용
    #
    #tcd 를 사용하기 위해 셋팅이 필요
    #
    #python 3.7 이상으로 tcd를 설치(이전 버전에서는 동작하지 않음)
    # git clone https://github.com/PetterKraabol/Twitch-Chat-Downloader
    # cd Twtich-Chat-Downloader
    # python3 setup.py build
    # sudo python3 setup.py install
    #
    #chat log를 원하는 포멧으로 저장하기 위해 설정 수정
    #
    # ~/.config/tcd/setting.json
    # 파일에서 
    #"capstone": {
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
    #},
    # 
    # 추가.

    proc = ["tcd",
            "-v", videoID,
            "--output", savePath,
            "--format", "capstone",
            ]

    subprocess.run(proc)

    print("twitch chat download finish!")
    print("this file downloaded in ",savePath)
    
    chatLogPath = savePath + videoID + ".txt"

    return chatLogPath
