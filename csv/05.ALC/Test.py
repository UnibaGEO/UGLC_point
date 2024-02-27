import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import trasforma_data_start,trasforma_data_end,trasforma_accuracy,apply_affidability_calculator,assign_country_to_points

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/05_ALC_native.csv", low_memory=False,encoding="utf-8")
df_OLD = df_OLD.rename(columns=lambda x: x.replace('\n', ' '))

print(df_OLD.columns.values)
