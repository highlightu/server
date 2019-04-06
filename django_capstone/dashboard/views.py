from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from .forms import RequestForm
import requests
import re

thSize = {'width': '1168', 'height': '657'}

def dashboard(request):
    if request.method == 'POST':  # if form is send by POST...
        form = RequestForm(request.POST)  # bind it to the request form
        if form.is_valid():  # if it has all attributes
            fullURL = form.cleaned_data['url']
            vid = re.split("[/]",fullURL)[-1]
            url = "https://player.twitch.tv/?autoplay=false&video=v" + vid
            # Redirect after POST
            return render(request, 'mypage/dashboard.html', {'url': url,'thumb':getThumb(vid)})
    return render(request, 'mypage/alert.html',{'msg':"잘못된 접근입니다"})


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
