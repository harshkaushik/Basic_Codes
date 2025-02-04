import os
import glob
import pandas as pd


class CSVCombiner:
    def __init__(self, input_folder: str, output_file: str, skip_rows: int = 2):
        """
        Initializes the CSVCombiner class.
        :param input_folder: Path to the folder containing CSV files.
        :param output_file: Path to the output Excel file.
        :param skip_rows: Number of rows to skip while reading CSV files.
        """
        self.input_folder = input_folder
        self.output_file = output_file
        self.skip_rows = skip_rows

    def get_file_paths(self) -> list:
        """
        Retrieves all CSV file paths from the input folder.
        :return: List of CSV file paths.
        """
        file_pattern = os.path.join(self.input_folder, "*.csv")
        return glob.glob(file_pattern)

    def read_and_combine_csv(self) -> pd.DataFrame:
        """
        Reads all CSV files, adds a new column with the filename, and concatenates them into a single DataFrame.
        :return: Combined DataFrame.
        """
        file_paths = self.get_file_paths()

        if not file_paths:
            raise FileNotFoundError("No CSV files found in the specified directory.")

        # Read and process each CSV file
        dataframes = []
        for file in file_paths:
            df = pd.read_csv(file, index_col=False, skiprows=self.skip_rows)
            df["Source_File"] = os.path.basename(file).split('.')[0]  # Add source filename as a new column
            dataframes.append(df)

        return pd.concat(dataframes, ignore_index=True)

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs additional processing on the DataFrame, such as splitting file names into relevant columns.
        :param df: Combined DataFrame.
        :return: Processed DataFrame.
        """
        # Example processing: Split 'Source_File' column into 'companyID' and 'author_name' (if applicable)
        if 'Source_File' in df.columns:
            new_split = df['Source_File'].str.split('_', n=1, expand=True)
            df['companyID'] = new_split[0]
            df['author_name'] = new_split[1] if new_split.shape[1] > 1 else None

        # Example processing: Modify URL column
        if 'Story URL' in df.columns:
            df['Curated_URL'] = "url:" + df['Story URL']
            df.drop('Story URL', axis=1, inplace=True)

        return df

    def save_to_excel(self, df: pd.DataFrame):
        """
        Saves the DataFrame to an Excel file.
        :param df: DataFrame to be saved.
        """
        df.to_excel(self.output_file, index=False)
        print(f"Data successfully saved to {self.output_file}")

    def execute(self):
        """
        Executes the entire process of combining, processing, and saving CSV data.
        """
        try:
            combined_df = self.read_and_combine_csv()
            processed_df = self.process_dataframe(combined_df)
            self.save_to_excel(processed_df)
        except Exception as e:
            print(f"Error: {e}")


# Usage example
if __name__ == "__main__":
    input_directory = r'Input Location'
    output_filepath = r'Output Location and File name'

    combiner = CSVCombiner(input_directory, output_filepath)
    combiner.execute()
