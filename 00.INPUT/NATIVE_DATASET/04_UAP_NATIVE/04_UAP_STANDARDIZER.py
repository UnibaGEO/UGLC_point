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


# Specifica il percorso del file Shapefile di input
input_shapefile = "us_ls_2_points.shp"

# Leggi il file Shapefile
gdf = gpd.read_file(input_shapefile)

# Specifica il sistema di coordinate del file Shapefile (sostituisci con il tuo sistema di coordinate)
crs_shapefile = gdf.crs

if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Crea la colonna 'WKT_GEOM' con la geometria WKT (senza dimensione Z)
gdf['WKT_GEOM'] = gdf['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")

# Elimina la colonna 'geometry' se non necessaria
# gdf = gdf.drop('geometry', axis=1)

# Specifica il percorso del file CSV di output
output_csv = "04_UAP_NATIVE.csv"


# Salva il GeoDataFrame come file CSV
gdf.to_csv(output_csv, index=False)

print("Conversione completata con successo.")
