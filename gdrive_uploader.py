import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_gdrive(file_path, drive_folder_id, service_account_path='gdrive_service_account.json'):
    # Authenticate using service account
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(
        service_account_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    # File metadata: Name and target folder
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [drive_folder_id]  # Folder ID in your Google Drive
    }
    media = MediaFileUpload(file_path, resumable=True)
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Uploaded to Google Drive! File ID: {uploaded.get('id')}")

# Example usage:
# upload_to_gdrive('output.mp4', 'YOUR_FOLDER_ID_HERE')
