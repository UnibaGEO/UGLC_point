import re
import pandas as pd
from shapely.wkt import loads
import numpy as np
from shapely import wkt
import calendar
import geopandas as gpd
from sklearn.neighbors import BallTree

#2
file_path = "../../01.CONVERSION_CSV/COUNTRIES.zip"


def assign_country_to_points(df):
    # Leggi i confini dei paesi dal file ZIP
    world = gpd.read_file("zip://" + file_path)

    # Crea un GeoDataFrame per i punti georeferenziati
    points = gpd.GeoDataFrame(df,
                              geometry=gpd.points_from_xy(df['long'], df['lat']),
                              crs='EPSG:4326')

    # Effettua un'operazione di "spazial join" per assegnare a ciascun punto il paese corrispondente
    points_with_country = gpd.sjoin(points, world[['geometry', 'NAME']], how='left', predicate='within')

    return points_with_country

print("________________________________________________________________________________________")
print("                             COUNTRY Corrections: DONE                                  ")
print("________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------
#3

def apply_affidability_calculator(df):
    # Converti la colonna 'ACCURACY' in numeri, trattando 'ND' come NaN
    df['ACCURACY'] = pd.to_numeric(df['ACCURACY'], errors='coerce')

    # Funzione di trasformazione per assegnare un valore da 1 a 10 alla colonna 'AFFIDABILITY'
    def assign_affidability(row):
        accuracy = row['ACCURACY']
        start_date = pd.to_datetime(row['START DATE'])
        end_date = pd.to_datetime(row['END DATE'])

        if pd.notna(accuracy):
            if accuracy <= 100:
                if start_date == end_date:
                    return 1
                else:
                    return 2
            elif 100 < accuracy <= 250:
                if start_date == end_date:
                    return 3
                else:
                    return 4
            elif 250 < accuracy <= 500:
                if start_date == end_date:
                    return 5
                else:
                    return 6
            elif 500 < accuracy <= 1000:
                if start_date == end_date:
                    return 7
                else:
                    return 8
            elif accuracy > 1000:
                return 9
        else:  # 'ND' case
            return 10

    # Applica la funzione di trasformazione alla colonna 'AFFIDABILITY'
    df['AFFIDABILITY'] = df.apply(assign_affidability, axis=1)

    # Riconverti la colonna 'ACCURACY' in stringhe, trasformando i NaN in 'ND'
    df['ACCURACY'] = df['ACCURACY'].fillna('ND')

    print("________________________________________________________________________________________")
    print("                             AFFIDABILITY  calculation: DONE                            ")
    print("________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------
#4 FUNZIONE DI TRASFORMAZIONE START_DATE
from datetime import datetime

def trasforma_data_start(data):

    if pd.isnull(data):
        return '1878/01/01'

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

# -----------------------------------------------------------------------------------------------------------------------
#5 FUNZIONE DI TRASFORMAZIONE END_DATE
from datetime import datetime

def trasforma_data_end(data):

    if pd.isnull(data):
        return '2021/12/31'

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

# ----------------------------------------------------------------------------------------------------------------------
#6 FUNZIONE DI TRASFORMAZIONE ACCURACY

def trasforma_accuracy(accuracy):

    if pd.isnull(accuracy):
        return None
    elif accuracy == 8 or accuracy == 5:
        return "0"
    elif accuracy == 3:
        return "250"
    elif accuracy == 2 or accuracy == 1:
        return "50000"

