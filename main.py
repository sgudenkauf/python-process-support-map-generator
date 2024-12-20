# main.py

import sys
import os
from excel_to_csv import convert_excel_to_csv
from generate_map import create_process_support_map

def main():
    # Define input and output paths
    input_excel_file = "excel/process_map.xlsx"
    output_csv_folder = "csv/"

    # Ensure the output folder exists
    if not os.path.exists(output_csv_folder):
        os.makedirs(output_csv_folder)

    # Step 1: Convert Excel to CSV
    print("Converting Excel to CSV...")
    convert_excel_to_csv(input_excel_file, output_csv_folder)

    # Step 2: Generate process support map
    print("Generating process support map...")
    create_process_support_map()

    print("Process completed!")

# If the script is run as standalone, call the main function
if __name__ == "__main__":
    main()
