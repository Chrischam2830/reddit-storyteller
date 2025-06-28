from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    VIDEO_SIZE = (1080, 1920)
    TARGET_DURATION = 60  # 1 minute in seconds

    # Load the background video, resize, set duration
    clip = VideoFileClip(background_path).resize(VIDEO_SIZE).subclip(0, TARGET_DURATION)

    # Optional: Wrap script to fit on screen nicely
    import textwrap
    wrapped_script = "\n".join(textwrap.wrap(script, width=40))

    # Create a text clip using Pillow only (no ImageMagick needed)
    txt = TextClip(
        wrapped_script,
        fontsize=60,
        color='white',
        size=(clip.size[0] - 100, clip.size[1] // 3),
        font="DejaVu-Sans",        # Use 'DejaVu-Sans' for compatibility
        method='caption',          # <-- THIS uses Pillow, NOT ImageMagick
        align='center'
    ).set_position(('center', 'bottom')).set_duration(TARGET_DURATION)

    # Load audio and ensure it's exactly 1 minute (pad with silence if too short)
    audio = AudioFileClip(audio_path)
    if audio.duration < TARGET_DURATION:
        from moviepy.audio.AudioClip import concatenate_audioclips, AudioClip
        silence = AudioClip(lambda t: 0, duration=TARGET_DURATION - audio.duration)
        silence = silence.set_fps(audio.fps)  # match audio fps for compatibility
        final_audio = concatenate_audioclips([audio, silence])
    else:
        final_audio = audio.subclip(0, TARGET_DURATION)

    # Compose video with text and audio
    video = CompositeVideoClip([clip, txt]).set_audio(final_audio).set_duration(TARGET_DURATION)

    # Write video file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)
    print(f"✅ Video saved as {output_path}")

# Example usage:
# create_video("Your script here.", "audio.mp3")
