#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     15 -  CAmpi Flegrei LAndslide Geodatabase (CAFLAG)
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_RELIABILITY_calculator, compose_start_date, compose_end_date

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/15_CAFLAG_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('15_CAFLAG_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["15_CAFLAG LOOKUP TABLES"]

# Application of lookup Tables to the columns of the old DataFrame
for column in df_OLD.columns:
    lookup_table_key = f"{column}_lookup"  # Lookup table match-Key construction

    # Lookup Tables check if is a string or a dictionary
    if lookup_table_key in lookup_tables and isinstance(lookup_tables[lookup_table_key], dict):
        lookup_table = lookup_tables[lookup_table_key]

        # If the lookup table is marked as "ND" the sytem will keep the original content
        if lookup_table == "ND":
            continue
        else:
            # Update just the no-"ND" columns
            df_OLD[column] = df_OLD[column].map(lambda x: lookup_table.get(str(x), x))

# New dataframe Configuration
new_data = {
    'WKT_GEOM': [],
    'NEW DATASET': [],
    'ID': [],
    'OLD DATASET': [],
    'OLD ID': [],
    'VERSION': [],
    'COUNTRY': [],
    'ACCURACY': [],
    'START DATE': [],
    'END DATE': [],
    'TYPE': [],
    'PHYSICAL FACTORS': [],
    'RELIABILITY': [],
    'RECORD TYPE': [],
    'FATALITIES': [],
    'INJURIES': [],
    'NOTES': [],
    'LINK': []
}

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['geometry']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "CAmpi Flegrei LAndslide Geodatabase"
df_NEW['OLD ID'] = df_OLD['ID']
df_NEW['VERSION'] = str("version 2 - 2021-04-23 (latest)")
df_NEW['COUNTRY'] = "Italy"
df_NEW['ACCURACY'] = df_OLD['LOCAT_ACC']
df_NEW['START DATE'] = df_OLD.apply(lambda row: compose_start_date(row['YEAR'], row['MONTH'], row['DAY']), axis=1)
df_NEW['END DATE'] = df_OLD.apply(lambda row: compose_end_date(row['YEAR'], row['MONTH'], row['DAY']), axis=1)
df_NEW['TYPE'] = df_OLD['TYPE']
df_NEW['PHYSICAL FACTORS'] = df_OLD['CAUSE']
df_NEW['RELIABILITY'] = "ND"
df_NEW['RECORD TYPE'] = "event"
df_NEW['FATALITIES'] = df_OLD['FATAL']
df_NEW['INJURIES'] = df_OLD['INJURED']
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"CAFLAG - locality: Italy,{(row['TOWN'])} {(row['LOCALITY'])} - description: {(row['GEOM_CONT'])} {(row['TYPE'])}", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {row['SOURCE']}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_RELIABILITY_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/15_CAFLAG_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             15_CAFLAG_native conversion: DONE                            ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
