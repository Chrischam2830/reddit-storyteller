from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    # Load the background video
    clip = VideoFileClip(background_path)

    # Create a text clip (fix: specify a common font that is installed)
    txt = TextClip(
        script,
        fontsize=48,
        color='white',
        size=clip.size,
        font="DejaVu-Sans",  # "DejaVu-Sans" is installed by Dockerfile!
        method='caption'
    ).set_position('center').set_duration(clip.duration)

    # Load the audio
    audio = AudioFileClip(audio_path)

    # Set audio duration to match video if necessary
    final_audio = audio.subclip(0, min(audio.duration, clip.duration))

    # Combine everything
    video = CompositeVideoClip([clip, txt])
    video = video.set_audio(final_audio)
    video = video.set_duration(min(clip.duration, final_audio.duration))

    # Write the result to a file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)

    print(f"✅ Video saved as {output_path}")

# EXAMPLE USAGE
# create_video("This is a test script", "audio.mp3")
