from moviepy.editor import VideoFileClip, concatenate_videoclips

# videos_path = ["demo_video.mp4", "demo_video.mp4"]
# processed_file_name = "demodemo.mp4"
def concatenate_video(videos_path, processed_file_name):

    clips = []
    for path in videos_path:
        clips.append(VideoFileClip(path))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(processed_file_name)
   

def split_video(video_path, split_times):

    clip = VideoFileClip(video_path)

    for split_time in split_times:

        sub_clip = clip.subclip(split_time[0],split_time[1])
        write_path = str(split_time[0]) + '_' + str(split_time[1]) + '.mp4'

        print("writing... to ", write_path)
        sub_clip.write_videofile(write_path)
         

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
    #split time들을 담은 리스트를
    # 파라미터로 넘긴다. 
    video_path = 'demo_video.mp4'
    split_times = [[0,3],[10,13],[20,30]]
    split_video(video_path, split_times)
