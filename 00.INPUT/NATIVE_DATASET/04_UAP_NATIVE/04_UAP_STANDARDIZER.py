#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     UAP - Landslide Inventories across the United States version2_USGS, Mirus, B.B., Jones, E.S., Baum, R.L. et al.
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import geopandas as gpd
from geopy import Point
from shapely.geometry import Point

## IL FILE E' STATO CONVERTITO NELLA CARTELLA
# E:\UNIVERSITA'\PROGETTO PLANETEK\FRANE GLOBALI\05_Landslide Inventories across the United State version2_USGS\pythonProject1
# POICHE' I FILE SHP CON CORREDO SONO TROPPO PESANTI PER ESSERE PUSHATI SU GIT HUB

import pandas as pd
import geopandas as gpd
from geopy import Point
from shapely.geometry import Point

# Leggi il CSV utilizzando pandas
df_orig = gpd.read_file('us_ls_2_points.shp')


# Crea un GeoDataFrame utilizzando le colonne 'lon' e 'lat' per generare geometrie di tipo Punto
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['long'], df_orig['lat']),
                             crs='EPSG:4326')  # Imposta il CRS su EPSG:4326

# Aggiungi una colonna 'WKT_GEOM' con i valori WKT
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# I create a 'TRIGGER' column with the same values as df_OLD['Inventory'] to create a lookup table in 04_UAP_CONVERSION."

gdf_orig['TRIGGER']=gdf_orig['Inventory']
gdf_orig['DATEf']=gdf_orig['Date']

# Salva il GeoDataFrame in un nuovo CSV
gdf_orig.to_csv('04_UAP_NATIVE.csv', index=False)
