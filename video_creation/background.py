from random import randrange
from pytube import YouTube
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from utils.console import print_step, print_substep


def get_start_and_end_times(video_length, length_of_clip):

    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length

# select a random video between https://www.youtube.com/watch?v=O3vaDxi7gio and https://www.youtube.com/watch?v=KXQVB2AHeTg&ab_channel=GroMan%E2%96%BAPlay
videos = [
    "https://www.youtube.com/watch?v=KXQVB2AHeTg&ab_channel=GroMan%E2%96%BAPlay"
]
video = videos[randrange(0, len(videos))]

def download_background():
    if not Path("assets/mp4/background2.mp4").is_file():
        print_step(
            "We need to download the Minecraft background video. This is fairly large but it's only done once. 😎"
        )
        print_substep("Downloading the background video... please be patient 🙏")
        YouTube(video).streams.filter(
            res="720p"
        ).first().download(
            "assets/mp4",
            filename="background2.mp4",
        )
        print_substep("Background video downloaded successfully! 🎉", style="bold green")


def chop_background_video(video_length):
    print_step("Finding a spot in the background video to chop...✂️")
    background = VideoFileClip("assets/mp4/background2.mp4")

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    ffmpeg_extract_subclip(
        "assets/mp4/background2.mp4",
        start_time,
        end_time,
        targetname="assets/mp4/clip.mp4",
    )
    print_substep("Background video chopped successfully! 🎉", style="bold green")
