from utils import load_config
from reddit_fetcher import fetch_top_post
from story_rewriter import rewrite_story
from tts_generator import generate_voiceover
from video_editor import create_video

def main():
    config = load_config()
    post = fetch_top_post(config)
    script = rewrite_story(post['title'], post['body'], config)
    audio = generate_voiceover(script, config)
    create_video(script, audio)
    print("✅ Done!")

if __name__ == "__main__":
    main()
