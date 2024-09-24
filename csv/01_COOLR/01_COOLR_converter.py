#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     COOLR report points - NASA
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import json
from lib.function_collection import apply_affidability_calculator, apply_country_corrections
import pandas as pd
import os
from dotenv import load_dotenv

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
df_OLD = pd.read_csv(f"{root}/input/native_datasets/01_COOLR_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('01_COOLR_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["01_COOLR LOOKUP TABLES"]

# null values replacement in the Native Dataframe
df_OLD['loc_acc'] = df_OLD['loc_acc'].fillna('-99999')
df_OLD['src_link'] = df_OLD['src_link'].fillna('ND')
df_OLD['loc_desc'] = df_OLD['loc_desc'].fillna('ND')
df_OLD['ev_desc'] = df_OLD['ev_desc'].fillna('ND')
df_OLD['ev_dateS'] = df_OLD['ev_date'].fillna('1956/01/01')
df_OLD['ev_dateE'] = df_OLD['ev_date'].fillna('2023/01/01')
df_OLD['ctry_name'] = df_OLD['ctry_name'].fillna('ND')

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
    'TRIGGER': [],
    'AFFIDABILITY': [],
    'RECORD TYPE': [],
    'FATALITIES': [],
    'INJURIES': [],
    'NOTES': [],
    'LINK': []
}

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['WKT_GEOM']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC"  #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "Cooperative Open Online Landslide Repository - NASA"
df_NEW['OLD ID'] = df_OLD['ev_id']
df_NEW['VERSION'] = str("2019")
df_NEW['COUNTRY'] = df_OLD['ctry_name'].replace("CÃ´te d'Ivoire", "Côte d'Ivoire", inplace=True)
df_NEW['ACCURACY'] = df_OLD['loc_acc']
df_NEW['START DATE'] = df_OLD.apply(lambda row: pd.to_datetime(row['ev_dateS']).strftime('%Y/%m/%d'), axis=1)
df_NEW['END DATE'] = df_OLD.apply(lambda row: pd.to_datetime(row['ev_dateE']).strftime('%Y/%m/%d'), axis=1)
df_NEW['TYPE'] = df_OLD['ls_cat'].fillna('ND')
df_NEW['TRIGGER'] = df_OLD['ls_trig'].fillna('ND')
df_NEW['AFFIDABILITY'] = 'CALC'
df_NEW['RECORD TYPE'] = df_OLD['OLD DATASET'].apply(lambda x: 'event' if x == 'COOLR_E' else 'report')
df_NEW['FATALITIES'] = df_OLD['fatalities']
df_NEW['INJURIES'] = df_OLD['injuries']
df_NEW['NOTES'] = df_OLD.apply(lambda row:f"{row['OLD DATASET']}, locality: {repr(row['loc_desc'])}, description: {repr(row['src_name'])} {repr(row['ev_desc'])}",axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {repr(row['src_link'])}",axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_country_corrections(df_NEW)
apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/01_COOLR_converted.csv", index=False, encoding="utf-8")

print("________________________________________________________________________________________")
print("                             01_COOLR_native conversion: DONE                           ")
print("________________________________________________________________________________________")

#-----------------------------------------------------------------------------------------------------------------------
# End
#-----------------------------------------------------------------------------------------------------------------------