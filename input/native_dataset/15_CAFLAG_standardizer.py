import os
import geopandas as gpd
from dotenv import load_dotenv
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

# Load the shp
input_shapefile = f"{root}/input/download/15_CAFLAG/CAFLAG_DATASET/23_CAFLAG_DATASET.shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

gdf['LONGITUDE'] = pd.to_numeric(gdf['LONGITUDE'], errors='coerce')
gdf['LATITUDE'] = pd.to_numeric(gdf['LATITUDE'], errors='coerce')
df_orig = gdf.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Crea un GeoDataFrame usando 'lon' e 'lat' colonne per generare il WKT_GEOM
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['LONGITUDE'], df_orig['LATITUDE']),
                             crs='EPSG:4326')  # Set the CRS as EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Fields NaN correction and fields merging for a easier conversion
gdf['YEAR'] = gdf['YEAR'].fillna("ND")
gdf['MONTH'] = gdf['MONTH'].fillna("ND")
gdf['DAY'] = gdf['DAY'].fillna("ND")
gdf['TYPE'] = gdf.apply(lambda row: row['MAT_TYPE'] + row['MOV_TYPE'], axis=1)
gdf['CAUSE'] = gdf['CAUSE'].fillna('ND')
gdf['LOCALITY'] = gdf['LOCALITY'].fillna(' ')

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/15_CAFLAG_native.csv"
gdf.to_csv(output_csv, index=False)