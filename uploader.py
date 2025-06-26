import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

def upload_to_youtube(video_path, title, config):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = None
    if os.path.exists(config['youtube']['credentials_file']):
        with open(config['youtube']['credentials_file'], "rb") as f:
            credentials = pickle.load(f)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(config['youtube']['client_secrets_file'], scopes)
        credentials = flow.run_console()
        with open(config['youtube']['credentials_file'], "wb") as f:
            pickle.dump(credentials, f)
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Generated with AI from Reddit",
                "tags": ["Reddit", "Story", "AI"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "madeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path)
    )
    request.execute()
