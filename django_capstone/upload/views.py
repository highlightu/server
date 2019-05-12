from django.shortcuts import render, redirect
from django.http import *
from dashboard.models import Video
from main.models import User
from .models import VideoUploadModel
from .forms import VideoUploadForm
import re, os
from dashboard.views import getThumb
import threading
from .highlightAlgo import makeHighlight
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload(request):
    keys = list(request.session.keys())
    if 'owner' not in keys and 'videoNumber' not in keys and 'today' not in keys:
        return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})

    if request.method == 'POST':  # if form is send by POST...
        request.session['delay'] = int(request.POST.get('delay', ''))
        request.session['face'] = request.POST.get('face', '') == 'on'
        request.session['speech'] = request.POST.get('speech', '') == 'on'
        request.session['chat'] = request.POST.get('chat', '') == 'on'
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
    return render(request, 'mypage/upload.html', {
        'form': VideoUploadForm(), 
        'thumb': getThumb(str(vid)), 
        })


def loading(request):
    return render(request, 'mypage/loading.html')



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
            ############ test code #############

            algorithm_thread = threading.Thread(target=makeHighlight,
                                                    args=(
                                                        new_request,
                                                        user_instance,
                                                        new_video,
                                                    ))
            algorithm_thread.start()

            ############# test code #############
            print('new video object created.')
            # settings.MEDIA_ROOT = temp




            for key in keys:
                if "auth" in key:
                    continue
                del request.session[key]
            return render(request, 'mypage/alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})
        return render(request, 'mypage/alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})


