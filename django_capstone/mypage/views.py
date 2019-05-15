# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import *
from .models import MergedVideo
from main.models import User
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse, Http404
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header


def archive(request):
    # check if the user is authorized
    user_instance = User.objects.filter(user_name=request.session['owner']).get()
    if user_instance is None:
        return HttpResponse("Unauthorized user")

    # Get result video set
    myMergedVideoSet = MergedVideo.objects.filter(owner=user_instance)
    if myMergedVideoSet is None:
        return HttpResponse("No video found")
    # video_url=myMergedVideoSet[0].video.url
    # pagination
    paginator = Paginator(myMergedVideoSet, 2)  # Show 2 video per page
    page = request.GET.get('page')
    myMergedVideoSet = paginator.get_page(page)
    return render(request, 'archive.html', {
        'merged_videos': myMergedVideoSet,
        'page': page,
        "MEDIA_URL": settings.MEDIA_URL
    })


def download(request, id):
    keys = list(request.session.keys())
    if 'owner' not in keys:
        return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})

    target = MergedVideo.objects.filter(id=id)[0]
    file_path = target.video.path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="video/mp4")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# def display_video(request,vid=None):
#     if vid is None:
#         return HttpResponse("No Video")
#
#     #Finding the name of video file with extension, use this if you have different extension of the videos
#     video_name = ""
#     for fname in os.listdir(settings.MEDIA_ROOT):
#         if fname.fnmatch(fname, vid+".*"): #using pattern to find the video file with given id and any extension
#             video_name = fname
#             break
#
#
#     '''
#         If you have all the videos of same extension e.g. mp4, then instead of above code, you can just use -
#
#         video_name = vid+".mp4"
#
#     '''
#
#     #getting full url -
#     video_url = settings.MEDIA_URL+video_name
#
#     return render(request, "video_template.html", {"url":video_url})


def payment(request):
    # check if the user is authorized
    user_instance = User.objects.filter(user_name=request.session['owner']).get()
    if user_instance is None:
        return HttpResponse("Unauthorized user")

    # Get result video set
    myMergedVideoSet = MergedVideo.objects.filter(owner=user_instance)
    if myMergedVideoSet is None:
        return HttpResponse("No video found")
    # video_url=myMergedVideoSet[0].video.url
    # pagination
    paginator = Paginator(myMergedVideoSet, 2)  # Show 2 video per page
    page = request.GET.get('page')
    myMergedVideoSet = paginator.get_page(page)
    return render(request, 'payment.html', {
        'merged_videos': myMergedVideoSet,
        'page': page,
        "MEDIA_URL": settings.MEDIA_URL
    })


def send_mail(to, reason="finished"):
    # 메시지 내용 작성
    smtp_host = 'smtp.gmail.com'  # Gmail
    smtp_port = 587  # Gmail
    smtp_email = 'laji.cau@gmail.com'  # email
    smtp_pw = 'uqjrfvdodcparspf'  # app_password

    content = ""
    msg = None

    if reason == "finished":
        content = """\
        <html>
         <head></head>
          <body>
            <h2>Extracting highlight is finished!</h2>
            <p>Visit our website to check results!!!</p>
            <br/>
            <a href="https://moyak.kr">LAJI - Auto Highlight Editor</a>
            <br/>
          </body>
        </html>
        """
        msg = MIMEText(content, 'html')
        msg['Subject'] = Header('[LAJI] Notification mail for your highlight request', 'utf-8')

    elif reason == "expired":
        content = 'Your membership period is over. \n\nPlease visit our website to extend your membership.' \
                  + '\n\nAll data will be deleted after 5 days if you don\'t purchase our membership.\n\n'
        content = """\
        <html>
         <head></head>
          <body>
            <h2>Your membership period is over.</h2>
            <p>Please visit our website to extend your membership. All data will be deleted after 5 days if you don\'t purchase our membership.</p>
            <br/>
            <a href="https://moyak.kr">LAJI - Auto Highlight Editor</a>
            <br/>
          </body>
        </html>
        """
        msg = MIMEText(content, 'html')
        msg['Subject'] = Header('[LAJI] Notification mail for your membership expiration', 'utf-8')

    else:
        content = '메일을 보내지 않을 이유가 없다.'
        msg = MIMEText(content.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = Header('[LAJI] 새로운 시대엔 새로운 디버깅 방법 -> 오류가 있다 이말이다.', 'utf-8')

    msg['From'] = smtp_email
    msg['To'] = to

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_email, smtp_pw)
            smtp.sendmail(smtp_email, [to], msg.as_string())
            smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
