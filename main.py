import os
import json
import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from utils import load_config
from reddit_fetcher import fetch_top_post
from story_rewriter import rewrite_story
from tts_generator import generate_voiceover
from video_editor import create_video

def upload_to_gdrive(local_file, drive_folder_id):
    print("UPLOAD FUNC: Starting upload_to_gdrive()")
    if not os.path.exists(local_file):
        print(f"[ERROR] File '{local_file}' does not exist! Skipping upload.")
        return
    try:
        sa_env_var = "GOOGLE_APPLICATION_CREDENTIALS_JSON"
        if sa_env_var not in os.environ:
            print(f"[ERROR] Env var '{sa_env_var}' not set! Upload cancelled.")
            return
        print("UPLOAD FUNC: Loading service account info")
        service_account_info = json.loads(os.environ[sa_env_var])
        print("UPLOAD FUNC: Loaded service account JSON.")
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        print("UPLOAD FUNC: Credentials created.")
        service = build('drive', 'v3', credentials=creds)
        print("UPLOAD FUNC: Built drive service.")
        file_metadata = {
            'name': os.path.basename(local_file),
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(local_file, mimetype='video/mp4')
        print("UPLOAD FUNC: Prepared MediaFileUpload.")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        print(f"UPLOAD FUNC: Uploaded to Google Drive: {file.get('webViewLink')}")
    except Exception as e:
        print("[ERROR] Upload failed:", str(e))
        traceback.print_exc()

def main():
    print("MAIN: Starting main()")
    config = load_config()
    print("MAIN: Loaded config")
    post = fetch_top_post(config)
    print("MAIN: Fetched top post")
    script = rewrite_story(post['title'], post['body'], config)
    print("MAIN: Rewrote story")
    audio = generate_voiceover(script, config)
    print("MAIN: Generated voiceover")
    
    background_path = "subway.mp4"
    output_path = "output.mp4"
    try:
        create_video(script, audio, background_path, output_path)
        print("MAIN: Done making video!")
    except Exception as e:
        print(f"[ERROR] create_video failed: {e}")
        traceback.print_exc()
        return  # Don't attempt upload if video failed

    # Check output exists before upload
    if os.path.exists(output_path):
        print("MAIN: Video file exists, ready to upload")
    else:
        print("MAIN: Video file does NOT exist! Skipping upload.")
        return

    # Upload to Google Drive
    drive_folder_id = "17YVgMsqt1AjKgh_Vz2m6Uc0Pk4lxDhKL"
    print("MAIN: Uploading to Google Drive...")
    upload_to_gdrive(output_path, drive_folder_id)
    print("MAIN: Finished upload_to_gdrive()")

if __name__ == "__main__":
    main()
