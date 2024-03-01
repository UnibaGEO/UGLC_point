import pandas as pd
from shapely import wkt
import geopandas as gpd
from sklearn.neighbors import BallTree
from shapely.geometry import Point
from dotenv import load_dotenv
import os

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

#1 ASSIGN COUNTRY ( FROM NODATA, WITHOUT COLUMN)
file_path = f"{root}/COUNTRIES.zip"


def assign_country_to_points(df):
    # Leggi i confini dei paesi dal file ZIP
    world = gpd.read_file("zip://" + file_path)

    # Crea un GeoDataFrame per i punti georeferenziati
    points = gpd.GeoDataFrame(df,
                              geometry=gpd.points_from_xy(df['long'], df['lat']),
                              crs='EPSG:4326')

    # Effettua un'operazione di "spazial join" per assegnare a ciascun punto il paese corrispondente
    points_with_country = gpd.sjoin(points, world[['geometry', 'NAME']], how='left', predicate='within')

    print("__________________________________________________________________________________________")
    print("                             COUNTRY Assignment: DONE                                  ")
    print("__________________________________________________________________________________________")

    return points_with_country



# -----------------------------------------------------------------------------------------------------------------------
#2 CORRECTION ND COUNTRY POINTS
def apply_country_corrections(df):
    """
    This function fixes all 'ND' value in the 'COUNTRY' column of the dataframe, using the Country name closest to the point coordinates.

    Input parameters:
    - df: pandas.DataFrame
        The dataframe contain all the geographic informations of the 'WKT_GEOM' and 'COUNTRY' columns.

    Returns:
    - pandas.Series
        A Pandas series wich contain the new fixed 'COUNTRY' column values.
    """
    # Convert the 'WKT_GEOM' column strings into point objects
    df['geometry'] = df['WKT_GEOM'].apply(wkt.loads).apply(Point)

    # Create a GeoDataFrame from df_NEW and specify 'geometry' as the geometry column
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Selects only points with value 'ND' in column 'COUNTRY'
    points_with_nd = gdf[gdf['COUNTRY'] == 'ND']

    # Select points without 'ND' to calculate distances
    points_without_nd = gdf[gdf['COUNTRY'] != 'ND']

    # Use BallTree to find the closest point for each point with 'ND'
    tree = BallTree(points_without_nd['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist())
    distances, indices = tree.query(points_with_nd['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist(), k=1)

    # Get the names of the correct states
    corrected_countries = gdf.loc[points_without_nd.index[indices.flatten()], 'COUNTRY'].values

    # Create a Pandas Series with the new corrected values
    corrected_series = pd.Series(corrected_countries, index=points_with_nd.index)

    # Assigns the new corrected values to the original dataframe
    df.loc[corrected_series.index, 'COUNTRY'] = corrected_series.values
    df.drop(columns=['geometry'], inplace=True)

    print("__________________________________________________________________________________________")
    print("                             COUNTRY Corrections: DONE                                  ")
    print("__________________________________________________________________________________________")

    return df['COUNTRY']

# -----------------------------------------------------------------------------------------------------------------------
#3 AFFIDABILITY CALCULATOR


def apply_affidability_calculator(df):
    # Converti la colonna 'ACCURACY' in numeri, trattando 'ND' come NaN
    df['ACCURACY'] = pd.to_numeric(df['ACCURACY'], errors='coerce')

    # Funzione di trasformazione per assegnare un valore da 1 a 10 alla colonna 'AFFIDABILITY'
    def assign_affidability(row):
        accuracy = row['ACCURACY']
        start_date = pd.to_datetime(row['START DATE'])
        end_date = pd.to_datetime(row['END DATE'])

        if pd.notna(accuracy):
            if 0 <= accuracy <= 100:
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
            elif accuracy == -99999:
                return 10


    # Applica la funzione di trasformazione alla colonna 'AFFIDABILITY'
    df['AFFIDABILITY'] = df.apply(assign_affidability, axis=1)

    # Riconverti la colonna 'ACCURACY' in stringhe, trasformando i NaN in 'ND'
    df['ACCURACY'] = df['ACCURACY'].fillna('ND')

    return df

    print("__________________________________________________________________________________________")
    print("                             AFFIDABILITY  calculation: DONE                            ")
    print("__________________________________________________________________________________________")

#4 START_DATE CORRECTION
from datetime import datetime

def trasforma_data_start(data):

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
        nuova_data = datetime.strptime(data[1:], '%Y').strftime('%Y/01/01')
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

    print("__________________________________________________________________________________________")
    print("                             START DATE  correction: DONE                            ")
    print("__________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------
#5 END DATE CORRECTION
from datetime import datetime

def trasforma_data_end(data):

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

    #Conversione da mm/yyyy a yyyy/mm/dd

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

    #Conversione da yyyy/mm a yyyy/mm/dd
    try:
        nuova_data = datetime.strptime(data, '%Y/%m')
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

    print("__________________________________________________________________________________________")
    print("                             END DATE  correction: DONE                            ")
    print("__________________________________________________________________________________________")

# ----------------------------------------------------------------------------------------------------------------------
#6 ACCURACY CORRECTION (only UAP)

def trasforma_accuracy(accuracy):

    if pd.isnull(accuracy):
        return "-99999"
    elif accuracy == 8 or accuracy == 5:
        return "0"
    elif accuracy == 3:
        return "250"
    elif accuracy == 2 or accuracy == 1:
        return "50000"
    elif accuracy == "Place name search":
        return "-99999"
    elif accuracy == "Gps measurement":
        return "0"
    elif accuracy == "Other":
        return "1000"
    elif accuracy == "Location edited by gis methods":
        return "0"
    elif accuracy == "Reported location":
        return "0"
    elif accuracy == "Map located":
        return "1000"
    elif accuracy == "Satellite imagery":
        return "0"


    print("__________________________________________________________________________________________")
    print("                             ACCURACY  correction: DONE                            ")
    print("__________________________________________________________________________________________")

# ----------------------------------------------------------------------------------------------------------------------
#7 TYPE CORRECTION
def convert_to_int(value):
    if isinstance(value, str):
        return int(value.split('.')[0])
    elif isinstance(value, (int, float)):
        return int(value)
    else:
        return value

# ----------------------------------------------------------------------------------------------------------------------
# 8 DATEs and DATEf conversion (only PCLD)

# Conversion DATEs from yyyy to yyyy/mm/dd
def date_s_correction(input_date_s):
    try:
        corrected_date = datetime.strptime(input_date_s, '%Y').strftime('%Y/01/01')
        return corrected_date
    except ValueError:
        return input_date_s
print("__________________________________________________________________________________________")
print("                             START DATE  correction: DONE                            ")
print("__________________________________________________________________________________________")

# Conversion DATEf from yyyy to yyyy/mm/dd
def date_f_correction(input_date_f):

    try:
        corrected_date = datetime.strptime(input_date_f, '%Y').strftime('%Y/12/31')
        return corrected_date
    except ValueError:
        return input_date_f
print("__________________________________________________________________________________________")
print("                             END DATE  correction: DONE                            ")
print("__________________________________________________________________________________________")
