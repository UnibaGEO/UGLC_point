#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     UAP - Landslide Inventories across the United States version2_USGS, Mirus, B.B., Jones, E.S., Baum, R.L. et al.
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import trasforma_data_start,trasforma_data_end,apply_affidability_calculator,assign_country_to_points

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/04_UAP_native.csv", low_memory=False,encoding="utf-8")

# JSON Lookup Tables Loading
with open('04_UAP_LOOKUPTABLES.json', 'r',encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["04_UAP LOOKUP TABLES"]

# null values replacement in the Native Dataframe
df_OLD['Notes'] = df_OLD['Notes'].fillna('ND')
df_OLD['InventoryU'] = df_OLD['InventoryU'].fillna('ND')
df_OLD['Catalog'] = df_OLD['Inventory']

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

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['WKT_GEOM']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC" #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "Landslide Inventories across the United States v.2 (USA, Alaska & Puertorico) - USGS"
df_NEW['OLD ID'] = df_OLD['OBJECTID']
df_NEW['VERSION'] = "V2 - 2022/06/03"
df_NEW['COUNTRY'] = assign_country_to_points(df_OLD)['NAME'].fillna('United States of America')
df_NEW['ACCURACY'] = df_OLD['Confidence']
df_NEW['START DATE'] = df_OLD['Date'].fillna('1878/01/01').apply(trasforma_data_start)
df_NEW['END DATE'] = df_OLD['DATEf'].fillna('2021/12/31').apply(trasforma_data_end)
df_NEW['TYPE'] = df_OLD['Inventory']
df_NEW['TRIGGER'] = df_OLD['TRIGGER']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['Fatalities']
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row:f"UAP - locality: ND - description: {repr(row['Notes'])}",axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row:f"Source: {row['InventoryU']}",axis=1)


#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/04_UAP_converted.csv", sep=',', index=False,encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             04_UAP_native conversion: DONE                               ")
print("__________________________________________________________________________________________")
