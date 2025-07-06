# Google Drive File Uploader

This Python script allows you to upload files to Google Drive using a service account for automated server deployment.

## Setup Instructions

1. Set up a Google Cloud Project and create a service account:

   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Drive API for your project
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Give it a name and description
   - Click "Create and Continue"
   - Click "Done"

2. Generate service account key:

   - In the Service Accounts list, find your service account
   - Click the three dots menu → "Manage keys"
   - Click "Add Key" → "Create new key"
   - Choose JSON format
   - Click "Create". The key file will download automatically
   - Rename the downloaded file to `service_account.json` and place it in the script directory

3. Grant Drive access:

   - If uploading to a shared drive or folder:
     - Open the target Google Drive folder in browser
     - Click "Share"
     - Add the service account email (found in `service_account.json`) and give it "Editor" access

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your `service_account.json` file in the same directory as the script
2. Modify the script parameters as needed:

   - `file_path`: Path to the file you want to upload
   - `folder_id`: ID of the target folder (found in the folder's URL)

3. Run the script:
   ```bash
   python upload.py
   ```

## Getting Folder ID

To upload to a specific folder:

1. Open the target Google Drive folder in your browser
2. The folder ID is in the URL: `https://drive.google.com/drive/folders/FOLDER_ID`

## Notes

- The service account has its own Drive space. To upload to a specific folder, you must share that folder with the service account's email
- The service account email can be found in the `service_account.json` file
- Make sure to keep your `service_account.json` secure and never commit it to version control
