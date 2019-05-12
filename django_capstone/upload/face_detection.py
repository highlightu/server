import face_recognition
import cv2
import time

'''
Usage : 
    face_detection(path)
Expected Inputs :
    path : ../cropped_video.mp4
Expected Outputs : 
    Dict { 00:00:00 : [x, y, width, height] }
'''


def face_detection(video_file,x=0, y=0, w=640, h=480):
    # Open the input movie file
    input_video = cv2.VideoCapture(video_file)
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize some variables
    face_locations = list()
    frame_number = 0
    fps = input_video.get(cv2.CAP_PROP_FPS)
    Output_Dict = dict()

    while input_video.isOpened():
        # Grab a single frame of video
        ret, frame = input_video.read()
        frame_number += 1

        #time = input_video.get(cv2.CAP_PROP_POS_MSEC)
        index = input_video.get(cv2.CAP_PROP_POS_FRAMES)

        #print('frames: %d   ---   times: %f' % (index, time/1000))

        if frame is None:
            break

        # Quit when the input video file ends
        if not ret:
            break

        # TODO Check if this one is necessary
        # Resize frame of video to 1/4 size for faster face detection processing
        frame = frame[y:y+h, x:x+w]
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        ''' If we need face recognition '''
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_frame = frame[:, :, ::-1]

        # Find all the faces in the frame
        face_locations = face_recognition.face_locations(small_frame)

        ''' If CNN is possible '''
        # face_locations = face_recognition.face_locations(small_frame, model="cnn")

        # Execute only face is detected
        if face_locations:

            ''' Face Detection '''
            for face_location in face_locations:
                top, right, bottom, left = face_location
                location = [top, left, right-left, bottom-top ]

            if index % 30 == 0:
                timestamp = time.strftime('%H:%M:%S', time.gmtime(index/30))
                Output_Dict[timestamp] = location
 
        # No face is detected at the frame
        else:
            continue
    # All done!
    input_video.release()
    cv2.destroyAllWindows()

    return Output_Dict
