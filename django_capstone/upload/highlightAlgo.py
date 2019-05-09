from dashboard.models import MergedVideo
from django.core.files import File
import os
from .chatAnalyze import ChatAnalyze
from .video_util import *
from django.conf import settings
import subprocess
import threading

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


def makeHighlight(highlight_request, user_instance, videoid, savepath, rect_x=0, rect_y=0, rect_width=0, rect_height=0):

    # Chat Download
    chat_save_path = os.path.join(settings.MEDIA_ROOT, savepath)
    print("The downloaded chat will be stored at --> " + chat_save_path)
    # chat download!!!
    chat_download_thread = threading.Thread(target=getTwitchChat,
                                            args=(str(videoid), chat_save_path))
    chat_download_thread.start()

    # No Face Detection
    if rect_width == 0 or rect_height == 0:
        labeldwords = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
                       'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']
        f = open("test.txt", 'rt', encoding='UTF8')

        # Download nltk
        chatanlyze = ChatAnalyze(f, labeldwords)

        score = chatanlyze.Preprocessing()
        result = chatanlyze.Scoring(score)
        sectioned_result = chatanlyze.Sectioned_Scoring(result, 5)
        cand = chatanlyze.makeCandidateList(histogram=sectioned_result,
                                            numOfMaximumHighlight=10,
                                            delay=1000,
                                            videoLen=19000)

        print(cand)
        # video_path = 'demo_video.mp4'
        video_path = highlight_request.videoFile.path
        # split_times = [[0, 3], [10, 13], [20, 30]]
        split_times = cand
        split_video(video_path, split_times)

    # Face Detection On
    else:
        ########################################################################################
        # Algorithms go here
        filepath1 = cropVideo(
            inputFile=highlight_request.videoFile.path,
            outputFile="face_detected.mp4",
            x=rect_x,
            y=rect_y,
            w=rect_width,
            h=rect_height
        )

        # Result file
        f1 = open(filepath1, 'rb')

        # Register them on DB
        a = MergedVideo.objects.create(
            owner=user_instance,
            videoNumber=409803829,
            date="20190424",
            path=savepath,
            video=None,
        )

        # Link DB and files
        a.video.save(highlight_request.title + ".mp4", File(f1))
        f1.close()
        ########################################################################################

        # ########################################################################################
        # # Algorithms go here
        # filepath2 = cropVideo(
        #     inputFile=highlight_request.videoFile.path,
        #     outputFile="face_detected.mp4",
        #     x=0,
        #     y=0,
        #     w=100,
        #     h=100
        # )
        #
        # # Result file
        # f2 = open(filepath2, 'rb')
        #
        # # Register them on DB
        # b = MergedVideo.objects.create(
        #     owner=user_instance,
        #     videoNumber=40980383243,
        #     date="20190427",
        #     path=savepath,
        #     video=None,
        # )
        # # Link DB and files
        # b.video.save(highlight_request.title + "2.mp4", File(f2))
        # f2.close()
        # ########################################################################################
        #
        # ########################################################################################
        # # Algorithms go here
        # filepath3 = cropVideo(
        #     inputFile=highlight_request.videoFile.path,
        #     outputFile="face_detected.mp4",
        #     x=100,
        #     y=100
        # )
        #
        # # Result file
        # f3 = open(filepath3, 'rb')
        #
        # # Register them on DB
        # c = MergedVideo.objects.create(
        #     owner=user_instance,
        #     videoNumber=409803829,
        #     date="20190502",
        #     path=savepath,
        #     video=None,
        # )
        #
        # # Link DB and files
        # c.video.save(highlight_request.title + "3.mp4", File(f3))
        # f3.close()
        # ########################################################################################

        # After algorithm runs
        os.remove("face_detected.mp4")