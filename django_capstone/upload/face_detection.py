# import face_recognition
# import cv2
# import time
#
# '''
# Usage :
#     face_detection(video_file, original_candidate, x, y, w, h)
# Expected Inputs :
#     video_file : ../cropped_video.mp4
#     original_candidate : Dict { '00:00:00':0.5 , ... }
#     x , y , w , h = resized frame
# Expected Outputs :
#     Dict { 00:00:00 : score calculted with chat score }
# '''
#
#
# def face_detection(video_file, original_candidate, x, y, w, h):
#     # Open the input movie file
#     input_video = cv2.VideoCapture(video_file)
#     length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
#
#     # Initialize some variables
#     face_locations = list()
#     fps = round(input_video.get(cv2.CAP_PROP_FPS))
#     section = 5
#     Checklist_withchat = Change_timeunit(
#         list(original_candidate.keys()), section)
#     Output_Dict = dict()
#
#     while input_video.isOpened():
#         # Grab a single frame of video
#         ret, frame = input_video.read()
#         # time = input_video.get(cv2.CAP_PROP_POS_MSEC)
#         index = input_video.get(cv2.CAP_PROP_POS_FRAMES)
#
#         # print('frames: %d   ---   times: %f' % (index, time/1000))
#
#         if frame is None:
#             break
#
#         # Quit when the input video file ends
#         if not ret:
#             break
#
#         # Check each sec if it is in the Checklist
#         if (index/fps) not in set(Checklist_withchat):
#             continue
#
#         # TODO Check if this one is necessary
#         # Resize frame of video to 1/4 size for faster face detection processing
#         frame = frame[y:y+h, x:x+w]
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
#         ''' If we need face recognition '''
#         # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#         # rgb_frame = frame[:, :, ::-1]
#
#         # Find all the faces in the frame
#         face_locations = face_recognition.face_locations(small_frame)
#
#         ''' If CNN is possible '''
#         # face_locations = face_recognition.face_locations(small_frame, model="cnn")
#
#         # Execute only face is detected
#         if face_locations:
#
#             ''' Face Detection '''
#             # We assume there is only one face in the image
#             for face_location in face_locations:
#                 top, right, bottom, left = face_location
#                 location = [top, left, right-left, bottom-top]
#
#             for key, value in Checklist_withchat.items():
#
#                 if (index/fps) in value:
#
#                     idx = value.index((index/fps))
#
#                     # Add score value calculated by mememoji
#                     # TODO mememoji <== location and make the image as 48x48
#                     # Get scores
#
#                     Checklist_withchat[key][idx] = 5
#                     #timestamp = time.strftime('%H:%M:%S', time.gmtime(index/fps))
#                     #Output_Dict[small_frame] = location
#
#         else:
#             continue
#     print(Checklist_withchat)
#     # Sum up
#     for key , value in Checklist_withchat.items():
#         print(key)
#         sumValue = 0
#         for eachValue in value:
#            sumValue += eachValue
#         Output_Dict[key] = sumValue / section # normalizing
#
#     print(Output_Dict)
#     # All done!
#     input_video.release()
#     cv2.destroyAllWindows()
#
#     return Output_Dict
#
#
# def Change_timeunit(time_list, section):
#     output = dict()
#     for eachtime in time_list:
#         sectioned_list = list()
#         int_timelist = eachtime.split(":")
#         for frame in range(section):
#             temp_result = (int(int_timelist[0]) * 3600) + \
#                 (int(int_timelist[1]) * 60) + \
#                 (int(int_timelist[2]))
#             sectioned_list.append(temp_result)
#             int_timelist[2] = int(int_timelist[2]) + 1
#         output[sectioned_list[0]] = sectioned_list
#
#     return output
#
# # location = [top, left, right-left, bottom-top]
# # Mememoji will return a score
#
#
# def mememoji_scoring(location):
#     pass
