import requests
import json

DROPBOX_API_BASE_URL = 'https://api.dropboxapi.com/2/files/list_folder'
access_token = ""  # Replace with your actual Dropbox access token

# Specify the folder path to list files from
folder_path = "/Hybrid_MG_Shared"  # Root folder or specify a folder path like "/MyFolder"

header = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Request body to specify folder path
data = {
    "path": folder_path,
    "recursive": False  # Set to True if you want to list all subfolders recursively
}

# Make the request to the Dropbox API to list the files
response = requests.post(
    url=DROPBOX_API_BASE_URL,
    headers=header,
    data=json.dumps(data)
)

# Parse the JSON response to get the file information
if response.status_code == 200:
    folder_contents = response.json()
    if 'entries' in folder_contents:
        if len(folder_contents['entries']) == 0:
            print("The folder is empty.")
        else:
            for entry in folder_contents['entries']:
                print(f"File/Folder Name: {entry['name']} | Type: {entry['.tag']}")
    else:
        print("No entries found in the folder.")
else:
    print(f"Failed to retrieve folder contents. Status Code: {response.status_code}")
    print(response.text)