import pandas as pd
import json
import os
#from lib.function_collection import trasforma_data_start,trasforma_data_end #,trasforma_accuracy,apply_affidability_calculator,assign_country_to_points
from dotenv import load_dotenv


#-------
#4 START_DATE CORRECTION
from datetime import datetime

def trasforma_data_start(data):

    if pd.isnull(data):
        return pd.to_datetime('1878/01/01').strftime('%Y/%m/%d')

    # Conversione da yyyy/mm/d a yyyy/mm/d ----------------------------
    try:
        nuova_data = datetime.strptime(data, '%Y/%m/%d').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da d/mm/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%d/%m/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
        # Conversione da yyyy/d/mm a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%Y/%d/%m').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy,Periodo a yyyy/mm/d
    try:
        # Splitta la data e il periodo
        parti = data.split(',')
        data_senza_periodo = parti[0]

        # Converte la data nel formato desiderato
        nuova_data = datetime.strptime(data_senza_periodo, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da mm/yyyy a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%m/%Y').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass
        # Conversione da yyyy/mm a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%Y/%m').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass

    #Conversione da d1/m1/y1-d2/m2/y2 a y1/m1/d1

    try:
        data_inizio, data_fine = data.split('-')
        data_inizio = datetime.strptime(data_inizio.strip(), '%m/%d/%y').strftime('%Y/%m/%d')
        return data_inizio


    except ValueError:
        pass

    # Conversione da yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data, '%Y').strftime('%Y/01/01')
        return nuova_data
    except ValueError:
        pass

    # Conversione da yyyy/mm/d1-d2 a yyyy/mm/d1
    try:
        data_inizio, _ = data.split('-')
        data_inizio = datetime.strptime(data_inizio.strip(), '%Y/%m/%d').strftime('%Y/%m/%d')
        return data_inizio
    except ValueError:
        pass

    # Conversione da -yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m:s AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da abbreviazione mese/anno a YYYY/MM/01
    try:
        nuova_data = datetime.strptime(data, '%b.%Y').strftime('%Y/%m/01')
        return nuova_data
    except ValueError:
        pass
        # Conversione da y1y1y1y1-y2y2y2y2 a y1y1y1y1/01/01
        try:
            y1, y2 = data[:4], data[4:]
            nuova_data = f"{y1}/01/01"
            return nuova_data
        except ValueError:
            pass
    # Conversione da mm/d/yyyy,Giorno settimana a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y, %A').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Se non viene effettuata nessuna trasformazione, restituisci la data originale
    return data

    print("________________________________________________________________________________________")
    print("                             START DATE  correction: DONE                            ")
    print("________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------
#5 END DATE CORRECTION
from datetime import datetime

def trasforma_data_end(data):

    if pd.isnull(data):
        return pd.to_datetime('2021/12/31').strftime('%Y/%m/%d')

    # Conversione da d/mm/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%d/%m/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
        # Conversione da yyyy/d/mm a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%Y/%d/%m').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy,Periodo a yyyy/mm/d
    try:
        # Splitta la data e il periodo
        parti = data.split(',')
        data_senza_periodo = parti[0]

        # Converte la data nel formato desiderato
        nuova_data = datetime.strptime(data_senza_periodo, '%m/%d/%Y').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    try:
        nuova_data = datetime.strptime(data, '%m/%Y')
        if nuova_data.month == 2:
            nuovo_giorno = 28
        elif nuova_data.month == 1:
            nuovo_giorno = 31
        elif nuova_data.month == 3:
            nuovo_giorno = 31
        elif nuova_data.month == 4:
            nuovo_giorno = 30
        elif nuova_data.month == 5:
            nuovo_giorno = 31
        elif nuova_data.month == 6:
            nuovo_giorno = 30
        elif nuova_data.month == 7:
            nuovo_giorno = 31
        elif nuova_data.month == 8:
            nuovo_giorno = 31
        elif nuova_data.month == 9:
            nuovo_giorno = 30
        elif nuova_data.month == 10:
            nuovo_giorno = 31
        elif nuova_data.month == 11:
            nuovo_giorno = 30
        elif nuova_data.month == 12:
            nuovo_giorno = 31

        nuova_data = nuova_data.replace(day=nuovo_giorno).strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    #Conversione da d1/m1/y1-d2/m2/y2 a y1/m1/d1

    try:
        data_inizio, data_fine = data.split('-')
        data_fine = datetime.strptime(data_fine.strip(), '%m/%d/%y').strftime('%Y/%m/%d')
        return data_fine
    except ValueError:
        pass

    # Conversione da yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data, '%Y').strftime('%Y/12/31')
        return nuova_data
    except ValueError:
        pass

    # Conversione da yyyy/mm/d1-d2 a yyyy/mm/d1
    try:
        _,data_fine, _ = data.split('-')
        data_fine = datetime.strptime(data_fine.strip(), '%Y/%m/%d').strftime('%Y/%m/%d')
        return data_fine
    except ValueError:
        pass

    # Conversione da yyyy/mm/d a yyyy/mm/d ----------------------------
    try:
        nuova_data = datetime.strptime(data, '%Y/%m/%d').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Conversione da -yyyy a yyyy
    try:
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y/12/31')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m:s AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass
    # Conversione da -mm/d/yyyy h:m AM/PM in yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y %I:%M %p').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

# Conversione da y1y1y1y1-y2y2y2y2 a y1y1y1y1/01/01
    try:
        y1, y2 = data[:4], data[4:]
        nuova_data = f"{y1}/12/31"
        return nuova_data
    except ValueError:
        pass
    # Conversione da mm/d/yyyy,Giorno settimana a yyyy/mm/d
    try:
        nuova_data = datetime.strptime(data, '%m/%d/%Y, %A').strftime('%Y/%m/%d')
        return nuova_data
    except ValueError:
        pass

    # Se non viene effettuata nessuna trasformazione, restituisci la data originale
    return data

    print("________________________________________________________________________________________")
    print("                             END DATE  correction: DONE                            ")
    print("________________________________________________________________________________________")
# ----------------------------------------------------------------------------------------------------------------------
#-------

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/04_UAP_native.csv", low_memory=False,encoding="utf-8")

# JSON Lookup Tables Loading
with open('04_UAP_LOOKUPTABLES.json', 'r',encoding="utf-8") as file:
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


df_OLD['Date'] = df_OLD['Date'].fillna('1878/01/01')
df_OLD['Date'] = df_OLD['Date'].apply(trasforma_data_start)

#print("first")

df_OLD['DATEf'] = df_OLD['DATEf'].fillna('2021/12/31')
df_OLD['DATEf'] = df_OLD['DATEf'].apply(trasforma_data_end)


#df_OLD['Date'] = pd.to_datetime(df_OLD['Date'],format='%Y/%m/%d',exact=False)
#df_OLD['Date'] = pd.to_datetime(df_OLD['Date'],format='%Y/%m/%d',exact=False)



'''
df_OLD[df_OLD['Date']=="1948"]
df_OLD['Date'] = pd.to_datetime(df_OLD['Date'].fillna('1878/01/01'))
df_OLD['Date'] = df_OLD['Date'].apply(trasforma_data_start)

df_OLD['DATEf'] = pd.to_datetime(df_OLD['DATEf'].fillna('2021/12/31'))
df_OLD['DATEf'] = df_OLD['DATEf'].apply(trasforma_data_end)
'''
print(df_OLD.iloc[18776])
print(type(df_OLD.iloc[18776]['Date']))
print(type(df_OLD.iloc[18776]['DATEf']))

#df_OLD.to_csv(f"{root}/input/native_datasets/prova04.csv", sep=',', index=False,encoding="utf-8")