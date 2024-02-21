#-----------------------------------------------------------------------------------------------------------------------
# native dataframe: ITALICA
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import geopandas as gpd
import pandas as pd

# Leggi il CSV utilizzando pandas
df_orig = pd.read_csv('ITALICA-v2.csv', sep=';')

print(df_orig.head)

# Crea un GeoDataFrame utilizzando le colonne 'lon' e 'lat' per generare geometrie di tipo Punto
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['lon'], df_orig['lat']),
                             crs='EPSG:4326')  # Imposta il CRS su EPSG:4326

# Aggiungi una colonna 'WKT_GEOM' con i valori WKT
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Seleziona le colonne necessarie
df_output = gdf_orig[['WKT_GEOM', 'id', 'landslide_type', 'municipality', 'province', 'region', 'geographic_accuracy', 'utc_date']]

# Salva il GeoDataFrame in un nuovo CSV
df_output.to_csv('03_ITALICA_native.csv', index=False)







