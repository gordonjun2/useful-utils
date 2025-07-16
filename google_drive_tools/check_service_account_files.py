from google.oauth2 import service_account
from googleapiclient.discovery import build

# Service account key path
SERVICE_ACCOUNT_FILE = './service_account.json'

# Use full drive access
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

total_size = 0
page_token = None

print("Listing files owned by the service account...\n")

while True:
    response = service.files().list(
        pageSize=100,
        fields="nextPageToken, files(id, name, size, mimeType)",
        pageToken=page_token).execute()

    files = response.get('files', [])

    for file in files:
        name = file.get('name')
        size = int(file.get('size', 0))  # size is in bytes
        mime = file.get('mimeType')
        print(f"{name} - {size / (1024**2):.2f} MB - {mime}")
        total_size += size

    page_token = response.get('nextPageToken', None)
    if not page_token:
        break

print(
    f"\n✅ Total storage used by service account: {total_size / (1024**2):.2f} MB"
)
