from django.shortcuts import render
from django.http import *
import subprocess
from .forms import RequestForm  # , VideoForm
from django.utils import timezone

import requests
import re

thSize = {'width': '1168', 'height': '657'}
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


def dashboard(request):
    if request.method == 'POST':  # if form is send by POST...
        form = RequestForm(request.POST)  # bind it to the request form
        if form.is_valid():  # if it has all attributes
            fullURL = form.cleaned_data['url']
            owner = form.cleaned_data['sender'].split('@')[0]

            vid = re.split("[/]", fullURL)[-1]
            url = "https://player.twitch.tv/?autoplay=false&video=v" + vid

            request.session['videoNumber'] = int(vid)
            request.session['owner'] = owner

            # date
            date = str(timezone.localtime())
            date = re.split('[ ]', date)[0]
            date = re.sub('[-]', '.', date)
            request.session['today'] = date

            date = re.split("[.]",date)
            month = dateDict[date[1]]
            day = date[2]


            request.session['month'] = month
            request.session['day'] = day

            # Redirect after POST
            return render(request, 'mypage/dashboard.html', {
                'url': url,
                'thumb': getThumb(vid),
            })
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

    proc = ["tcd",
            "-v", videoID,
            "--output", savePath,
            "--format", "capstone",
            ]

    subprocess.run(proc)

    print("twitch chat download finish!")
    print("this file downloaded in ", savePath)

    chatLogPath = savePath + videoID + ".txt"

    return chatLogPath