from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    VIDEO_SIZE = (1080, 1920)
    TARGET_DURATION = 60  # 1 minute in seconds

    # Load the background video, resize, set duration
    clip = VideoFileClip(background_path).resize(VIDEO_SIZE).subclip(0, TARGET_DURATION)

    # Wrap script to fit on screen (optional, for nicer look)
    import textwrap
    wrapped_script = "\n".join(textwrap.wrap(script, width=40))

    # Create a text clip that lasts the full minute
    txt = TextClip(
        wrapped_script,
        fontsize=60,
        color='white',
        size=(clip.size[0] - 100, clip.size[1] // 3),
        font="DejaVu-Sans",
        method='caption',
        align='center'
    ).set_position(('center', 'bottom')).set_duration(TARGET_DURATION)

    # Load audio and make it exactly 1 min (pad or trim)
    audio = AudioFileClip(audio_path)
    if audio.duration < TARGET_DURATION:
        from moviepy.audio.AudioClip import concatenate_audioclips, AudioClip
        silence = AudioClip(lambda t: 0, duration=TARGET_DURATION - audio.duration)
        final_audio = concatenate_audioclips([audio, silence])
    else:
        final_audio = audio.subclip(0, TARGET_DURATION)

    # Compose video
    video = CompositeVideoClip([clip, txt]).set_audio(final_audio).set_duration(TARGET_DURATION)

    # Write video
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)
    print(f"✅ Video saved as {output_path}")

# Example usage:
# create_video("Your script here.", "audio.mp3")
