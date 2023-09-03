import os
import webbrowser
from datetime import datetime
import json
import os
import msal
import requests
from upload_file_to_one_drive import generate_access_token,GRAPH_API_ENDPOINT,APPLICATION_ID,SCOPES,upload_file,get_drive_files,list_files_in_folder


def list_files_in_folder(folder_path):
    file_paths = []

    # Walk through the directory tree using os.walk
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Join the root path with the filename to get the full file path
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    return file_paths



# Function to upload a file to OneDrive
def upload_file_to_particular_folder(access_token,file_path,file_name,folder_name):
    try:
        with open(file_path, 'rb') as file:
            headers={'Authorization':'Bearer '+access_token['access_token']}

            #file_name = file.filename

            response=requests.put(
                GRAPH_API_ENDPOINT+f'/me/drive/items/root:/{folder_name}/{file_name}:/content',
                headers=headers,
                data=file.read()
            )

            print(response.json())

            
            if response.status_code == 201 or response.status_code == 200:
                print(f"File {file_name} uploaded successfully.")
            else:
                print(f"File upload failed. Status code: {response.status_code}")

            return response.json()
    except Exception as e:
        print(f"Error generating get_drive_files: {str(e)}")




if __name__ == "__main__":
    folder_path = 'C:\Workspace\WestUrbanProjects'
    access_token=generate_access_token(APPLICATION_ID,SCOPES)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = list_files_in_folder(folder_path)
        for file in files:

            print(file.split("\\")[-2],file.split("\\")[-1],file)
            upload_file_to_particular_folder(access_token,file,file.split("\\")[-1],file.split("\\")[-2])

    else:
        print(f"The folder '{folder_path}' does not exist.")







