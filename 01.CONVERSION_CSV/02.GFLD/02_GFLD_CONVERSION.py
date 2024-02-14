#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     GFLD - Global fatal landslide occurrence from 2004 to 2016, Froude, M. J. and Petley, D. N
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import json
import numpy as np


# Native Dataframe 02_GFLD_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/02_GFLD_NATIVE/02_UGLC_NATIVE.csv",low_memory=False)

# JSON Lookup Tables Loading
with open('02_GFLD_LOOKUPTABLES.json', 'r') as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["02_GFLD LOOKUP TABLES"]


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
df_OLD = df_OLD.fillna("ND")

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
df_NEW['OLD DATASET'] = "GFLD"
df_NEW['OLD ID'] = df_OLD['LandslideN']
df_NEW['VERSION'] = "2017"
df_NEW['COUNTRY'] = df_OLD['Country']
df_NEW['ACCURACY'] = round(np.sqrt((df_OLD['Precision'].astype(int)/ np.pi)),0)
df_NEW['START DATE'] = df_OLD['Year'].astype(str) + "/" + df_OLD['Month'].astype(str) + "/" + df_OLD['Day'].astype(str)
df_NEW['END DATE'] = df_OLD['Year'].astype(str) + "/" + df_OLD['Month'].astype(str) + "/" + df_OLD['Day'].astype(str)
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = df_OLD['Trigger']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['Fatalities']
df_NEW['INJURIES'] = "ND"
df_NEW['NOTES'] = " Global fatal landslide, locality: " + df_OLD['Location_M'] + ", description: " + df_OLD['Report_1']
df_NEW['LINK'] = "Source: " + df_OLD['Source_1']

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------f

from function import apply_affidability_calculator

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------
print(df_NEW['TRIGGER'].unique())
# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv('../../02.OUTPUT/DATASET_CONVERTED/02_GFLD_CONVERTED.csv', index=False)
print("________________________________________________________________________________________")
print("                            02_GFLD_NATIVE conversion: DONE                             ")
print("________________________________________________________________________________________")
#-----------------------------------------------------------------------------------------------------------------------