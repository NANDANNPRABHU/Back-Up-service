from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

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
    
    results = service.files().list(

        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)",
        q="'1405ZtnKdWPrRXCd1Z3zFhLT7wtnnFKt6' in parents").execute()  # Adjusted query to exclude "Shared with Me"
    items = results.get('files', [])

    if not items:
        print('No files or folders found.')
    else:
        print('Files and Folders:')
        for item in items:
            itemType = "Folder" if item['mimeType'] == "application/vnd.google-apps.folder" else "File"
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], itemType))

if __name__ == '__main__':
    main()
