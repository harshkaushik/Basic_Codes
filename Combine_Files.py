import pandas as pd
import os


def combine_files_with_filenames(input_folder, file_type, output_file='combined_data.csv'):
    """
    Combines all files of a specified type (.xlsx or .csv) from a given folder
    into a single CSV file. A new 'filename' column is added to identify the
    source of each row.

    Args:
        input_folder (str): The path to the folder containing the files.
        file_type (str): The type of files to combine ('excel' or 'csv').
        output_file (str): The name of the output CSV file (default is 'combined_data.csv').
    """
    # Check if the input folder exists
    if not os.path.isdir(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # Create an empty list to store dataframes from each file
    all_dfs = []

    # Determine the file extension based on user input
    if file_type.lower() == 'csv':
        extension = '.csv'
    elif file_type.lower() == 'excel':
        extension = '.xlsx'
    else:
        print("Invalid file type specified. Please choose 'excel' or 'csv'.")
        return

    # Iterate over all files in the specified directory
    for filename in os.listdir(input_folder):
        # Create the full file path
        file_path = os.path.join(input_folder, filename)

        # Skip directories and non-file entries
        if not os.path.isfile(file_path) or not filename.endswith(extension):
            continue

        try:
            # Check the file extension to determine how to read it
            if filename.endswith('.csv'):
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(file_path)
            elif filename.endswith('.xlsx'):
                # Read the Excel file into a pandas DataFrame
                df = pd.read_excel(file_path)

            # Add a new column to the DataFrame with the original filename
            df['filename'] = filename

            # Append the DataFrame to our list
            all_dfs.append(df)
            print(f"Successfully processed {filename}")

        except Exception as e:
            # Catch any errors during file reading and report them
            print(f"Error processing {filename}: {e}")

    # Check if any dataframes were successfully loaded
    if not all_dfs:
        print(f"No supported {file_type.upper()} files found to combine.")
        return

    # Concatenate all dataframes in the list into a single one
    # The ignore_index=True argument resets the index of the combined DataFrame
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    try:
        combined_df.to_csv(output_file, index=False)
        print(f"\nAll files successfully combined into '{output_file}'.")
    except Exception as e:
        print(f"Error saving the combined file: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    folder_to_combine = r'C:\Users\Lenovo\PycharmProjects\basic-codes\test csv files'
    output_combined_file = 'combined_output.csv'

    # Get user input for the file type to combine
    user_file_type = input("Enter the file type to combine ('excel' or 'csv'): ")

    combine_files_with_filenames(folder_to_combine, user_file_type, output_combined_file)
