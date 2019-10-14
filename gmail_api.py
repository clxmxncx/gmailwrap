import pickle
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.text import MIMEText
import base64
from urllib.error import HTTPError

# If modifying these scopes, delete the file token.pickle.
# https://developers.google.com/gmail/api/auth/scopes
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = [
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.readonly'
]
# compose: Create, read, update, and delete drafts. Send messages and drafts.

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def get_gmail_service():
    current_directory = Path.cwd()
    credentials_json_file = current_directory / 'credentials.json'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = current_directory / 'token.pickle'

    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json_file,
                SCOPES
            )
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def print_labels():
    ''' from quickstart.py
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    '''
    service = get_gmail_service()
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
            #######
        return labels


def main():
    res = None

    return res

if __name__ == '__main__':
    # res = main()
    print_labels()
