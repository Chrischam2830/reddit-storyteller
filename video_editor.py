from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def create_video(audio_path, script_text, config):
    background = VideoFileClip("gameplay.mp4").subclip(0, 60).resize((1080, 1920))
    audio = AudioFileClip(audio_path)
    text = TextClip(script_text, fontsize=40, color='white', size=(1000, 1600), method='caption').set_duration(audio.duration).set_position('center')
    video = CompositeVideoClip([background.set_audio(audio), text])
    output_path = "final_video.mp4"
    video.write_videofile(output_path, fps=24)
    return output_path
