import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from utils import load_config
from reddit_fetcher import fetch_top_post
from story_rewriter import rewrite_story
from tts_generator import generate_voiceover
from video_editor import create_video

def upload_to_gdrive(local_file, drive_folder_id):
    service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': os.path.basename(local_file),
        'parents': [drive_folder_id]
    }
    media = MediaFileUpload(local_file, mimetype='video/mp4')
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,webViewLink'
    ).execute()
    print(f"Uploaded to Google Drive: {file.get('webViewLink')}")

def main():
    config = load_config()
    post = fetch_top_post(config)
    script = rewrite_story(post['title'], post['body'], config)
    audio = generate_voiceover(script, config)
    
    background_path = "subway.mp4"
    output_path = "output.mp4"
    create_video(script, audio, background_path, output_path)
    print("✅ Done making video!")

    # Upload to Google Drive
    drive_folder_id = "17YVgMsqt1AjKgh_Vz2m6Uc0Pk4lxDhKL"
    upload_to_gdrive(output_path, drive_folder_id)

if __name__ == "__main__":
    main()
