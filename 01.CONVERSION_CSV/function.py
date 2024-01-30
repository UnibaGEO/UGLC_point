import pandas as pd
from shapely.wkt import loads
from opencage.geocoder import OpenCageGeocode

#1
def assign_affidability(row, col_acc, col_st_dt, col_end_dt):
    accuracy = row[col_acc]
    start_date = pd.to_datetime(row[col_st_dt])
    end_date = pd.to_datetime(row[col_end_dt])

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
#_______________________________________________________________________________________________________________________
#2
#import pandas as pd
from opencage.geocoder import OpenCageGeocode
from shapely.wkt import loads

def get_country_name_from_wkt(wkt_point, geocoder):
    # Gestisci il caso in cui la cella sia vuota o NaN
    if pd.isna(wkt_point):
        return None

    # Estrai le coordinate dal punto WKT
    point_coords = loads(wkt_point).coords[0]

    # Utilizza OpenCage Geocoding API per ottenere informazioni sulla posizione
    results = geocoder.reverse_geocode(point_coords[1], point_coords[0], language='en')

    # Estrai il nome del paese dai risultati del reverse geocoding
    country_name = None
    if results and len(results):
        country_name = results[0]['components']['country']

    return country_name
#_______________________________________________________________________________________________________________________
#3
