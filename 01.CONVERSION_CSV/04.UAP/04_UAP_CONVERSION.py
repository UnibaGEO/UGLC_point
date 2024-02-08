#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     UAP - Landslide Inventories across the United States version2_USGS, Mirus, B.B., Jones, E.S., Baum, R.L. et al.
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import json
import numpy as np
from opencage.geocoder import OpenCageGeocode
from function import get_country_name
from function import trasforma_data

# Native Dataframe 02_GFLD_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/04_UAP_NATIVE/04_UAP_NATIVE.csv",low_memory=False)


# JSON Lookup Tables Loading
with open('04_UAP_LOOKUPTABLES.json', 'r') as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["04_UAP LOOKUP TABLES"]


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

# null values replacement in the Native Dataframe
#df_OLD = df_OLD.fillna("ND")

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
df_NEW['NEW DATASET'] = "UAP"
df_NEW['ID'] = "CALC" #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "GFLD"
df_NEW['OLD ID'] = df_OLD['OBJECTID']
df_NEW['VERSION'] = "V2 - 2022/06/03"
df_NEW['COUNTRY'] = 'ND'
df_NEW['ACCURACY'] = "ND"
df_NEW['Date']=df_OLD['Date']
df_NEW['START DATE'] =df_OLD['Date'].apply(trasforma_data)
df_NEW['END DATE'] = "nd"
df_NEW['TYPE'] = df_OLD['Inventory']
df_NEW['TRIGGER'] = df_OLD['TRIGGER']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['Fatalities']
df_NEW['INJURIES'] = "ND"
df_NEW['NOTES'] = "  Landslide Inventories across the United States v.2 (USA, Alaska & Puertorico) - USGS, locality: " + df_NEW['COUNTRY'] + ", description: " + df_OLD['Notes']
df_NEW['LINK'] = "Source: " + df_OLD['InventoryU']
df_NEW['START DATE'].fillna('1878/01/01', inplace=True)
-------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------f

#df_NEW['COUNTRY'] = df_NEW['WKT_GEOM'].apply(lambda x: get_country_name(x))

#from function import update_country_column
#from function import apply_affidability_calculator

#apply_affidability_calculator(df_NEW)
#apply_country_corrections(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv('../../02.OUTPUT/DATASET_CONVERTED/04_UAP_CONVERTED.csv', index=False)
#print("________________________________________________________________________________________")
#print("COOLR-report points successfully converted as UAP_04_CONVERTED.csv in the DATASET_CONVERTED directory")
#print("________________________________________________________________________________________")




#-----------------------------------------------------------------------------------------------------------------------