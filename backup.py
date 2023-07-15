import argparse
import datetime
import io
import os
import pickle
import re
import time
import zipfile
from shutil import rmtree
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def sanitize_filename(filename):
    filename = re.sub(r'[^\x00-\x7f]', r'', filename)  # remove non-ASCII characters
    filename = re.sub(r'[\\/:"*?<>|]+', r'', filename)  # remove illegal characters
    return filename.rstrip()  # remove trailing whitespace

def calculate_size(file_path):
    if os.path.isfile(file_path):
        return os.path.getsize(file_path) / (1024 ** 3)  # size in GB
    else:
        total_size = 0
        for path, dirs, files in os.walk(file_path):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
        return total_size / (1024 ** 3)  # size in GB

def send_email(subject, content, from_email, to_email, sendgrid_api_key):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
    except Exception as e:
        print(str(e))

def check_creds(client_json, from_email, to_email, sendgrid_api_key, token_path):
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            send_email("[Notification] New Token Needed", 
                       "<div style='background-color: yellow;'>Your Google Drive backup program requires a new authentication token. Please run the program manually to obtain a new token.</div>", 
                       from_email, to_email, sendgrid_api_key)
            flow = InstalledAppFlow.from_client_secrets_file(client_json, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def download_file(service, item, filepath):
    print(f"Downloading file {filepath}.")
    request = service.files().get_media(fileId=item['id'])
    fh = io.FileIO(filepath, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

def download_drive_data(service, download_folder, parent='root', path=''):
    skipped_files = []
    page_token = None
    while True:
        results = service.files().list(q=f"'{parent}' in parents",
                                       fields="nextPageToken, files(id, name, mimeType)",
                                       pageToken=page_token).execute()
        items = results.get('files', [])
        for item in items:
            filename = sanitize_filename(re.sub(r'[^\x00-\x7f]', r'', item['name']))
            folderpath = os.path.join(download_folder, path)
            os.makedirs(folderpath, exist_ok=True)
            filepath = os.path.join(folderpath, filename)
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                download_drive_data(service, download_folder, item['id'], os.path.join(path, filename))
            else:
                try:
                    download_file(service, item, filepath)
                except Exception as e:
                    print(f"Error downloading file {filepath}. Error: {str(e)}. Skipping this file.")
                    skipped_files.append(filepath)
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    return skipped_files

def zip_data(backup_folder, download_folder):
    print("Zipping process started.")
    zipf = zipfile.ZipFile(backup_folder + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(download_folder):
        for file in files:
            zipf.write(os.path.join(root, file), arcname=file)
    zipf.close()
    print("Zipping process ends.")
    return backup_folder + '.zip'

def delete_old_files(folder, retention_days):
    current_time = time.time()
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        file_creation_time = os.path.getmtime(file_path)
        if current_time - file_creation_time > retention_days * 24 * 60 * 60:
            if os.path.isfile(file_path):
                print(f"Deleting old file: {file_name}")
                os.remove(file_path)

def backup_drive(backup_folder, download_folder, from_email, to_email, sendgrid_api_key, client_json):
    token_path = os.path.join(os.path.dirname(download_folder), 'token.pickle')
    creds = check_creds(client_json, from_email, to_email, sendgrid_api_key, token_path)

    service = build('drive', 'v3', credentials=creds)
    try:
        send_email("[Starting] Google Drive backup started", 
                   "<div style='background-color: yellow;'>Your backup process has started.</div>", 
                   from_email, to_email, sendgrid_api_key)
        
        skipped_files = download_drive_data(service, download_folder)
        
        zip_file_path = zip_data(backup_folder, download_folder)
        size_after = calculate_size(zip_file_path)
        if len(skipped_files) > 0:
            send_email("[Success] Google Drive backup succeeded", 
                       f"<div style='background-color: green;'>Your backup was successful. The final backup size is {size_after:.2f} GB.</div><br>Following files were skipped:<br> {'<br>'.join(skipped_files)}", 
                       from_email, to_email, sendgrid_api_key)
        else:
            send_email("[Success] Google Drive backup succeeded", 
                       f"<div style='background-color: green;'>Your backup was successful. The final backup size is {size_after:.2f} GB.</div>", 
                       from_email, to_email, sendgrid_api_key)
    except Exception as e:
        send_email("[Failed] Google Drive backup failed", f"<div style='background-color: red;'>Your backup failed. Error: {str(e)}</div>", from_email, to_email, sendgrid_api_key)
    finally:
        for filename in os.listdir(download_folder):
            file_path = os.path.join(download_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--download_folder', required=True, help='Folder where files will be downloaded')
    parser.add_argument('--backup_folder', required=True, help='Folder where backup will be saved')
    parser.add_argument('--sendgrid_api_key', required=True, help='Your SendGrid API key')
    parser.add_argument('--from_email', required=True, help='Email to send notifications from')
    parser.add_argument('--to_email', required=True, help='Email to send notifications to')
    parser.add_argument('--client_json', required=True, help='Path to your Google client json')
    parser.add_argument('--hour', type=int, required=True, help='Hour to start the backup')
    parser.add_argument('--minute', type=int, required=True, help='Minute to start the backup')
    parser.add_argument('--retention_days', type=int, help='How many days to retain old files')

    args = parser.parse_args()

    DOWNLOAD_FOLDER = args.download_folder
    BACKUP_FOLDER = args.backup_folder
    SENDGRID_API_KEY = args.sendgrid_api_key
    FROM_EMAIL = args.from_email
    TO_EMAIL = args.to_email
    CLIENT_JSON = args.client_json
    HOUR = args.hour
    MINUTE = args.minute
    RETENTION_DAYS = args.retention_days

    while True:
        current_time = datetime.datetime.now()
        if (current_time.hour == HOUR and current_time.minute == MINUTE):
            print("Let's start")
            backup_drive(os.path.join(BACKUP_FOLDER, current_time.strftime("%Y-%m-%d_%H-%M-%S")), DOWNLOAD_FOLDER, FROM_EMAIL, TO_EMAIL, SENDGRID_API_KEY, CLIENT_JSON)
            print("Backup finished. Starting deleting old backups")
            delete_old_files(BACKUP_FOLDER, RETENTION_DAYS)
            print("Finishing deleting old backups. See ya tomorrow at ", HOUR, " ", MINUTE)
        time.sleep(10)
