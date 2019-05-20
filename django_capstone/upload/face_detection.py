import cv2
import numpy as np
import time
from .deep import build_net
from collections import deque
from tflearn.data_preprocessing import ImagePreprocessing

'''
Usage :
    face_detection(video_file, original_candidate, x, y, w, h)
Expected Inputs :
    video_file : ../cropped_video.mp4
    original_candidate : Dict { '00:00:00':0.5 , ... }
    x , y , w , h = resized frame
Expected Outputs :
    Dict { 00:00:00 : score calculted with chat score }
'''


def face_detection(video_file, original_candidate, pixel_x, pixel_y, width, height, inputsection):
    # Open the input movie file
    input_video = cv2.VideoCapture(video_file)
    # the number of total frame of the video
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    # frame per second of the video
    fps = round(input_video.get(cv2.CAP_PROP_FPS))

    print('length = {}, fps = {} '.format(length, fps))

    # Initialize some variables
    face_locations = list()
    check_timelist = list()
    section = inputsection
    gy_offset = 0
    gx_offset = 0

    # Special varialbes
    '''
    Checklist_withchat = { time(sec) : [time(sec) , time(sec)+1 , .. , time(sec)+4] , ... }
    Checklist_withframe = [ time(sec), .. ]
    '''

    Checklist_withchat = Change_timeunit(
        list(original_candidate.keys()), section)

    Checklist_withframe = Make_Checklist_withframe(Checklist_withchat)

    Output_Dict = dict()

    # Start main function
    # Load model
    face_cascade = cv2.CascadeClassifier(
        'upload/haarcascade_frontalface_default.xml')
    model_emo = build_net()
    emotions = ["Fear", "Happy", "Sad", "Surprise", "Neutral"]

    # check timelist for scoring
    for eachValue in Checklist_withchat.values():
        for eachElement in eachValue:
            check_timelist.append(eachElement)

    # Get the specific frame
    iteration = 0
    print('Checklist_withframe : ', Checklist_withframe)

    # Read specific moment (second)
    ''' 1 STEP '''
    for eachTime in Checklist_withframe:

        '''If YOU WANT TO CHECK VALUES'''
        # print('============================')
        # print('#iteration = ', iteration)
        # iteration += 1
        # print('eachtime = ', eachTime)
        # print('eachframe = ', eachTime * fps)

        
        maxValue = list()
        framelist = check_framelist(eachTime, fps)

        '''Check each frame in the specific time 
           and append all emotional probability to maxValue array
        '''
        # Example, if fps is 30, and the specific moment is 10s,
        # this will check frames from #frame 270~299

        ''' 2 STEP ''' 
        for eachFrame in framelist:
        
            # Set the frame number where you are heading to
            # input_video.set(int propid, doulbe value): 
            # int propid = 1 ( cv::CAP_PROP_POS_FRAMES = 1 )
            input_video.set(1, eachFrame)

            # Grab a single frame of video
            ret, frame = input_video.read()
            #time = input_video.get(cv2.CAP_PROP_POS_MSEC)

            index = input_video.get(cv2.CAP_PROP_POS_FRAMES)

            # print('current frame number is ', ret)
            # print('current time is ', (index/fps))

            if frame is None:
                continue

            # Quit when the input video file ends
            if not ret:
                continue

            # Find all the faces in the frame

            frame = frame[pixel_y:pixel_y+height, pixel_x:pixel_x+width]
            grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_locations = face_cascade.detectMultiScale(grayed, 1.3, 5)

            ''' Face Detection '''
            # We assume there is only one face in the image
            # Execute only face is detected

            ''' 3 STEP '''
            for (x, y, w, h) in face_locations:

                print("Face is detected at {} at time {} sec".format(
                    face_locations, round((index/fps))))

                # TODO IF YOU WANT TO SEE THE IMAGE THAT HAS DETECTED FACE
                if ret == True:
                    cv2.imshow("", frame)

                y_offset = y
                x_offset = x+w

                gy_offset = y_offset
                gx_offset = x_offset

                roi_gray = grayed[y:y + h, x:x + w]

                image_scaled = np.array(cv2.resize(
                    roi_gray, (48, 48)), dtype=float)
                image_processed = image_scaled.flatten()
                processedimage = image_processed.reshape([-1, 48, 48, 1])
                print("predict image")

                prediction = model_emo.predict(processedimage)
                emotion_probability, emotion_index = max(
                    (val, idx) for (idx, val) in enumerate(prediction[0]))
                emotion = emotions[emotion_index]

                if emotion == 'Neutral':
                    emotion_probability = 0

                print(emotion_probability)
                print(emotion)

                # We will consider only max value among evalutated values in the frames
                maxValue.append(emotion_probability)

                # We will replace the time value with emotion_probability
                '''
                Example:

                Checklist_withchat = { time(sec) : [ time(sec), time(sec)+1, ... , time(sec)+4] }
                
                if the time(sec) is 70 (1min 10sec),
                    we will look up all value in Checklist_withchat to replace 70 with emotion_probability

                '''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        ''' 4 STEP '''
        for key, value in Checklist_withchat.items():

            for eachValue in value:
                if eachValue == eachFrame:

                # Replace the time(sec) value with emotion_probability
                    Checklist_withchat[key][value.index(
                    eachValue)] = max(maxValue)

    ''' 5 STEP '''
    # Replace unchanged values with 0 in Checklist_withchat
    for key, value in Checklist_withchat.items():
        index = 0
        for eachValue in value:
            if eachValue > 1:
                Checklist_withchat[key][index] = 0
            index += 1

    print('Outputted Checklist_withchat : ', Checklist_withchat, end='\n')
    print('Original_candidate : ', original_candidate, end='\n')
    # Sum up
    for key, value in Checklist_withchat.items():
        sumValue = 0
        timesection = section
        for eachValue in value:
            if eachValue == 0:
                timesection -= 1
            elif eachValue > 1:
                eachValue = 0
            sumValue += eachValue

        try:
            Output_Dict[key] = (sumValue / timesection) * \
                original_candidate[Change_inverse_timeunit(key)]  # normalizing
        except ZeroDivisionError:
            # If there is no face detected in the section, 
            # We divide chatlog value by 2
            Output_Dict[key] = original_candidate[Change_inverse_timeunit(key)] / 2

    print("Output Dict : ", Output_Dict, end='\n')

    # All done!
    input_video.release()
    cv2.destroyAllWindows()

    return Output_Dict


def Change_timeunit(time_list, section):
    output = dict()
    for eachtime in time_list:
        sectioned_list = list()
        int_timelist = eachtime.split(":")
        for frame in range(section):
            temp_result = (int(int_timelist[0]) * 3600) + \
                (int(int_timelist[1]) * 60) + \
                (int(int_timelist[2]))
            sectioned_list.append(temp_result)
            int_timelist[2] = int(int_timelist[2]) + 1
        output[sectioned_list[0]] = sectioned_list

    return output


def Change_inverse_timeunit(time_sec):

    hour = time_sec / 3600
    minute = (time_sec % 3600) / 60
    second = (time_sec % 60)

    output = '%01d' % hour + ':' + '%02d' % minute + ':' + '%02d' % second
    return output


def Make_Checklist_withframe(Checklist_withchat):
    # all distinct values in checklist_withchat should be checked
    frame_list = list()

    print('Inputted Checklist_withchat ', Checklist_withchat)

    for key, value in Checklist_withchat.items():
        for eachValue in value:
            if eachValue not in set(frame_list):
                frame_list.append(eachValue)

    return frame_list

def check_framelist(eachTime, fps):
    output = list()

    for i in range(1, fps+1):
        output.append((eachTime * fps) - i)

    return output.sort()