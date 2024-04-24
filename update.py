import os
import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv


load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    folder_id = os.getenv('FOLDER_ID')
    # folder_id = '1RniXadmT7FpyC1pSXlOa5ddy2vgW9pRH'
      # ID of the 'backup' folder in Drive
    local_folder_path = '/usr/src/app/files/'  # Path to the local backup folder

    # Check for changes and update if necessary
    if check_and_update(service, folder_id, local_folder_path):
        print("Updates were made based on the changes detected.")
    else:
        print("No changes detected. No updates made.")

def check_and_update(service, folder_id, local_folder_path):
    # Get all files in the Drive folder
    query = f"'{folder_id}' in parents"
    response = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    drive_files = {file['name']: file['id'] for file in response.get('files', [])}

    # Get all files in the local folder
    local_files = {f: None for f in os.listdir(local_folder_path) if os.path.isfile(os.path.join(local_folder_path, f))}

    # Determine changes: new files or deleted files
    new_files = local_files.keys() - drive_files.keys()
    deleted_files = drive_files.keys() - local_files.keys()

    # Delete files in Drive not present locally
    for file_name in deleted_files:
        service.files().delete(fileId=drive_files[file_name]).execute()
        print(f'Deleted file: {file_name} (ID: {drive_files[file_name]})')

    # Upload new files from local to Drive
    for file_name in new_files:
        local_file_path = os.path.join(local_folder_path, file_name)
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(local_file_path)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Uploaded file: {file_name} (ID: {file["id"]})')

    return bool(new_files or deleted_files)

if __name__ == '__main__':
    main()
