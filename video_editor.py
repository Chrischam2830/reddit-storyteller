from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_video(script, audio_path, background_path='subway.mp4', output_path='output.mp4'):
    VIDEO_SIZE = (1080, 1920)
    TARGET_DURATION = 60

    clip = VideoFileClip(background_path).resize(VIDEO_SIZE).subclip(0, TARGET_DURATION)
    wrapped_script = "\n".join(textwrap.wrap(script, width=40))

    # === PIL image workaround ===
    img_width, img_height = clip.size[0] - 100, 300
    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 60)
    except:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    draw.multiline_text(
        (img_width // 2, 20),
        wrapped_script,
        font=font,
        fill="white",
        anchor="ma",  # center align
        align="center"
    )
    img.save("/tmp/tmp_text_overlay.png")
    txt_clip = ImageClip("/tmp/tmp_text_overlay.png").set_position(('center', 'bottom')).set_duration(TARGET_DURATION)

    # Audio padding logic (unchanged)
    audio = AudioFileClip(audio_path)
    if audio.duration < TARGET_DURATION:
        from moviepy.audio.AudioClip import concatenate_audioclips, AudioClip
        silence = AudioClip(lambda t: 0, duration=TARGET_DURATION - audio.duration).set_fps(audio.fps)
        final_audio = concatenate_audioclips([audio, silence])
    else:
        final_audio = audio.subclip(0, TARGET_DURATION)

    video = CompositeVideoClip([clip, txt_clip]).set_audio(final_audio).set_duration(TARGET_DURATION)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=clip.fps)
    print(f"✅ Video saved as {output_path}")

# Example usage:
# create_video("Your script here.", "audio.mp3")
