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





