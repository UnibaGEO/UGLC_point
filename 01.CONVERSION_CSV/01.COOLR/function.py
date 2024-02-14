import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.wkt import loads
from geopy.geocoders import Nominatim
import requests
#1
"""
file_path = "../../01.CONVERSION_CSV/COUNTRIES.zip"

def apply_country_corrections(df):
    def get_country_name(wkt_geom):
        geometry = loads(wkt_geom)
        longitude, latitude = geometry.xy
        geolocator = Nominatim(user_agent="country_lookup")
        location = geolocator.reverse((latitude[0], longitude[0]), language='en')
        country = location.raw.get('address', {}).get('country')
        return country

    # Leggi i confini dei paesi dal file ZIP
    world = gpd.read_file("zip://" + file_path)

    # Converti la colonna WKT in geometrie Shapely
    df['geometry'] = df['WKT_GEOM'].apply(wkt.loads)

    # Crea un GeoDataFrame per i punti georeferenziati
    points = gpd.GeoDataFrame(df,
                              geometry='geometry',
                              crs='EPSG:4326')

    # Effettua un'operazione di "spazial join" per assegnare a ciascun punto il paese corrispondente
    points_with_country = gpd.sjoin(points, world[['geometry', 'NAME']], how='left', predicate='within')

    # Seleziona le righe con 'ND' nella colonna 'COUNTRY'
    #nd_rows = points_with_country[points_with_country['COUNTRY'] == 'ND'].index

    # Applica il reverse geocoding solo alle righe selezionate
    #points_with_country.loc[nd_rows, 'COUNTRY'] = points_with_country.loc[nd_rows, 'WKT_GEOM'].apply(get_country_name)

    print("________________________________________________________________________________________")
    print("                             COUNTRY Corrections: DONE                                  ")
    print("________________________________________________________________________________________")

    return points_with_country

"""
# -----------------------------------------------------------------------------------------------------------------------
#2

def apply_affidability_calculator(df):
   # Affidability calculations
    def assign_affidability(row):
        accuracy = pd.to_numeric(row['ACCURACY'])
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

    # Apply the addifability calculation
    df['AFFIDABILITY'] = df.apply(assign_affidability, axis=1)

    print("________________________________________________________________________________________")
    print("                             AFFIDABILITY Calculation: DONE                             ")
    print("________________________________________________________________________________________")