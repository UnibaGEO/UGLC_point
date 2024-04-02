import os
import pandas as pd
from dotenv import load_dotenv

# Load the environment variables from config.env file
load_dotenv("../config.env")
root = os.getenv("FILES_REPO")

# Directory where converted csv are located
directory = f"{root}/output/converted_csv/"

# List of all csv files present into the directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# new empty DataFrame
df_combined = pd.DataFrame()

# Read all the csv files and merge them into a single DataFrame
for file in csv_files:
    file_path = os.path.join(directory, file)
    df_temp = pd.read_csv(file_path, dtype={'VERSION': object})  # Imposta il tipo di dati della colonna "VERSION" come object (stringa)
    df_combined = pd.concat([df_combined, df_temp], ignore_index=True)

df_combined['ID'] = ['P-' + str(i) for i in range(1, len(df_combined) + 1)]

# Verify the presence of csv converted datasets into the specified directory
if csv_files:
    # Save the new dataframe as a new csv file
    output_file = f"{root}/output/UGLC.csv"
    df_combined.to_csv(output_file, index=False)
    print(f"UGLC dataset saved as CSV into: '{output_file}'")
else:
    print("No CSV file found into the directory")
