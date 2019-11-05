from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from mypage.models import Video
from main.models import User
from .models import VideoUploadModel
from .forms import VideoUploadForm
from .forms import RequestForm
from .highlightAlgo import makeHighlight
from mypage.views import get_date

import os
import threading
import re
import requests


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

labelwordOf = {
    'ko' : ['와', '오', '으', '쩐다', '미친', '방금', '캬', '키야', '갈고리', '뭐지', '캡처', '클립',
            'ㅋ', 'ㅎ', 'ㅁㅊ', 'ㄷ', 'ㅇㅅㅇ', 'ㅅ', 'ㄱㅈㅇ', '?', ],
    'en' : ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
         'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy',
         'omfg', 'kappa', 'trihard', '4head', 'cmonbruh', 'lul', 'haha', 'sourpls',
         'feelsbadman', 'feelsgoodman', 'gachigasm', 'monkas', 'pepehands',
         'destructroid', 'jebaited']
}

@login_required(login_url='/social/')
def dashboard(request):
    get_date(request)
    keys = list(request.session.keys())
    if request.method == 'POST':  # if form is send by POST...
        form = RequestForm(request.POST)  # bind it to the request form
        if form.is_valid():  # if it has all attributes
            fullURL = form.cleaned_data['url']
            owner = form.cleaned_data['sender'].split('@')[0]

            vid = re.split("[/]", fullURL)[-1]
            print("Working VideoNumber is : " + vid)
            url = "https://player.twitch.tv/?autoplay=false&video=v" + vid

            request.session['videoNumber'] = int(vid)
            request.session['owner'] = owner

            # Redirect after POST
            return render(request, 'dashboard.html', {
                'thumb': getThumb(vid),
            })
        else:
            return render(request, 'alert.html', {'msg': "Invalid Form was sent."})

    elif 'owner' in keys and 'videoNumber' in keys and 'today' in keys:     # kind of redirect or something...
        return render(request, 'dashboard.html', {
            'thumb': getThumb(str(request.session['videoNumber'])),
        })
    # no session data nor valid post data
    return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})


def getVideoId(url):
    VideoId = url.split("/")[-1]
    return VideoId


def getThumb(videoId, size=thSize):
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

    return thumb_template_url.format(**size)


@csrf_exempt
@login_required(login_url='/social/')
def upload(request):
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})

    if request.method == 'POST':  # if form is send by POST...
        request.session['delay'] = int(request.POST.get('delay', ''))
        request.session['face'] = request.POST.get('face', '') == 'on'
        request.session['speech'] = request.POST.get('speech', '') == 'on'
        request.session['chat'] = request.POST.get('chat', 'ko')
        request.session['youtube'] = request.POST.get('youtube', '') == 'on'
        request.session['rect_x'] = int(request.POST.get('rect_x', ''))
        request.session['rect_y'] = int(request.POST.get('rect_y', ''))
        request.session['rect_width'] = int(request.POST.get('rect_width', ''))
        request.session['rect_height'] = int(request.POST.get('rect_height', ''))

        user_name = request.session['owner']
        vid = request.session['videoNumber']
        date = re.sub('[.]', '', request.session['today'])
        request.session['path'] = os.path.join(str(user_name),str(date),str(vid))
        print(request.session['path'])

    # Redirect after POST
    return render(request, 'uploading.html', {
        'form': VideoUploadForm(), 
        'thumb': getThumb(str(vid),{'width': '1920', 'height': '1080'}),
        'imageURL' : 'images/flags/' + request.session['chat'],
        'example_words': labelwordOf[request.session['chat']],
        })

@login_required(login_url='/social/')
def loading(request):
    return render(request, 'loading.html')



@login_required(login_url='/social/')
def uploadVideo(request):
    global delimiter
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})


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
                chat=True,
                youtube=request.session['youtube'],
                date=date,
                videoFileURL=new_request.videoFile,
                title=form.cleaned_data['title'],
                rect_x=request.session['rect_x'],
                rect_y=request.session['rect_y'],
                rect_width=request.session['rect_width'],
                rect_height=request.session['rect_height'],
            )
            ############ test code #############

            algorithm_thread = threading.Thread(target=makeHighlight,
                                                    args=(
                                                        new_request,
                                                        user_instance,
                                                        new_video,
                                                        request.session['chat'],
                                                    ))
            algorithm_thread.start()

            ############# test code #############
            print('new video object created.')
            # settings.MEDIA_ROOT = temp



            for key in keys:
                if "auth" in key:
                    continue
                del request.session[key]
            return render(request, 'alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})
        return render(request, 'alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})


