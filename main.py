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
    
    background_path = "subway.mp4"  # Make sure this exists!
    output_path = "output.mp4"
    create_video(script, audio, background_path, output_path)
    print("✅ Done!")

if __name__ == "__main__":
    main()
