from django.shortcuts import render
from django.http import *
from .forms import UploadVideoForm
from dashboard.forms import UploadOptionForm

def upload(request):
    if request.method == 'POST':  # if form is send by POST...
        # form = UploadOptionForm(request.POST)
        # if form.is_valid():
            delay = request.POST.get('delay','')
            face = request.POST.get('face', '') == 'on'
            speech = request.POST.get('speech', '') == 'on'
            chat = request.POST.get('chat', '') == 'on'
            youtube = request.POST.get('youtube', '') == 'on'

            # Redirect after POST
            return render(request, 'mypage/upload.html', {'delay': delay,
                                                          'face': face,
                                                          'speech': speech,
                                                          'chat': chat,
                                                          'youtube': youtube
                                                          })



def loading(request):
    return render(request, 'mypage/loading.html')
