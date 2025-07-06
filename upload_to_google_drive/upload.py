from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


class GoogleDriveUploader:

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.SERVICE_ACCOUNT_FILE = 'service_account.json'

    def authenticate(self):
        """Handles the authentication using service account."""
        if not os.path.exists(self.SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(
                f"{self.SERVICE_ACCOUNT_FILE} not found. Please download it from Google Cloud Console."
            )

        credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        return build('drive', 'v3', credentials=credentials)

    def find_and_delete_existing_file(self,
                                      service,
                                      file_name,
                                      parent_folder_id=None):
        """
        Finds and deletes a file with the same name in the specified folder.
        
        Args:
            service: Google Drive service instance
            file_name (str): Name of the file to find
            parent_folder_id (str, optional): ID of the parent folder to search in
        """
        query = f"name = '{file_name}' and trashed = false"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        results = service.files().list(q=query,
                                       spaces='drive',
                                       fields='files(id, name)').execute()
        files = results.get('files', [])

        for file in files:
            print(
                f"Found existing file '{file['name']}' with ID: {file['id']}. Deleting..."
            )
            service.files().delete(fileId=file['id']).execute()
            print(f"Deleted existing file: {file['name']}")

    def upload_file(self, file_path, parent_folder_id=None):
        """
        Uploads a file to Google Drive. If a file with the same name exists, it will be overwritten.
        
        Args:
            file_path (str): Path to the file to upload
            parent_folder_id (str, optional): ID of the parent folder in Google Drive.
                                            If None, uploads to root of service account's Drive.
        
        Returns:
            dict: Response from the upload request containing file ID and other metadata
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            service = self.authenticate()
            file_name = os.path.basename(file_path)

            # Delete existing file with the same name if it exists
            self.find_and_delete_existing_file(service, file_name,
                                               parent_folder_id)

            file_metadata = {'name': file_name}
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            media = MediaFileUpload(file_path, resumable=True)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink').execute()

            print(f"File uploaded successfully!")
            print(f"File name: {file.get('name')}")
            print(f"File ID: {file.get('id')}")
            print(f"Web view link: {file.get('webViewLink')}")

            return file

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


def main():
    uploader = GoogleDriveUploader()

    # Configure these values for your deployment
    file_path = "sisc_user_data.csv"
    folder_id = "1Uqus6BoaRfANkQoyiwob6wgX0zqOW2-_"

    if not folder_id:
        folder_id = None

    uploader.upload_file(file_path, folder_id)


if __name__ == "__main__":
    main()
