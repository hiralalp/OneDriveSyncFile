import webbrowser
from datetime import datetime
import json
import os
import msal
import requests
from email_send import send_user_code_in_mail
from dataframeprocess import modify_dataframe


GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
APPLICATION_ID="23055c44-19e2-47b6-8c1f-5a72a5dc6b9d"
SCOPES=['Files.ReadWrite']

def generate_access_token(app_id, scopes):
    try:
        # Save Session Token as a token file
        access_token_cache = msal.SerializableTokenCache()

        # read the token file
        if os.path.exists('ms_graph_api_token.json'):
            access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
            token_detail = json.load(open('ms_graph_api_token.json',))
            token_detail_key = list(token_detail['AccessToken'].keys())[0]
            token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
            if datetime.now() > token_expiration:
                os.remove('ms_graph_api_token.json')
                access_token_cache = msal.SerializableTokenCache()

        # assign a SerializableTokenCache object to the client instance
        client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

        accounts = client.get_accounts()
        if accounts:
            # load the session
            token_response = client.acquire_token_silent(scopes, accounts[0])
        else:
            # authetnicate your accoutn as usual
            flow = client.initiate_device_flow(scopes=scopes)
            print('user_code: ' + flow['user_code'])
            send_user_code_in_mail(flow['user_code'])
            webbrowser.open('https://microsoft.com/devicelogin')
            token_response = client.acquire_token_by_device_flow(flow)

        with open('ms_graph_api_token.json', 'w') as _f:
            _f.write(access_token_cache.serialize())

        return token_response
    except Exception as e:
        print(f"Error generating access token: {str(e)}")



def get_drive_files(access_token):
    try:
        headers={'Authorization':'Bearer '+access_token['access_token']}
        #https://graph.microsoft.com/v1.0/me/drive/recent
        response=requests.get(
            GRAPH_API_ENDPOINT+f'/me/drive/root/children',
            headers=headers
        )

        print(response.json())


        if response.status_code == 201 or response.status_code == 200:
            print(f" successfully.")
        else:
            print(f" failed. Status code: {response.status_code}")

        df=modify_dataframe(response.json()['value'])

        return df
    except Exception as e:
        print(f"Error generating get_drive_files: {str(e)}")


# Function to upload a file to OneDrive
def upload_file(access_token,file):
    try:
        headers={'Authorization':'Bearer '+access_token['access_token']}

        file_name = file.filename

        response=requests.put(
            GRAPH_API_ENDPOINT+f'/me/drive/items/root:/{file_name}:/content',
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


