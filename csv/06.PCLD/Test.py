import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import date_f_correction, date_s_correction
# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")
#------------------------------
# MODIFICABILI
#------------------------------
df = pd.read_csv(f"{root}/output/converted_csv/06_PCLD_converted.csv", low_memory=False, encoding="utf-8")
row = 1731
column = 'START DATE'
#------------------------------
print(f"Il tipo della cella è {type(df.iloc[row][column])}")
print(f"Il contenuto della cella è {df.iloc[row][column]}")
