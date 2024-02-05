#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     ITALICA - CNR IRPI
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json

# Native Dataframe 02_COOLR_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/03_ITALICA_NATIVE/03_ITALICA_NATIVE.csv",low_memory=False)

# JSON Lookup Tables Loading
with open('03_ITALICA_LOOKUPTABLES.json', 'r') as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["03_ITALICA LOOKUP TABLES"]

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
df_NEW['ID'] = "CALC"  #range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = "ITALICA"
df_NEW['OLD ID'] = df_OLD['id']
df_NEW['VERSION'] = "V2 - 2023"
df_NEW['COUNTRY'] = "Italy"
df_NEW['ACCURACY'] = df_OLD['geographic_accuracy']
df_NEW['START DATE'] = pd.to_datetime(df_OLD['utc_date'], format="%d/%m/%Y %H:%M:%S", errors='coerce').dt.strftime("%Y/%m/%d")
df_NEW['END DATE'] = pd.to_datetime(df_OLD['utc_date'], format="%d/%m/%Y %H:%M:%S", errors='coerce').dt.strftime("%Y/%m/%d")
df_NEW['TYPE'] = df_OLD['landslide_type']
df_NEW['TRIGGER'] = "rainfall"
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = "ND"
df_NEW['INJURIES'] = "ND"
df_NEW['NOTES'] = "ITAlian rainfall-induced LandslIdes Catalogue - CNR IRPI, locality:"+df_OLD['province']+", "+ df_OLD['region'] +", description: ND"
df_NEW['LINK'] = "Source: ND"

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

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv('../../03.OUTPUT/DATASET_CONVERTED/03_ITALICA_CONVERTED.csv', index=False)
print("________________________________________________________________________________________")
print("COOLR-report points successfully converted as ITALICA_03_CONVERTED.csv in the DATASET_CONVERTED directory")
print("________________________________________________________________________________________")
#-----------------------------------------------------------------------------------------------------------------------
