from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from dotenv import load_dotenv

# Load environment variables from .env file
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

    # Replace 'YourFolderName' with the actual name of the folder you're searching for
    folder_name = input("Enter folder name: ")
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name)",
        q="mimeType='application/vnd.google-apps.folder' and name = '{}' and trashed = false".format(folder_name)
    ).execute()
    items = results.get('files', [])

    if not items:
        print('No folders found with the name "{}".'.format(folder_name))
    else:
        print('Folders named "{}":'.format(folder_name))
        for item in items:
            print(u'{0} (ID: {1})'.format(item['name'], item['id']))
            # Save folder ID to .env file
            with open('.env', 'a') as env_file:
                env_file.write(f"\nFOLDER_ID={item['id']}")

if __name__ == '__main__':
    main()
