from google.oauth2 import service_account
from googleapiclient.discovery import build
import sys

# Service account key path
SERVICE_ACCOUNT_FILE = './service_account.json'

# Use full drive access for deletion
SCOPES = ['https://www.googleapis.com/auth/drive']


def initialize_service():
    """Initialize and return the Google Drive service."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)


def list_files(service):
    """List all files owned by the service account."""
    files_to_delete = []
    page_token = None

    while True:
        response = service.files().list(
            pageSize=100,
            fields="nextPageToken, files(id, name, size, mimeType)",
            pageToken=page_token).execute()

        files = response.get('files', [])

        for file in files:
            name = file.get('name')
            size = int(file.get('size', 0))  # size in bytes
            mime = file.get('mimeType')
            file_id = file.get('id')
            files_to_delete.append({
                'id': file_id,
                'name': name,
                'size': size,
                'mimeType': mime
            })
            print(f"{name} - {size / (1024**2):.2f} MB - {mime}")

        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

    return files_to_delete


def delete_files(service, files):
    """Delete the specified files."""
    total_deleted = 0
    total_size_deleted = 0

    for file in files:
        try:
            service.files().delete(fileId=file['id']).execute()
            print(f"✓ Deleted: {file['name']}")
            total_deleted += 1
            total_size_deleted += file['size']
        except Exception as e:
            print(f"✗ Failed to delete {file['name']}: {str(e)}")

    return total_deleted, total_size_deleted


def main():
    try:
        service = initialize_service()
    except Exception as e:
        print(f"Failed to initialize service: {str(e)}")
        sys.exit(1)

    print("Listing files owned by the service account...\n")
    files_to_delete = list_files(service)

    if not files_to_delete:
        print("\nNo files found to delete.")
        return

    total_size = sum(file['size'] for file in files_to_delete)
    print(
        f"\nFound {len(files_to_delete)} files using {total_size / (1024**2):.2f} MB"
    )

    # Ask for confirmation
    confirmation = input(
        "\n⚠️  Are you sure you want to delete these files? This action cannot be undone! (yes/no): "
    )
    if confirmation.lower() != 'yes':
        print("Operation cancelled.")
        return

    print("\nDeleting files...")
    total_deleted, total_size_deleted = delete_files(service, files_to_delete)

    print(
        f"\n✅ Successfully deleted {total_deleted} files ({total_size_deleted / (1024**2):.2f} MB)"
    )


if __name__ == "__main__":
    main()
