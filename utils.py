import os

def load_config():
    return {
        "reddit": {
            "client_id": os.getenv("REDDIT_CLIENT_ID"),
            "client_secret": os.getenv("REDDIT_SECRET"),
            "username": os.getenv("REDDIT_USERNAME"),
            "password": os.getenv("REDDIT_PASSWORD"),
            "user_agent": os.getenv("REDDIT_USER_AGENT"),
            "subreddits": [s.strip() for s in os.getenv("REDDIT_SUBREDDITS", "AskReddit").split(",")]
        },
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "organization": os.getenv("OPENAI_ORGANIZATION")
        },
        "elevenlabs": {
            "api_key": os.getenv("ELEVEN_API_KEY"),
            "voice_id": os.getenv("ELEVEN_VOICE_ID")
        }
    }
