#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     SLIDO -  Statewide Landslide Information Database for Oregon (DOGAMI)
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_affidability_calculator, start_date_SLIDO, end_date_SLIDO

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/13_SLIDO_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('13_SLIDO_LOOKUPTABLES.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["13_SLIDO LOOKUP TABLES"]

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
    'PSV': [],
    'DCMV': [],
    'FATALITIES': [],
    'INJURIES': [],
    'NOTES': [],
    'LINK': []
}

df_OLD['LOC_METHOD'] = df_OLD['LOC_METHOD'].fillna("-99999")
df_OLD['LOSSES'] = df_OLD['LOSSES'].fillna("-99999")
df_OLD['COMMENTS'] = df_OLD['COMMENTS'].fillna("ND")
df_OLD['DAMAGES'] = df_OLD['DAMAGES'].fillna("ND")
df_OLD['DATA_SOURC'] = df_OLD['DATA_SOURC'].fillna("ND")

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['geometry']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "Statewide Landslide Information Database for Oregon (DOGAMI)"
df_NEW['OLD ID'] = df_OLD['UNIQUE_ID']
df_NEW['VERSION'] = "v. 4.4 2021/10/29"
df_NEW['COUNTRY'] = "United States of America"
df_NEW['ACCURACY'] = df_OLD['LOC_METHOD']
df_NEW['START DATE'] = df_OLD.apply(start_date_SLIDO, axis=1)
df_NEW['END DATE'] = df_OLD.apply(end_date_SLIDO, axis=1)
df_NEW['TYPE'] = df_OLD['MOVE_CLASS']
df_NEW['TRIGGER'] = df_OLD['CONTR_FACT'].fillna('ND')
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['LOSSES']
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"SLIDO - locality: Oregon - description: {repr(row['COMMENTS'])} {repr(row['DAMAGES'])}", axis=1)
df_NEW['LINK'] = df_OLD['DATA_SOURC'].fillna('ND')

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/13_SLIDO_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             13_SLIDO_native conversion: DONE                             ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
