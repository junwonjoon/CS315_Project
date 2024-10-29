import pandas as pd

# Function to read the CSV file and convert it to a pandas DataFrame
def read_airports_csv(file_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

# Path to the sample CSV file
file_path = "/mnt/data/airports_sample.csv"

# Read the CSV and convert it to a pandas DataFrame
airports_df = read_airports_csv(file_path)

# Display the DataFrame as a sample
print(airports_df)
