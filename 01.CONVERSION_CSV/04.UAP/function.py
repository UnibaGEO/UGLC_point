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

