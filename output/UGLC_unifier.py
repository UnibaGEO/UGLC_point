import os
import pandas as pd
from dotenv import load_dotenv

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Directory contenente i file CSV standardizzati
directory = f"{root}/output/converted_csv/"

# List sll CSV files into the dir
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
df_combined = pd.DataFrame()

# Verifica se ci sono file CSV nella directory specificata
if csv_files:
    # Read CSV files from the list then merge em as a single dataframe
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df_temp = pd.read_csv(file_path, dtype={'VERSION': object})   # Set datatype of the col "VERSION as obj str (hotfix)
        df_combined = pd.concat([df_combined, df_temp], ignore_index=True)
else:
    print("No CSV file found in the directory.")

## ------------------ DATA CLEANING ------------------

# Data Cleaning: removes records with 'TYPE' == "snow avalanche"
df_combined = df_combined[df_combined['TYPE'] != "snow avalanche"]

## ------------------ NO DUPLICATES ------------------

# Removes duplicates based on having same 'WKT_GEOM', 'START DATE', 'END DATE' keeping the ones wth more affidability
df_cleaned = df_combined.loc[df_combined.groupby(['WKT_GEOM', 'START DATE', 'END DATE'])['AFFIDABILITY'].idxmin()]
df_cleaned['ID'] = [str(i) for i in range(1, len(df_cleaned) + 1)] # Generates ID

# Save the duplicate-free dataframe as a csv file
output_file = f"{root}/output/UGLC.csv"
df_cleaned.to_csv(output_file, index=False, sep='|')
print(f"UGLC dataset cleaned created on '{output_file}' path with '|' as separator.")

## ------------------ DUPLICATES ------------------

# Find duplicates based on having same 'WKT_GEOM', 'START DATE', 'END DATE' (same event)
duplicates = df_combined[~df_combined.index.isin(df_cleaned.index)].copy()
duplicates['ID'] = [str(i) for i in range(1, len(duplicates) + 1)] # Generates ID

# Save the duplicates as a separate csv file
duplicates_file = f"{root}/output/UGLC_duplicates.csv"
duplicates.to_csv(duplicates_file, index=False, sep='|')
print(f"Duplicates file created on '{duplicates_file}' with '|' as separator.")

print(len(df_cleaned))