import praw
import random

def fetch_top_post(config):
    reddit = praw.Reddit(
        client_id=config["reddit"]["client_id"],
        client_secret=config["reddit"]["client_secret"],
        username=config["reddit"]["username"],
        password=config["reddit"]["password"],
        user_agent=config["reddit"]["user_agent"],
    )

    subs = config["reddit"]["subreddits"]
    random.shuffle(subs)

    for sub in subs:
        for submission in reddit.subreddit(sub).hot(limit=20):
            if not submission.stickied and submission.selftext and len(submission.selftext) > 100:
                return {"title": submission.title, "body": submission.selftext}

    raise Exception("No suitable post found.")
