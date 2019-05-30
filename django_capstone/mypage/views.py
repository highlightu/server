# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from django.http import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import auth


from .models import MergedVideo
from main.models import User
from main.models import WithdrawnUser

import os, re
import smtplib
from email.mime.text import MIMEText
from email.header import Header


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


@login_required(login_url='/social/')
def archive(request):
    # Get result video set
    user_instance = User.objects.filter(user_name=request.user.username).get()
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


@login_required(login_url='/social/')
def download(request, id):
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





def get_date(request):
    date = str(timezone.localtime())
    date = re.split('[ ]', date)[0]
    date = re.sub('[-]', '.', date)
    request.session['today'] = date

    date = re.split("[.]", date)
    year = date[0]
    month = dateDict[date[1]]
    day = date[2]

    request.session['year'] = year
    request.session['month'] = month
    request.session['day'] = day


@login_required(login_url='/social/')
def payment(request):
    get_date(request)
    user_instance = User.objects.filter(user_name=request.user.username).get()
    request.session['remaining'] = user_instance.membership_remaining
    request.session['total_pay'] = user_instance.total_pay
    return render(request, 'payment.html')


@login_required(login_url='/social/')
def withdraw(request):
    user_instance = User.objects.filter(user_name=request.user.username).get()
    # user_instance.membership_remaining = 0
    # user_instance.save()
    #
    # request.session['remaining'] = user_instance.membership_remaining
    # request.session['total_pay'] = user_instance.total_pay

    # register user as a withdrawn user, all data will be saved.
    WithdrawnUser.objects.create(
        user_name=user_instance.user_name,
        user_email=user_instance.user_email,
        membership_remaining=user_instance.membership_remaining,
        total_pay=user_instance.total_pay,
    )
    user_instance.delete()
    auth.logout(request)
    return HttpResponseRedirect('/home/')


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
        msg['Subject'] = Header('[LAJI] Notification mail for your MEMBERSHIP EXPIRATION', 'utf-8')

    elif reason == "failed":
        content = """\
        <html>
         <head></head>
          <body>
            <h2>Sorry.</h2>
            <p>We failed to create a video. Please check your video is the right one.</p>
            <br/>
            <a href="https://moyak.kr">LAJI - Auto Highlight Editor</a>
            <br/>
          </body>
        </html>
        """
        msg = MIMEText(content, 'html')
        msg['Subject'] = Header('[LAJI] Notification mail for FAILURE processing your request', 'utf-8')

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
