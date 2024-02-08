from calendar import calendar
import pandas as pd
import json
import numpy as np
from opencage.geocoder import OpenCageGeocode
from datetime import datetime
from function import trasforma_data

df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/04_UAP_NATIVE/04_UAP_NATIVE.csv",low_memory=False)

#df_OLD['Date'] = df_OLD['Date'].apply(trasforma_data)

print(df_OLD)

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
df_OLD = df_OLD.fillna("1878/01/01")


# Assume che df_NEW sia il tuo nuovo DataFrame con la colonna 'start_date'
# E 'start_date' è la colonna che vuoi trasformare
new_data = {
    'OLD_DATA': [],
    'START_DATA': [],
}
df_NEW = pd.DataFrame(new_data)

# Creazione di un nuovo DataFrame con la colonna 'start_date' originale
df_NEW['OLD_DATA'] = df_OLD['Date']

# Creazione della colonna 'start_date_converted' applicando la funzione trasforma_data
df_NEW['START_DATA'] = df_OLD['Date'].apply(trasforma_data)

# Visualizza il nuovo DataFrame
#print(df_NEW)
righe_con_data_specifica = df_NEW[df_NEW['OLD_DATA'] == '1852/05/14']
righe_con_data_specifica = df_NEW[df_NEW['OLD_DATA'] == '1869/10/01']
print(righe_con_data_specifica)

# Utilizzo della funzione per trasformare il file CSV
df_NEW.to_csv('../../02.OUTPUT/DATASET_CONVERTED/04_UAP_CONVERTED_temp_data5.csv')

