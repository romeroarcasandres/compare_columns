import os
import pandas as pd
import diff_match_patch as dmp_module
from tkinter import Tk, filedialog

def select_directory():
    """Prompt the user to select a directory and return the path."""
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Directory with Files")
    return directory

def get_column_indices_and_headers():
    """Prompt the user to input the column indices and headers."""
    cols = input("Enter the column indices to compare (e.g., 2,3): ")
    header1 = input("Enter the header name for the first column: ")
    header2 = input("Enter the header name for the second column: ")
    col1, col2 = map(int, cols.split(','))
    return col1, col2, header1, header2

def generate_html_template(header1, header2, filename):
    """Generate the HTML template for the report."""
    return [
        f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 10px;
                }}
                .file-info {{
                    background-color: #f8f9fa;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
            </style>
        </head>
        <body>
            <h1>Comparison Report</h1>
            <div class="file-info">
                <strong>File:</strong> {filename}
            </div>
            <table>
                <tr>
                    <th>Row</th>
                    <th>{header1}</th>
                    <th>{header2}</th>
                    <th>Differences</th>
                </tr>
        '''
    ]

def read_delimited_file(file_path):
    """Read different types of delimited files based on file extension."""
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.csv':
            return pd.read_csv(file_path, encoding='utf-8')
        elif file_extension == '.tsv':
            return pd.read_csv(file_path, sep='\t', encoding='utf-8')
        elif file_extension == '.txt':
            # First try tab-delimited
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                # Check if we got more than one column
                if len(df.columns) > 1:
                    return df
            except:
                pass
            
            # If tab-delimited failed or only got one column, try comma-delimited
            return pd.read_csv(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except UnicodeDecodeError:
        # If UTF-8 fails, try with a different encoding
        return pd.read_csv(file_path, encoding='latin1')
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def compare_columns_in_file(file_path, col1, col2, header1, header2):
    """Compare the specified columns in a single file and generate an HTML report."""
    dmp = dmp_module.diff_match_patch()
    filename = os.path.basename(file_path)
    html_report = generate_html_template(header1, header2, filename)
    
    try:
        df = read_delimited_file(file_path)
        
        # Ensure that columns exist
        if col1-1 >= len(df.columns) or col2-1 >= len(df.columns):
            raise IndexError(f"Columns {col1} or {col2} do not exist in file (file has {len(df.columns)} columns)")
        
        col1_data = df.iloc[:, col1-1].astype(str).tolist()
        col2_data = df.iloc[:, col2-1].astype(str).tolist()
        
        for idx, (data1, data2) in enumerate(zip(col1_data, col2_data), 1):
            diffs = dmp.diff_main(str(data1), str(data2))
            dmp.diff_cleanupSemantic(diffs)
            diff_html = dmp.diff_prettyHtml(diffs)
            html_report.append(f'<tr><td>{idx}</td><td>{data1}</td><td>{data2}</td><td><pre>{diff_html}</pre></td></tr>')
        
        html_report.append('</table></body></html>')
        
        # Generate report filename based on input filename
        base_name = os.path.splitext(filename)[0]
        report_filename = f'comparison_report_{base_name}.html'
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_report))
        
        print(f"HTML diff report generated: {report_filename}")
        return True
        
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")
        return False

def main():
    directory = select_directory()
    if not directory:
        print("No directory selected. Exiting.")
        return
    
    col1, col2, header1, header2 = get_column_indices_and_headers()
    
    # Process all supported files in the directory
    supported_extensions = ('.csv', '.tsv', '.txt')
    files_processed = 0
    files_failed = 0
    
    # Get list of all files first
    files_to_process = [f for f in os.listdir(directory) 
                       if f.lower().endswith(supported_extensions)]
    
    if not files_to_process:
        print(f"\nNo supported files found in the directory.")
        print(f"Supported file types: {', '.join(supported_extensions)}")
        return
    
    print(f"\nFound {len(files_to_process)} files to process...")
    
    for filename in files_to_process:
        file_path = os.path.join(directory, filename)
        print(f"\nProcessing {filename}...")
        
        if compare_columns_in_file(file_path, col1, col2, header1, header2):
            files_processed += 1
        else:
            files_failed += 1
    
    print(f"\nProcessing complete!")
    print(f"Files processed successfully: {files_processed}")
    print(f"Files failed: {files_failed}")
    if files_processed > 0:
        print(f"Reports have been generated in the current directory")

if __name__ == "__main__":
    main()