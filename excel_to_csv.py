import os
import pandas as pd

def convert_excel_to_csv(excel_file, output_folder="csv/"):
    """
    Convert specific sheets from an Excel file into individual CSV files.

    Args:
        excel_file (str): Path to the Excel file.
        output_folder (str): Directory where the CSV files will be saved.

    Raises:
        FileNotFoundError: If the Excel file does not exist.
        ValueError: If required sheets are missing from the Excel file.
    """
    # Ensure the Excel file exists
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file '{excel_file}' not found.")

    # Load the Excel file
    try:
        excel_data = pd.ExcelFile(excel_file)
    except Exception as e:
        raise ValueError(f"Failed to load the Excel file: {e}")

    # Required sheet names and their corresponding CSV output names
    required_sheets = {
        "software": "software.csv",
        "processes": "processes.csv",
        "organizational_units": "organizational_units.csv",
        "links": "links.csv"
    }

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each required sheet
    for sheet_name, csv_file in required_sheets.items():
        if sheet_name not in excel_data.sheet_names:
            raise ValueError(f"Required sheet '{sheet_name}' is missing from the Excel file.")

        # Read the sheet into a DataFrame
        sheet_data = excel_data.parse(sheet_name)

        # Save DataFrame as a CSV file
        output_path = os.path.join(output_folder, csv_file)
        sheet_data.to_csv(output_path, index=False)
        print(f"Generated CSV: {output_path}")


# Allow both module import and standalone execution
if __name__ == "__main__":
    # Define paths
    input_excel_file = "excel/process_map.xlsx"
    output_csv_folder = "csv/"

    # Convert Excel sheets to CSV files
    convert_excel_to_csv(input_excel_file, output_csv_folder)
