import pandas as pd
import json
from datetime import datetime as dt
import numpy as np
import os
# Function to format datetime
def format_datetime(input_datetime):
    try:
        # Attempt to parse with fractional seconds and 'Z' for UTC time zone
        parsed_datetime = dt.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        try:
            # Try parsing without fractional seconds
            parsed_datetime = dt.strptime(input_datetime, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return "Invalid datetime format"
    
    formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
    return formatted_datetime


def extract_user_display_name(data_dict):
    display_name = data_dict.get("user", {}).get("displayName")
    return display_name
    
def format_file_size(file_size_bytes):
    kb = file_size_bytes / 1024
    mb = kb / 1024
    if mb < 1:
        return f"{kb:.2f} KB"
    else:
        return f"{mb:.2f} MB"

# Function to extract mimeType or return "folder" based on conditions
def extract_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension[1:] if extension else "Folder"


def extract_data_from_excel(df):
    
    df=df[['createdDateTime', 'lastModifiedDateTime', 'name', 'size', 'webUrl','createdBy', 'lastModifiedBy', 'folder', 'specialFolder', 'file']]

    # Apply the formatting function to the 'timestamp' column
    df['createdDateTime'] = df['createdDateTime'].apply(format_datetime)
    df['lastModifiedDateTime'] = df['lastModifiedDateTime'].apply(format_datetime)


    df['user_display_name'] = df['createdBy'].apply(extract_user_display_name)
    
    # Apply the extraction function to the 'data' column
    df['file_type'] = df['name'].apply(extract_extension)
    df['size'] = df['size'].apply(format_file_size)

    df=df[['createdDateTime', 'lastModifiedDateTime', 'name', 'size', 'webUrl', 'user_display_name', 'file_type']]
    sorted_df = df.sort_values(by='lastModifiedDateTime', ascending=False)
    return sorted_df


def modify_dataframe(response):

    #save to database
    # Create a DataFrame from the database
    df = pd.DataFrame(response)
    print(df.iloc[1].tolist())

    df=extract_data_from_excel(df)

    # Save the DataFrame to an Excel file
    excel_file = 'excelfiles/data.xlsx'
    df.to_excel(excel_file, index=False, engine='openpyxl')

    return df