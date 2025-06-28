from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    # Load the background video
    clip = VideoFileClip(background_path)

    # Create a text clip with SAFE width AND height (max 80% of video width, 30% of video height)
    txt_width = int(clip.w * 0.8)
    txt_height = int(clip.h * 0.3)

    txt = TextClip(
        script,
        fontsize=48,
        color='white',
        font="DejaVu-Sans",
        method='caption',
        size=(txt_width, txt_height)  # Constrain both width AND height!
    ).set_position('center').set_duration(clip.duration)

    # Load the audio
    audio = AudioFileClip(audio_path)
    final_audio = audio.subclip(0, min(audio.duration, clip.duration))

    # Combine background and text
    video = CompositeVideoClip([clip, txt])
    video = video.set_audio(final_audio)
    video = video.set_duration(min(clip.duration, final_audio.duration))

    # Export final video
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)
    print(f"✅ Video saved as {output_path}")
