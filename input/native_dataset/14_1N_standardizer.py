from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the CSV
df_orig = pd.read_csv(f"{root}/input/download/14_1N/1N_downloaded.csv", sep=';', low_memory=False, encoding="utf-8")

df_orig["Longitude"] = pd.to_numeric(df_orig["Longitude"], errors='coerce')
df_orig["Latitude"] = pd.to_numeric(df_orig["Latitude"], errors='coerce')
gdf_orig = gpd.GeoDataFrame(df_orig,
                            geometry=gpd.points_from_xy(df_orig["Longitude"], df_orig["Latitude"]),
                            crs='EPSG:4326')  # Set the CRS as EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

df_orig = df_orig.dropna(subset=['Latitude', 'Longitude'])

# Save the geodataframe as a CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/14_1N_native.csv", index=False)