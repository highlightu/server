import cv2
import numpy as np
import time
from deep import build_net
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


def face_detection(video_file, original_candidate, pixel_x, pixel_y, width, height):
    # Open the input movie file
    input_video = cv2.VideoCapture(video_file)
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize some variables
    face_locations = list()
    check_timelist = list()
    fps = round(input_video.get(cv2.CAP_PROP_FPS))
    section = 5
    Checklist_withchat = Change_timeunit(
        list(original_candidate.keys()), section)
    Output_Dict = dict()

    face_cascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')
    model_emo = build_net()
    emotions = ["Fear", "Happy", "Sad", "Surprise", "Neutral"]

    gy_offset = 0
    gx_offset = 0

    for eachValue in Checklist_withchat.values():
        for eachElement in eachValue:
            check_timelist.append(eachElement)

    while input_video.isOpened():
        # Grab a single frame of video
        ret, frame = input_video.read()
        #time = input_video.get(cv2.CAP_PROP_POS_MSEC)
        index = input_video.get(cv2.CAP_PROP_POS_FRAMES)
        #print('frames: %d   ---   times: %f' % (index, time/1000))

        if frame is None:
            break

        # Quit when the input video file ends
        if not ret:
            break

        # Check each sec if it is in the Checklist
        if (index/fps) not in set(check_timelist):
            continue

        # TODO Check if this one is necessary
        # Resize frame of video to 1/4 size for faster face detection processing
        # x, y , w, h

        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Find all the faces in the frame
        #face_locations = face_recognition.face_locations(small_frame)
        frame = frame[pixel_y:pixel_y+height, pixel_x:pixel_x+width]
        grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_locations = face_cascade.detectMultiScale(grayed, 1.3, 5)

        ''' Face Detection '''
        # We assume there is only one face in the image
        # Execute only face is detected

        for (x, y, w, h) in face_locations:

            print("Face is detected at {} at time {} sec".format(
                face_locations, (index/fps)))

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

            print(emotion_probability)
            print(emotion)

            if emotion == 'Neutral':
                emotion_probability = 0

            # We will replace the time value with emotion_probability
            '''
            Example:

            Checklist_withchat = { time(sec) : [ time(sec), time(sec)+1, ... , time(sec)+4] }
            
            if the time(sec) is 70 (1min 10sec),
                we will look up all value in Checklist_withchat to replace 70 with emotion_probability

            '''
            for key, value in Checklist_withchat.items():

                if (index/fps) in value:

                    idx = value.index((index/fps))

                    Checklist_withchat[key][idx] = emotion_probability

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("checklist withchat")
    print(Checklist_withchat)

    # Replace unchanged values with 0 in Checklist_withchat
    for key, value in Checklist_withchat.items():
        if value > 1:
            Checklist_withchat[key] == 0

    # Sum up
    for key, value in Checklist_withchat.items():
        sumValue = 0
        timesection = section
        for eachValue in value:
            if eachValue == 0:
                timesection -= 1
            sumValue += eachValue
        Output_Dict[key] = (sumValue / timesection) * \
            original_candidate[key]  # normalizing

    print("output dict")
    print(Output_Dict)

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
