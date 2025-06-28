from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    # Load the background video
    clip = VideoFileClip(background_path)

    # Create a text clip (use safe font, safe size)
    txt = TextClip(
        script,
        fontsize=48,
        color='white',
        size=(clip.w, int(clip.h * 0.25)),  # 25% of video height, same width as background
        font="DejaVu-Sans",                 # This font is installed in your Docker image!
        method='caption',
        align='center'
    ).set_position(('center', 'bottom')).set_duration(clip.duration)

    # Load the audio
    audio = AudioFileClip(audio_path)

    # Cut audio/video to the shortest length
    min_duration = min(audio.duration, clip.duration)
    final_audio = audio.subclip(0, min_duration)
    final_clip = clip.subclip(0, min_duration)

    # Combine everything
    video = CompositeVideoClip([final_clip, txt])
    video = video.set_audio(final_audio)
    video = video.set_duration(min_duration)

    # Write the result to a file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)

    print(f"✅ Video saved as {output_path}")

# Uncomment this and fill in the actual script/audio to test:
# create_video("This is a test script", "audio.mp3")
