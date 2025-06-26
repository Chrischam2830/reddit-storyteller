from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def create_video(script, voice_path, output_path="output.mp4"):
    clip = VideoFileClip("subway.mp4").subclip(0, 60).resize(width=1080)
    txt = TextClip(script, fontsize=48, color="white", size=clip.size, method="caption")
    txt = txt.with_duration(clip.duration)
    final = CompositeVideoClip([clip, txt.set_pos("center")])
    final.write_videofile(output_path, audio=voice_path, fps=24)
import os
import requests

def ensure_subway_video():
    if not os.path.exists("subway.mp4"):
        print("⏬ Downloading subway.mp4 from Google Drive...")
        file_id = "1B3PXzOhvVlWJWfScZr8sSj4bLT5G7HXA"
        url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(url)
        if response.status_code == 200:
            with open("subway.mp4", "wb") as f:
                f.write(response.content)
        else:
            raise Exception("Failed to download subway.mp4")
