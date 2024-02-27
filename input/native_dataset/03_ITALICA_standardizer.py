import geopandas as gpd
import pandas as pd
from dotenv import load_dotenv
import os

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# ITALICA -----------------------------------------------------------------------

# CSV read
df_orig = pd.read_csv(f"{root}/input/download/03_ITALICA/ITALICA-v2.csv", sep=';')

# Crete a GeoDataFrame using 'lon' and 'lat' columns for generating the WKT_GEOM
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['lon'], df_orig['lat']),
                             crs='EPSG:4326')  # Imposta il CRS su EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Save the GeoDataFrame as a CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/03_ITALICA_native.csv", index=False)







