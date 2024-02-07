
import pandas as pd
import json
import numpy as np
from opencage.geocoder import OpenCageGeocode

import pandas as pd


import pandas as pd
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/04_UAP_NATIVE/04_UAP_NATIVE.csv",low_memory=False)

import csv
from datetime import datetime
""""
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
df_OLD = df_OLD.fillna("ND")
"""

def trasforma_data(data):

    if pd.isnull(data):
        return None

    # Conversione da d/mm/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%d/%m/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    original_data = data
    # Conversione da mm/yyyy a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%m/%Y').strftime('%Y/%m')
        return nuova_data
    except ValueError:
        pass

    #Conversione da d1/m1/y1-d2/m2/y2 a y1/m1/d1

    try:
        data_inizio, data_fine = data.split('-')
        data_inizio = datetime.strptime(data_inizio.strip(), '%m/%d/%y').strftime('%Y/%m/%d')
        return data_inizio

        #data_inizio, data_fine = data.split('-')
        #data_inizio = datetime.strptime(data_inizio.strip(), '%m/%d/%Y').strftime('%Y/%m/%d')
        #data_fine = datetime.strptime(data_fine.strip(), '%m/%d/%Y').strftime('%Y/%m/%d')
        #nuova_data = f"{data_inizio}"
       #return nuova_data
    except ValueError:
        pass

    # Conversione da yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data, '%Y').strftime('%Y')
        return nuova_data
    except ValueError:
        pass

    # Conversione da -yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y')
        return nuova_data
    except ValueError:
        pass
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    try:
        nuova_data = datetime.strptime(data, '%b.%Y').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y, %A').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Se non viene effettuata nessuna trasformazione, restituisci la data originale
    return data


def trasforma_file_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        with open(output_file, 'w', newline='') as csvfile_output:
            writer = csv.writer(csvfile_output)
            for row in reader:
                row = [trasforma_data(data) for data in row]
                writer.writerow(row)


#df_OLD = pd.DataFrame({'Date': ['1/1/2022', '02/2023', '15/12/2024', '10/1/2024-20/1/2024', '2025', '-2026', 'abc', '2/26/2018 7:30:00 AM', 'Sept.2019', '1/3/1999, Daytime', '5/1/19-6/9/19']})

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
print(df_NEW)
# Utilizzo della funzione per trasformare il file CSV
df_NEW.to_csv('../../02.OUTPUT/DATASET_CONVERTED/04_UAP_CONVERTED_temp_data.csv')

