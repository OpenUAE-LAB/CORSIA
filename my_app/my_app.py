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
# from Validation import excel_validation
# from xlsxwriter import workbook
import datetime
# import zipfile

import pandas as pd
import os
import time
"""
    Reads data from two excel files, performs some data validation and prints error messages
"""
# specify the file path

def excel_validation(file_path):
    err_dict = {}
    invalid = 0
    # file_path = "/Users/yasmeenelsalhy/Desktop/Mariame/MyApp/my_app/tmp/Operator1.xlsx"

    # Read the CSV file/xlsx file
    df = pd.read_excel(file_path)

    # Define the required column labels
    required_columns = ['From','To','CO2 Emissions (tonnes of CO2)']

    # Errors counter to differentiate
    err_counter = 0

    # Check if the required columns exist in the DataFrame
    if set(required_columns).issubset(df.columns):

        if df.shape[0] != 0:
            # print("All required columns exist in the CSV file.")
            # read the Excel file into a DataFrame
            df = pd.read_excel(file_path, usecols=['From','To','CO2 Emissions (tonnes of CO2)'])

            # create a list of tuples from the DataFrame
            data_list = [[str(mystring) for mystring in  x] for x in df.values]


            file2_path="my_app/countries list.xlsx"


            cf = pd.read_excel(file2_path, usecols=['countries'])
            countries_list=cf['countries'].tolist()

            countries_list=[i.strip().capitalize() for i in countries_list]
            # countries_list=[i.capitalize() for i in countries_list]

            for i, t in enumerate(data_list, start=2):
                if (t[0].strip()).capitalize() not in countries_list:
                    # print(f"error in line {i} in from {t[0]}")
                    # err_dict[f"error in line {i}, from column"] = f" {t[0]}"
                    err_dict[err_counter] = {
                        "line": f" {i}",
                        "column": "From",
                        "error": str(t[0]),
                    }
                    err_counter +=1
                    invalid = 1

                if (t[1].strip()).capitalize() not in countries_list:   
                    # print(f"error in line  {i} :to {t[1]}")
                    # err_dict[f"error in line {i}, to column"] = f" {t[1]}"
                    err_dict[err_counter] = {
                        "line": f" {i}",
                        "column": "To",
                        "error": str(t[1]),
                    }
                    err_counter +=1
                    invalid = 1

                if  t[2].isnumeric(): 
                    if(float(t[2])<=0 or t[2]=='nan'):
                        print(t[2])
                        # print(f"error in line  {i} :to {t[2]}")
                        # err_dict[f"error in line {i}, nan or less than 0"] = f" {t[2]}"
                        err_dict[err_counter] = {
                            "line": f" {i}",
                            "column": "CO2 Emissions",
                            "error": str(t[1]),
                        }
                        err_counter +=1
                        invalid = 1

                elif not t[2].isnumeric():
                    # print(f"error in line  {i} :to {t[2]}")
                    # err_dict[f"error in line {i}, not a number"] = f" {t[2]}"
                    err_dict[err_counter] = {
                        "line": f" {i}",
                        "column": "CO2 Emissions",
                        "error": f"{t[2]} not a number",
                    }
                    err_counter +=1
                    invalid = 1
            # row_count = len(data_list)
            # print("the number of rows in the data: ", row_count)
        else:
            # print("The CSV file has no data")
            # err_dict["Empty Error"] = " File has no data"
            err_dict[err_counter] = {
                "line": f"-",
                "column": "-",
                "error": "File is Empty",
                }
            err_counter += 1
            invalid = 1
    else:
        missing_columns = [col for col in required_columns if col not in df.columns]
        # print(f"The following columns are missing from the CSV file: {missing_columns}.")
        err_dict[err_counter] = {
            "line": f"Missing",
            "column": "Columns",
            "error": str(missing_columns),
            }
        err_counter += 1
        invalid = 1
    
    if invalid:
        os.remove(file_path)
    # print(err_dict)
    return err_dict




def create_app():
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

    # Display files for the admin-history page
    @app.route('/file_info_previously')
    def retrieve_file_info_previously():
        files_dict = {} 

        # Read all file in directory and convert to lower for comparison
        operators_path = r'my_app/tmp/'
        files = os.listdir(operators_path)
        files = [x.lower() for x in files]

        # Read list of files names combined previously and convert to lower for comparison
        aggregated_files_names_path = 'my_app/output/Combined_File_Names.csv'
        df = pd.read_csv(aggregated_files_names_path)
        files_list = df['File Names'].to_list()
        files_list = [x.lower() for x in files_list]

        # Constructing a dictionary with information on files to be displayed
        for file in files:
            if ".xlsx" in file:
                file_path = r'my_app/tmp/' + file
                data = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                if (file in files_list): # If file is previously aggregated --> Display
                    files_dict[f'{file.title()}'] = {
                        "size" : os.path.getsize(file_path),
                        "upload_date" : data.strftime('%m/%d/%Y'),
                        "upload_time" : data.time().strftime('%H:%M'),
                    }

        return jsonify(files_dict)

    # Display file info in admin page
    @app.route('/file_info')
    def retrieve_file_info():
        files_dict = {}

        # Read all file in directory and convert to lower for comparison
        operators_path = r'my_app/tmp/'
        files = os.listdir(operators_path)
        files = [x.lower() for x in files]

        # Read list of files names combined previously and convert to lower for comparison
        
        aggregated_files_names_path = 'my_app/output/Combined_File_Names.csv'
        if os.path.exists(aggregated_files_names_path):
            df = pd.read_csv(aggregated_files_names_path)
            files_list = df['File Names'].to_list()
            files_list = [x.lower() for x in files_list]
        else:
            files_list = []

        for file in files:
            if ".xlsx" in file.lower():
                file_path = r'my_app/tmp/' + file
                data = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                if (file not in files_list): # If file NOT previously aggregated --> Display
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
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("The file does not exist")
        return redirect('/admin')

    # Enables admin to delete the uploaded files from the system
    @app.route('/download_file/<filename>', methods = ['GET'])
    def file_download(filename):
        if request.method == 'GET':
            if '.xlsx' not in str(filename).lower():
                file_path = 'tmp/'+str(filename)+'.xlsx'
            else:
                file_path = 'tmp/'+str(filename)
            return send_file(file_path, as_attachment=True)

    # Enables admin to download all currently uploaded files
    @app.route('/download_files', methods = ['GET'])
    def files_download():
        if request.method == 'GET':
            shutil.make_archive('uploaded_files', format='zip', root_dir='my_app/tmp')
            files_path = '../uploaded_files.zip'
            return send_file(files_path, as_attachment=True)
        
    # Enables admin to download selected uploaded files
    @app.route('/download_files_selected', methods = ['GET'])
    def download_files_selected():
        if request.method == 'GET':
            shutil.make_archive('uploaded_files', format='zip', root_dir='my_app/tmp')
            files_path = '../uploaded_files.zip'
            return send_file(files_path, as_attachment=True)


    # This is where the application uploads the files to the my_app/tmp/ folder after it confirms they are valid
    @app.route('/uploader', methods = ['POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['file']
            file_path = "my_app/tmp/"+f.filename
            f.save(file_path)
        #     err_dict = excel_validation(file_path)
        #     print(err_dict)
        #     return err_dict
        return 'success'
        # elif request.method == 'GET':
        #     return 'file is ready'
        
    # @app.route('/uploader', methods = ['GET', 'POST'])
    # def upload_file():
    #     if request.method == 'POST':
    #         f = request.files['file']
    #         file_path = "my_app/tmp/"+f.filename
    #         f.save(file_path)
    #         err_dict = excel_validation(file_path)
    #         print(err_dict)
    #         return err_dict
    #     elif request.method == 'GET':
    #         return 'file is ready'

    @app.route('/validate_response', methods=["GET"])
    def validate_response():
        return render_template('validate_response.html')

    @app.route('/validate', methods=["GET"])
    def validate():
        return render_template('validate.html')

    @app.route('/upload', methods=["GET"])
    def upload():
        return render_template('upload.html')

    # Combining specified files as chosen in the checkboxes
    @app.route('/combine_selected', methods=["POST"])
    def combine_selected():
        if request.method == 'POST':
            operators_path = r'my_app/tmp/'
            file_names = []
            combined = pd.DataFrame()

            # Get the list of selected files 
            files_list = request.form
            selected_files = files_list.getlist('fileslist')

            # Combining all the operaters flight data
            for file in selected_files:
                file_names.append(file.title())
                df = pd.read_excel(operators_path+file)
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
            grouped.to_csv(r'my_app/output/Combined.csv')
            file_names_df.to_csv(r'my_app/output/Combined_File_Names.csv', index=False, header=True)

            # Converting the results to a csv and xlsx files
            grouped.to_csv(r'my_app/output/Combined.csv')
            file_names_df.to_csv(r'my_app/output/Combined_File_Names.csv', index=False, header=True)
            return jsonify({"response": "successfully combined selected files"})  
        else:
            print("not allowed access")
            return jsonify({"response": "acess denied"})


    @app.route("/get_combined", methods=["GET"])
    def combine():
        # Extracting all the files in a path
        operators_path = r'my_app/tmp/'
        files = os.listdir(operators_path)
        file_names = []
        combined = pd.DataFrame()

        # Combining all the operaters flight data
        for file in files:
            if ".xlsx" in file.lower():
                df = pd.read_excel(operators_path+file)
                file_names.append(file.title())
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
        return jsonify({"response": "successfully combined all files"})

    @app.route('/revert/<file_name>', methods = ['GET'])
    def revert(file_name):
        if request.method == 'GET':
            aggregated_files_names_path = 'my_app/output/Combined_File_Names.csv'
            if os.path.exists(aggregated_files_names_path):
                df = pd.read_csv(aggregated_files_names_path)
                df['File Names'] = df['File Names'].apply(str.lower)
                file_name = str(file_name + '.xlsx')
                df = df[df['File Names'] != file_name.lower()]
                df.to_csv(r'my_app/output/Combined_File_Names.csv', index=False, header=True)
        
        return redirect('/admin')

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app
