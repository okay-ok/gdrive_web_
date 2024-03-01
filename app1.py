'''
import streamlit as st
import pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def save_to_drive(filename):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)

    file_drive = drive.CreateFile({'title': filename})
    file_drive.SetContentFile(filename)
    file_drive.Upload()
    print('Created file %s with mimeType %s' % (file_drive['title'], file_drive['mimeType']))

def app():
    st.title('Medical Record Upload')
    st.write("Please connect your Google account to upload files to Google Drive.")
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json") # Load previously saved credentials
    if gauth.credentials is None:
        st.warning("Please connect your Google account by clicking the button below.")
        if st.button("Connect Google Account"):
            gauth.LocalWebserverAuth() # Opens a new tab to authenticate the user
            gauth.SaveCredentialsFile("credentials.json") # Save the credentials for future use
            st.success("Google account connected successfully.")
    else:
        st.success("Google account already connected.")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        save_to_drive(uploaded_file.name)
        st.success('File uploaded to Google Drive')

if __name__ == '__main__':
    app()
    
    '''

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
