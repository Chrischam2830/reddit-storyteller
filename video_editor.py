import os
import requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import loop

def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None

    # Look for the confirm token (for big files)
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def ensure_subway_video():
    if not os.path.exists("subway.mp4"):
        print("⏬ Downloading subway.mp4 from Google Drive (with confirm token support)...")
        file_id = "1IBRp3tl-dc1sJQlB0md5OZMmt4WCwMrF"   # <--- THIS IS YOUR NEW FILE ID!
        download_file_from_google_drive(file_id, "subway.mp4")
        print("✅ subway.mp4 downloaded.")

def create_video(script, voice_path, output_path="output.mp4"):
    ensure_subway_video()  # ✅ Make sure the background video exists

    print("🎬 Creating video...")

    # Load and loop video to at least 60 seconds
    base_clip = VideoFileClip("subway.mp4")
    clip = loop(base_clip, duration=60).resize(width=1080)

    audio = AudioFileClip(voice_path)

    # Create text overlay
    txt = TextClip(script, fontsize=48, color="white", size=clip.size, method="caption")
    txt = txt.set_duration(clip.duration)

    # Combine video + text + audio
    final = CompositeVideoClip([clip, txt.set_pos("center")])
    final = final.set_audio(audio)

    # Export the final video
    final.write_videofile(output_path, fps=24)
