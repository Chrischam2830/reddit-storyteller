import os
import requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def ensure_subway_video():
    if not os.path.exists("subway.mp4"):
        print("⏬ Downloading subway.mp4 from Google Drive...")
        file_id = "1B3PXzOhvVlWJWfScZr8sSj4bLT5G7HXA"  # Replace with your file ID
        url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(url)
        if response.status_code == 200:
            with open("subway.mp4", "wb") as f:
                f.write(response.content)
        else:
            raise Exception("Failed to download subway.mp4")

def create_video(script, voice_path, output_path="output.mp4"):
    ensure_subway_video()  # ✅ Make sure the background video exists

    print("🎬 Creating video...")

    # Load video and audio
    clip = VideoFileClip("subway.mp4").subclip(0, 60).resize(width=1080)
    audio = AudioFileClip(voice_path)

    # Create text overlay
    txt = TextClip(script, fontsize=48, color="white", size=clip.size, method="caption")
    txt = txt.set_duration(clip.duration)

    # Combine video + text + audio
    final = CompositeVideoClip([clip, txt.set_pos("center")])
    final = final.set_audio(audio)

    # Export the final video
    final.write_videofile(output_path, fps=24)
