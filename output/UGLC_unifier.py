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

directory = f"{root}/output/converted_csv/"

# List sll CSV files into the dir
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
df_combined = pd.DataFrame()

# Read CSV files from the list then merge em as a single dataframe
for file in csv_files:
    file_path = os.path.join(directory, file)
    df_temp = pd.read_csv(file_path, dtype={'VERSION': object})  # Set datatype of the col "VERSION as obj str (hotfix)
    df_combined = pd.concat([df_combined, df_temp], ignore_index=True)

# Removes duplicates based on WKT_GEOM, START DATE, END DATE (same events)
df_combined.drop_duplicates(subset=['WKT_GEOM', 'START DATE', 'END DATE'], keep='first', inplace=True)

# Generates ID
df_combined['ID'] = [str(i) for i in range(1, len(df_combined) + 1)]

# Test file existence then save
if csv_files:
    output_file = f"{root}/output/UGLC_no_duplicates.csv"
    df_combined.to_csv(output_file, index=False, sep='|')
    print(f"UGLC dataset created on '{output_file}' path with '|' as separator.")
else:
    print("No CSV file found tino the directory.")
