from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import os.path
import pickle

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

    folder_id = '1405ZtnKdWPrRXCd1Z3zFhLT7wtnnFKt6'  # ID of the 'backup' folder in Drive
    local_folder_path = '/usr/src/app/files/'  # Path to the local backup folder

    # Get all files in the Drive folder
    query = f"'{folder_id}' in parents"
    response = service.files().list(q=query, spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute()
    drive_files = {file['name']: file['id'] for file in response.get('files', [])}

    # Delete all files in the Drive folder
    for file_name, file_id in drive_files.items():
        service.files().delete(fileId=file_id).execute()
        print(f'Deleted file: {file_name} (ID: {file_id})')

    # Upload new files from the local folder
    for local_file in os.listdir(local_folder_path):
        local_file_path = os.path.join(local_folder_path, local_file)
        if os.path.isfile(local_file_path):
            file_metadata = {
                'name': local_file,
                'parents': [folder_id]
            }
            media = MediaFileUpload(local_file_path)
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
            print(f'Uploaded file: {local_file} (ID: {file["id"]})')

if __name__ == '__main__':
    main()
