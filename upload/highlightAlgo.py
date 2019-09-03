from .face_detection import face_detection
from .chatAnalyze import ChatAnalyze
from .video_util import *
from .video_util import cropVideo
from mypage.models import MergedVideo
from django.core.files import File
from django.conf import settings
from mypage.views import send_mail
from queue import Queue
from moviepy.editor import VideoFileClip

import subprocess
import os
import re
import platform
import shutil

HIGHLIGHT_DEBUG = True

# queueing system using producer-consumer logic
queue = Queue()
queue.put(object())


class Error(Exception):
    pass


class AlgorithmError(Error):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def getTwitchChat(videoID, savePath):

    text_file = videoID + ".txt"
    chatLogPath = os.path.join(savePath, text_file)
    if os.path.isfile(chatLogPath):
        print("Chatlog already exists ! ")
        return chatLogPath
    else:
        for (path, dir, files) in os.walk(settings.MEDIA_ROOT):
            for filename in files:
                if filename == text_file:
                    print("Chatlog found in previous request ! ")
                    shutil.copy2(os.path.join(path, filename), chatLogPath)
                    return chatLogPath

    system = platform.system()
    if system == "Linux":
        if savePath[-1] != '/':
            savePath = savePath + '/'
        proc = ["sudo", "tcd",
                "-v", videoID,
                "--output", savePath,
                "--format", "capstone",
                ]
    elif system == "Windows":
        if savePath[-1] != '\\':
            savePath = savePath + '\\'

        proc = ["tcd",
                "-v", videoID,
                "--output", savePath,
                "--format", "capstone",
                ]
    else:
        print("Cannot detect operating system...")
        return None
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
    try:
        subprocess.check_call(proc)
        print("twitch chat download finish!")
        print("this file downloaded in ", savePath)

        return chatLogPath

    except subprocess.CalledProcessError as e:
        print("Twitch chat download failed: ", e)
        return None


def makeCandidatesByChatlog(chatlog, numOfHighlights, cummulative_sec):

    labeldwords = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
                   'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy',
                   'omfg', 'kappa', 'trihard', '4head', 'cmonbruh', 'lul', 'haha', 'sourpls',
                   'feelsbadman', 'feelsgoodman', 'gachigasm',  'monkas', 'pepehands',
                   'destructroid', 'jebaited']

    f = open(chatlog, 'rt', encoding='UTF8')

    # Download nltk
    chat_analyzer = ChatAnalyze(f, labeldwords)
    score = chat_analyzer.Preprocessing()
    result = chat_analyzer.Scoring(score)
    sectioned_result = chat_analyzer.Sectioned_Scoring(result, cummulative_sec)
    sorted_list = sorted(sectioned_result.items(),
                         key=lambda t: t[1], reverse=True)[:numOfHighlights]
    sorted_list = dict(sorted([(t, v) for t, v in sorted_list]))
    print("[Chat analyze result]")
    print(sorted_list)
    f.close()

    return sorted_list


def second(timestamp):
    arr = re.split("[:]", timestamp)
    if len(arr) != 3:
        print("check time string :"+timestamp)
    else:
        return int(arr[0])*3600 + int(arr[1])*60 + int(arr[2])
    return -1


def No_facedetection(dictionary):
    output = dict()
    for k, v in dictionary.items():
        changed_time = second(k)
        output[changed_time] = v
    return output


def getTimeSection(candidates, videoLen, delay):
    # make raw candidate list (must be sorted by key)
    candidates = list(candidates.keys())

    # if picked points are too close
    mergeList = {}
    deleteList = []
    for i in range(len(candidates)):
        if i in deleteList:
            continue
        else:
            mergeList[candidates[i]] = candidates[i]
            j = 1
            while i+j < len(candidates) and candidates[i+j] - candidates[i] < delay:
                deleteList.append(i + j)
                # ex) 300: 310 -> 300: 320 -> 300: 330
                mergeList[candidates[i]] = candidates[i+j]
                j += 1

    if HIGHLIGHT_DEBUG:
        print("Merge List : ", end=' ')
        print(mergeList)
        print("Will be deleted : ", end=' ')
        print(deleteList)
        # print("Will be deleted : ", end=' ')
        print("[Candidates]")
        print(candidates)

    for i in deleteList:
        candidates[i] = -1

    if HIGHLIGHT_DEBUG:
        print(candidates)

    candidates = [[i-2*delay, mergeList[i]+delay] for i in candidates if i != -1]

    if HIGHLIGHT_DEBUG:
        print("using -2*delay ~ +delay")
        print(candidates)

    # post-processing
    for i in range(len(candidates)):
        if candidates[i][0] < 0:
            candidates[i][0] = 0
        if candidates[i][1] > videoLen:
            candidates[i][1] = videoLen

    return candidates

def getLasttime(chatlog):
    f = open(chatlog, 'rt', encoding='UTF8')
    lineList = f.readlines() 
    f.close()

    lastline = lineList[-1]
    lasttime = lastline.split(" ")
    inttime = lasttime[0].split(":")

    output = (int(inttime[0]) * 3600) + \
                (int(inttime[1]) * 60) + \
                (int(inttime[2]))
    
    return output-300


def makeHighlight(highlight_request, user_instance, video_object):
    queue.get()
    numOfHighlights = 10
    multiplier = 4 # 후보군을 몇배수로 추출할지 결정
    cummulative_sec = 10

    try:

        # Chat Download
        chat_save_path = os.path.join(
            settings.MEDIA_ROOT, highlight_request.path)
        print("The downloaded chat will be stored at --> " + chat_save_path)
        chatlog = getTwitchChat(str(video_object.videoNumber), chat_save_path)

        # If TCD fails, there will be no highlight
        if chatlog is None:
            print("Fail to create chatlog !!!")
            raise AlgorithmError
        #
        # 채팅로그의 마지막 시간 <= 업로드한 비디오 시간.
        #
        lasttime = getLasttime(chatlog)
        # clip = VideoFileClip(video_object.videoFileURL)
        # if lasttime >= round(clip.duration):
            # print("do what you need")

        video_length = get_video_length(clip=highlight_request.videoFile.path)

        if lasttime >= video_length:
            print(lasttime, video_length)
            highlight_request.delete()
            video_object.delete()
            os.remove(highlight_request.videoFile.path)
            send_mail(to=user_instance.user_email, reason="failed")
            queue.put(object())
            return


        #
        # Make Highlights
        #
        
        delay = int(video_object.delay)  # add input delay value
        print(delay)

        if video_object.face == True:
            print("Face Detection On !!")
            temp_cand = makeCandidatesByChatlog(chatlog=chatlog,
                                                numOfHighlights=numOfHighlights*multiplier, cummulative_sec=cummulative_sec)
            # TODO videopath should be input

            # Get video path and resized frame info
            videopath = video_object.videoFileURL.path
            x = video_object.rect_x
            y = video_object.rect_y
            width = video_object.rect_width
            height = video_object.rect_height

            cand = face_detection(videopath, temp_cand, x,
                                  y, width, height, cummulative_sec)

        else:
            print("Face Detection Off !!")
            cand = makeCandidatesByChatlog(chatlog=chatlog,
                                           numOfHighlights=numOfHighlights, cummulative_sec=cummulative_sec)
            cand = No_facedetection(cand)



        sections = getTimeSection(
            candidates=cand, videoLen=video_length, delay=delay)

        ''' Print highlight list'''
        i = 0
        for eachHighlight in sections:
            print("[{}] highlight : {}".format(i, eachHighlight))

        highlights = split_video(video_path=highlight_request.videoFile.path,
                                 save_path=chat_save_path,
                                 video_id=video_object.videoNumber,
                                 split_times=sections)

        #
        # Register them on DB
        #
        nov = 1  # number of video
        for highlight in highlights:
            with open(highlight, 'rb') as file:
                highlight_obj = MergedVideo.objects.create(
                    owner=user_instance,
                    videoNumber=video_object.videoNumber,
                    date=video_object.date,
                    path=highlight_request.path,
                    video=None,
                    title=highlight_request.title + str(nov)
                )

                # Link DB and files
                highlight_obj.video.save(
                    highlight_request.title + str(nov) + ".mp4", File(file))
                nov += 1

        for highlight in highlights:
            os.remove(highlight)

        send_mail(to=user_instance.user_email)

        user_instance.membership_remaining -= 1
        user_instance.save()
        queue.put(object())
    except:

        # When highlight process fails
        send_mail(to=user_instance.user_email, reason="failed")
        queue.put(object())
