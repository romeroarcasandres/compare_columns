# compare_columns
This script generates detailed comparison reports by comparing specified columns from delimited text files. It highlights differences between the columns and exports an HTML report for each file processed.

## Overview:
The Compare Columns script processes delimited text files (e.g., .csv, .tsv, .txt) within a selected directory. For each file, it compares two user-specified columns, calculates differences, and generates an HTML report displaying the results. These reports include side-by-side column data and highlighted differences for easy visualization.

## Requirements:
Python 3
tkinter library (utilized for file dialog)
pandas (for data manipulation)
diff_match_patch (for text difference calculation)
os library (for file path operations)

## Files
compare_columns.py

## Usage
1. Run the script.
2. A file dialog will prompt you to select a directory containing the delimited files to process.
3. Provide input for the following:
   * Two column indices to compare (e.g., 2,3 for comparing the 2nd and 3rd columns).
   * Headers to label the compared columns in the HTML report.
4. The script processes all .csv, .tsv, and .txt files in the selected directory:
   * Reads the file and verifies the existence of the specified columns.
   * Compares the columns row by row.
   * Generates an HTML report highlighting differences for each file.
5. The reports are named as 'comparison_report_<filename>.html'

See "compare_columns.JPG" and "comparison_report".

## Supported File Types
The script supports the following file extensions:
* .csv (comma-separated values)
* .tsv (tab-separated values)
* .txt (detects both comma and tab delimiters)

## Example Report
The HTML report displays the following:
* Row number
* Content of both columns
* Highlighted differences between the columns

## Important Notes
1. Ensure the files have valid content and the columns specified exist.
2. Files are read using UTF-8 encoding. If the encoding fails, the script attempts latin-1 encoding.
3. Reports are created for files where comparisons are successful.

## License
This project is governed by the CC BY-NC 4.0 license. For comprehensive details, kindly refer to the LICENSE file included with this project.
