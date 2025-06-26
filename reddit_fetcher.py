import praw

def fetch_top_post(config):
    reddit = praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent'],
        username=config['reddit']['username'],
        password=config['reddit']['password']
    )
    subreddit = reddit.subreddit(config['reddit']['subreddit'])
    for submission in subreddit.hot(limit=10):
        if not submission.stickied and len(submission.selftext) > 100:
            return {'title': submission.title, 'body': submission.selftext}
    raise Exception("No suitable post found.")
