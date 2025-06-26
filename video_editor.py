from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def create_video(script, voice_path, output_path="output.mp4"):
    clip = VideoFileClip("subway.mp4").subclip(0, 60).resize(width=1080)
    txt = TextClip(script, fontsize=48, color="white", size=clip.size, method="caption")
    txt = txt.with_duration(clip.duration)
    final = CompositeVideoClip([clip, txt.set_pos("center")])
    final.write_videofile(output_path, audio=voice_path, fps=24)
