#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     GFLD - Global fatal landslide occurrence from 2004 to 2016, Froude, M. J. and Petley, D. N
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import geopandas as gpd
from geopy import Point
from shapely.geometry import Point


# Specifica il percorso del file Shapefile di inputt
input_shapefile = "../00.INPUT/NATIVE_DATASET/02_GFLD_NATIVE/Landslidepoints_GFLD.shp"

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
output_csv = "../00.INPUT/NATIVE_DATASET/02_GFLD_NATIVE/02_UGLC_NATIVE.csv"


# Salva il GeoDataFrame come file CSV
gdf.to_csv(output_csv, index=False)

print("Conversione completata con successo.")

#-----------------------------------------------------------------------------------------------------------------------
# native dataframe: ITALICA
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import geopandas as gpd

# Leggi il file CSV originale con geometrie
df_orig = gpd.read_file('00.INPUT/NATIVE_DATASET/03_ITALICA_NATIVE/ITALICA-v2.csv')

# Aggiungi una colonna con i valori WKT_GEOM
df_orig['WKT_GEOM'] = df_orig.geometry.apply(lambda geom: geom.wkt)

# Seleziona solo le colonne necessarie, includendo la nuova colonna WKT_GEOM
df_output = df_orig[['WKT_GEOM', 'altra_colonna', 'ancora_una_colonna']]

# Salva il nuovo DataFrame in un file CSV
df_output.to_csv('00.INPUT/NATIVE_DATASET/03_ITALICA_NATIVE/03_ITALICA_NATIVE.csv', index=False)



#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
