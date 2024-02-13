import re
import pandas as pd
from shapely.wkt import loads
from opencage.geocoder import OpenCageGeocode
import numpy as np
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely import wkt

#1
"""
def apply_country_corrections(df):
    def get_country_name(WKT_GEOM):
        geometry = loads(WKT_GEOM)
        longitude, latitude = geometry.xy
        geolocator = Nominatim(user_agent="country_lookup")
        location = geolocator.reverse((latitude[0], longitude[0]), language='en')
        country = location.raw.get('address', {}).get('country')
        return country

    # Indexes rows with 'ND' in the column 'COUNTRY'
    nd_rows = df[df['COUNTRY'] == 'ND'].index

    # Iterate on the lines and update the country name
    for idx in nd_rows:
        WKT_GEOM = df.at[idx, 'WKT_GEOM']

        try:
            country_name = get_country_name(WKT_GEOM)
            df.at[idx, 'COUNTRY'] = country_name
        except Exception as e:
            print("_")
            #print(f"Error during the coordinates extraction from the row {idx}: {e}")
            #print("________________________________________________________________________________________")
"""

api_key = '345b70a41acc4ae49b07f28e0bd637c1'
geocoder = OpenCageGeocode(api_key)
def get_country_name(row):
    # Utilizza il geocoder di OpenCage Geocode per ottenere il nome del paese
    result = geocoder.geocode(f"{row['lat']}, {row['long']}", no_annotations=1)
    if result and 'components' in result[0]:
        return result[0]['components']['country']
    return 'ND'



# -----------------------------------------------------------------------------------------------------------------------
#2

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
    print("Valori di 'AFFIDABILITY' assegnati con successo.")
    print("________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------
#3 FUNZIONE DI TRASFORMAZIONE START_DATE
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
#4 FUNZIONE DI TRASFORMAZIONE END_DATE
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

    # Conversione da mm/yyyy a yyyy/mm
    try:
        nuova_data = datetime.strptime(data, '%m/%Y').strftime('%Y/%m/31')
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
    # Conversione da abbreviazione mese/anno a YYYY/MM/01
    try:
        nuova_data = datetime.strptime(data, '%b.%Y').strftime('%Y/%m/31')
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
