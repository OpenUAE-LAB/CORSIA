from flask import Flask, render_template, request, jsonify, redirect, Response, send_file
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
# from bson import Binary
# from openpyxl import Workbook, load_workbook
import pandas as pd
import os
import time
import shutil
# from flask_ngrok import run_with_ngrok
from Validation import excel_validation
from xlsxwriter import workbook
import datetime
# import zipfile


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'ACOE@4123'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/success')
def upload_sucess():
    return render_template('success.html')

@app.route('/admin-history')
def admin_history():
    return render_template('admin-history.html')

@app.route('/success_admin')
def upload_sucess_admin():
    return render_template('success_admin.html')

@app.route('/processing')
def process():
    return render_template('processing.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/file_info')
def retrieve_file_info():
    # File name, size and upload time are retrieved and sent
    files_dict = {}
    operators_path = r'my_app/tmp/'
    files = os.listdir(operators_path)
    for file in files:
        if ".xlsx" in file.lower():
            file_path = r'my_app/tmp/' + file.title()
            data = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            # print(data.time())
            files_dict[f'{file.title()}'] = {
                "size" : os.path.getsize(file_path),
                "upload_date" : data.strftime('%m/%d/%Y'),
                "upload_time" : data.time().strftime('%H:%M'),
            }

    return jsonify(files_dict)

# Enables admin to download the aggregation file
@app.route('/download_combined', methods = ['GET'])
def combined_file_download():
    if request.method == 'GET':
        file_path = 'output/Combined.csv'
        return send_file(file_path, as_attachment=True)


# Enables admin to download individual files
@app.route('/delete_file/<filename>', methods = ['GET'])
def file_delete(filename):
    if request.method == 'GET':
        file_path = 'my_app/tmp/'+str(filename)+'.xlsx'
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            return "The file does not exist"
        return render_template('admin.html')

# Enables admin to delete the uploaded files from the system
@app.route('/download_file/<filename>', methods = ['GET'])
def file_download(filename):
    if request.method == 'GET':
        file_path = 'tmp/'+str(filename)+'.xlsx'
        return send_file(file_path, as_attachment=True)

# Enables admin to download all currently uploaded files
@app.route("/download_files", methods = ['GET'])
def files_download():
    if request.method == 'GET':
        shutil.make_archive('uploaded_files', format='zip', root_dir='my_app/tmp')
        files_path = '../uploaded_files.zip'
        return send_file(files_path, as_attachment=True)


# This is where the application uploads the files to the my_app/tmp/ folder after it confirms they are valid
@app.route('/uploader', methods = ['GET', 'POST', 'PUT'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      file_path = "my_app/tmp/"+f.filename
      f.save(file_path)
      err_dict = excel_validation(file_path)
    #   print(err_dict)
      return err_dict
    elif request.method == 'GET':
        return 'file is ready'

@app.route('/validate_response', methods=["GET"])
def validate_response():
    return render_template('validate_response.html')

@app.route('/validate', methods=["GET"])
def validate():
    return render_template('validate.html')

@app.route('/upload', methods=["GET"])
def upload():
    return render_template('upload.html')

@app.route("/get_combined", methods=["GET"])
def combine():
    # Extracting all the files in a path
    operators_path = r'my_app/tmp/'
    files = os.listdir(operators_path)
    file_names = []
    combined = pd.DataFrame()

    # Combining all the operaters flight data
    for file in files:
        if ".xlsx" in file:
            df = pd.read_excel(operators_path+file)
            file_names.append(file)
            combined = pd.concat([combined, df], ignore_index=True)

    # Converting all the countries names to lowercase for comparison
    combined["From"] = combined["From"].map(str.lower)
    combined["To"] = combined["To"].map(str.lower)

    # Adding CO2 emissions based on the destination and depature countries
    grouped = combined.groupby(["From", "To"]).sum()

    # Create a DataFrame from the list of file names
    file_names_df = pd.DataFrame(file_names, columns=["File Names"])

    # Write the aggregated data and the file names to an Excel file
    writer = pd.ExcelWriter(r'my_app/output/Combined.xlsx', engine='xlsxwriter')
    grouped.to_excel(writer, sheet_name='Aggregated Data', index=False)
    file_names_df.to_excel(writer, sheet_name='File Names', index=False)
    writer.close()

    # Converting the results to a csv and xlsx files
    # grouped.to_excel(r'my_app/output/Combined.xlsx')
    grouped.to_csv(r'my_app/output/Combined.csv')
    file_names_df.to_csv(r'my_app/output/Combined_File_Names.csv', index=False, header=True)
    return jsonify({"response": "successfully combined folders in the folder tmp"})

if __name__ == "__main__":
    app.run(debug=True)