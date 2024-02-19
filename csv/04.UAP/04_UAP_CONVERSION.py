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
from pandas import DataFrame
import geopandas as gpd
from UGLC.lib.function_collection import trasforma_data_start,trasforma_data_end,trasforma_accuracy,apply_affidability_calculator,assign_country_to_points


# Native Dataframe 02_GFLD_native loading
df_OLD: DataFrame = pd.read_csv("../../input/native_dataset/04_UAP_native/04_UAP_NATIVE.csv", low_memory=False,encoding="utf-8")

# JSON Lookup Tables Loading
with open('04_UAP_LOOKUPTABLES.json', 'r',encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["04_UAP LOOKUP TABLES"]

# null values replacement in the Native Dataframe
df_OLD['Notes']=df_OLD['Notes'].fillna('ND')
df_OLD['InventoryU']=df_OLD['InventoryU'].fillna('ND')

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
df_NEW['OLD DATASET'] = "UAP"
df_NEW['OLD ID'] = df_OLD['OBJECTID']
df_NEW['VERSION'] = "V2 - 2022/06/03"
df_NEW['COUNTRY'] =assign_country_to_points(df_OLD)['NAME'].fillna('United States of America')
df_NEW['ACCURACY']= df_OLD['Confidence'].apply(trasforma_accuracy)
df_NEW['START DATE'] =df_OLD['Date'].apply(trasforma_data_start)
df_NEW['END DATE'] = df_OLD['Date'].apply(trasforma_data_end)
df_NEW['TYPE'] = df_OLD['Inventory']
df_NEW['TRIGGER'] = df_OLD['TRIGGER']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['Fatalities']
df_NEW['INJURIES'] = "ND"
df_NEW['NOTES'] = f"Landslide Inventories across the United States v.2 (USA, Alaska & Puertorico) - USGS - locality: ND - description: {df_OLD['Notes']}"
df_NEW['LINK'] = f"Source: {df_OLD['InventoryU']}"


#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------


apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv('../../output/converted_datasets/04_UAP_CONVERTED.csv',sep=',', index=False,encoding="utf-8")

print("________________________________________________________________________________________")
print("                             04_UAP_native conversion: DONE                             ")
print("________________________________________________________________________________________")




#-----------------------------------------------------------------------------------------------------------------------