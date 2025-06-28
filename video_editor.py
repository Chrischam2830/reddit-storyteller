from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    # Fixed video size
    VIDEO_SIZE = (1080, 1920)

    # Load the background video and resize to 1080x1920 if needed
    clip = VideoFileClip(background_path).resize(VIDEO_SIZE)

    # Limit the amount of text per screen
    # For vertical, 8-12 lines fits best. We'll wrap at 40 chars per line.
    import textwrap
    wrapped_script = "\n".join(textwrap.wrap(script, width=40))

    # Make the text clip (with a reasonable box, font, and method)
    txt = TextClip(
        wrapped_script,
        fontsize=60,
        color='white',
        size=(clip.size[0] - 100, clip.size[1] // 3),
        font="DejaVu-Sans",   # Installed in Docker!
        method='caption',
        align='center'
    ).set_position(('center', 'bottom')).set_duration(clip.duration)

    # Load and trim the audio if needed
    audio = AudioFileClip(audio_path)
    final_audio = audio.subclip(0, min(audio.duration, clip.duration))

    # Combine everything
    video = CompositeVideoClip([clip, txt]).set_audio(final_audio)
    video = video.set_duration(min(clip.duration, final_audio.duration))

    # Export
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)
    print(f"✅ Video saved as {output_path}")

# Example usage:
# create_video("Short example script.", "audio.mp3")
