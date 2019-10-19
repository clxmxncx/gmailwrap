import pickle
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from urllib.error import HTTPError
from apiclient import errors
import email


# If modifying these scopes, delete the file token.pickle.
# https://developers.google.com/gmail/api/auth/scopes
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://mail.google.com/']

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


# ListMessagesMatchingQuery
# fonction récupérée sur :
# https://developers.google.com/gmail/api/v1/reference/users/messages/list
# et adaptée à python3

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                    q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                     pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)

def trash_message(service,user_id, msg_id):
    try:
        #for i in range(len(msg_ids)):
        service.users().messages().trash(userId=user_id, id=msg_id).execute()
        print ("Message with id: ", msg_id," trashed successfully.")
    except errors.HttpError as e:
        print ('An error occurred: ', e)



if __name__ == '__main__':

    # récuperation de l'objet service, permettant l'accès à l'API gmail
    service = get_gmail_service()

    # query = 'from:no-reply@dropbox.com'
    query = 'from:security@mail.instagram.com'
    messages = ListMessagesMatchingQuery(service, 'me', query=query)

    for m in messages:
        trash_message(service, 'me', m['id'])
