from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Load the CSV
df_orig = pd.read_csv(f"{root}/input/download/06_PCLD/Canadian_landslide_database_October2024_version9.csv", sep=',', low_memory=False, encoding="utf-8")

df_orig['longitude'] = pd.to_numeric(df_orig['Longitude'], errors='coerce')
df_orig['latitude'] = pd.to_numeric(df_orig['Latitude'], errors='coerce')
df_orig = df_orig.dropna(subset=['latitude', 'longitude'])

# Create a GeoDataFrame using 'lon' e 'lat' columns as WKT_GEOM source
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['longitude'], df_orig['latitude']),
                             crs='EPSG:4326')  # Set the CRS as EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Standardizing Trigger Data
gdf_orig['NEWContributo'] = gdf_orig['Contributo'].fillna('ND')
gdf_orig['NEWTrigger'] = gdf_orig['Trigger'].fillna(gdf_orig['NEWContributo'])

# Standardizing Type Data
gdf_orig['Type'] = gdf_orig['Type'].fillna('ND')

# Creating  the DATAs and DATAf fields replacing the NaT with the oldest (except for pre 1976 dates) date and the most recent
gdf_orig['DATEs'] = (gdf_orig['Timing'].fillna('1678/01/01')).astype(str)
gdf_orig['DATEf'] = (gdf_orig['Timing'].fillna('2024/10/12')).astype(str)

# Removing standard space format from some records and replacing it with '!', for and easy identification with the lookup table
gdf_orig['DATEs'] = gdf_orig['DATEs'].str.replace('\xa0', '!', regex=False)
gdf_orig['DATEf'] = gdf_orig['DATEf'].str.replace('\xa0', '!', regex=False)

# Merging the Name and Study area content, removing the NaN values
gdf_orig['Name'] = gdf_orig['Name'].fillna('ND')
gdf_orig['Study_area'] = gdf_orig['Study_area'].fillna('ND')
gdf_orig['Info'] = gdf_orig.apply(lambda row: f"{row['Study_area']}, {row['Name']}", axis=1)

#standardize ACCURACY field content
gdf_orig['Accuracy'] = gdf_orig['Location_confidence'].fillna('-99999')

gdf_orig['Reference'] = gdf_orig['Reference'].fillna('ND')

# Salva il GeoDataFrame come CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/06_PCLD_native.csv", index=False)
