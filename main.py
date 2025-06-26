import os
from reddit_fetcher import fetch_top_post
from story_rewriter import rewrite_story
from tts_generator import generate_voiceover
from video_editor import create_video
from utils import load_config

CONFIG = load_config("config.yaml")

def main():
    print("[1] Fetching Reddit post...")
    post = fetch_top_post(CONFIG)

    print("[2] Rewriting story with GPT...")
    script_text = rewrite_story(post['title'], post['body'], CONFIG)

    print("[3] Generating voiceover using ElevenLabs...")
    audio_path = generate_voiceover(script_text, CONFIG)

    print("[4] Creating vertical video with gameplay footage...")
    video_path = create_video(audio_path, script_text, CONFIG)

    print(f"✅ Video created and saved locally at: {video_path}")

if __name__ == "__main__":
    main()
    main()
