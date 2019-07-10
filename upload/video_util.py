from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2
import os

# videos_path = ["demo_video.mp4", "demo_video.mp4"]
# processed_file_name = "demodemo.mp4"


def concatenate_video(videos_path, processed_file_name):

    clips = []
    for path in videos_path:
        clips.append(VideoFileClip(path))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(processed_file_name)


def split_video(video_path, save_path, video_id, split_times):

    clip = VideoFileClip(video_path)
    video_list = []

    for split_time in split_times:
        title = os.path.join(save_path, str(video_id) + '_' + str(split_time[0]) + '_' + str(split_time[1]) + '.mp4')
        sub_clip = clip.subclip(split_time[0],split_time[1])

        print("writing... to ", title)
        sub_clip.write_videofile(title)
        video_list.append(title)

    return video_list


def get_video_length(clip):
    v = cv2.VideoCapture(clip)
    fps = v.get(cv2.CAP_PROP_FPS)
    total = v.get(cv2.CAP_PROP_FRAME_COUNT)
    return int(total/fps)


def cropVideo(inputFile, outputFile, x=100, y=200, w=200, h=300):

    # Read video
    video = cv2.VideoCapture(inputFile)
    fps = video.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    # In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2.(XVID is more preferable. MJPG results in high size video. X264 gives very small size video)
    # In Windows: DIVX(More to be tested and added)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # for mp4
    out = cv2.VideoWriter(outputFile, fourcc, fps, (w, h))

    while(video.isOpened()):
        ret, frame = video.read()
        if ret == True:
            frame = frame[y:y+h, x:x+w]
            cv2.imshow("", frame)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()
    return outputFile

# if __name__ == "__main__":
#     cropVideo(inputFile='Wildlife.wmv',
#               outputFile='result.mp4',
#               x=400,
#               y=100,
#               )


if __name__ == "__main__":
    # 비디어 합치기
    # concatenate_video(videos_path, processed_file_name)
    # 사용법 video를 합치는 경우 합치는 영상의 path를 리스트로 담아 넘김.
    videos_path = ["demo_video.mp4", "demo_video.mp4"]
    processed_file_name = "demodemo.mp4"
    concatenate_video(videos_path, processed_file_name)

    # 비디오 분할
    # 비디오는 하나의 파일에서 분할하므로
    # 하나의 video_path와
    # 여려개의 sub video들로 나뉠 수 있으므로
    # split time들을 담은 리스트를
    # 파라미터로 넘긴다.
    video_path = 'demo_video.mp4'
    split_times = [[0, 3], [10, 13], [20, 30]]
    split_video(video_path, split_times)
