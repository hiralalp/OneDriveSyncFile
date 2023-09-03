from flask import Flask, render_template, request, redirect, url_for,send_file
import requests
from upload_file_to_one_drive import generate_access_token,GRAPH_API_ENDPOINT,APPLICATION_ID,SCOPES,upload_file,get_drive_files,upload_file_to_particular_folder,list_files_in_folder
import pandas as pd
import json
from dataframeprocess import extract_data_from_excel,modify_dataframe
import os
app = Flask(__name__)

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    alert_message=None
    if request.method == 'POST':
        user_input = request.form['user_input']
        upload_file2(user_input)
        alert_message="OneDrive Sync Successfully"
        return render_template('index.html', alert_message=alert_message)

    return render_template('index.html', alert_message=alert_message)

@app.route('/database')
def get_database():
    access_token=generate_access_token(APPLICATION_ID,SCOPES)
    return render_template('database.html', df=get_drive_files(access_token))


@app.route('/download_excel')
def download_excel():
    filename = 'data.xlsx'
    excel_path = 'excelfiles/' + filename  
    return send_file(excel_path, as_attachment=True, download_name=filename)


def upload_file2(folder_path):
    access_token=generate_access_token(APPLICATION_ID,SCOPES)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = list_files_in_folder(folder_path)
        for file in files:

            print(file.split("\\")[-2],file.split("\\")[-1],file)
            upload_file_to_particular_folder(access_token,file,file.split("\\")[-1],file.split("\\")[-2])

    else:
        print(f"The folder '{folder_path}' does not exist.")

if __name__ == "__main__":
    app.run(debug=True)
