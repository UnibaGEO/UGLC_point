import zipfile
import geopandas as gpd
from dotenv import load_dotenv
import os
import fiona

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

# - Access to the information into the geodatabase
# Load the zip files variables from config.env file
zip_file = f"{root}/input/download/13_SLIDO/SLIDO_Release_4p5_wMetadata.gdb.zip"
extract_to = f"{root}/input/download/13_SLIDO/extracted/"

# Create a destination folder (if is not present) for the unzipped file, then unzip it
if not os.path.exists(extract_to):
    os.makedirs(extract_to)

with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

# Defy the geodatabase path and layer name
gdb_path = f"{root}/input/download/13_SLIDO/extracted/SLIDO_Release_4p5_wMetadata.gdb"
layer_name = "Historic_Landslide_Points"

# Defy the destination path and the shapefile name
output_shp = f"{root}/input/download/13_SLIDO/Historic_Landslide_Points.shp"

# Create the shapefile
with fiona.open(gdb_path, layer=layer_name) as src:
    meta = src.meta
    meta['driver'] = 'ESRI Shapefile'
    with fiona.open(output_shp, 'w', **meta) as dst:
        for feature in src:
            dst.write(feature)

df_orig = gpd.read_file(f"{root}/input/download/13_SLIDO/Historic_Landslide_Points.shp", decimal=".", low_memory=False, encoding="utf-8")

# Read the shapefile into a GeoDataFrame
df_orig = gpd.read_file(output_shp, decimal=".", low_memory=False, encoding="utf-8")

# Set the CRS to EPSG 4326
df_orig = df_orig.to_crs("EPSG:4326")

#Useful conversion
df_orig['DATE_RANGEe'] = df_orig['DATE_RANGE']
df_orig['REACTIVATIe'] = df_orig['REACTIVATI']
df_orig['YEARe'] = df_orig['YEAR']
df_orig['MONTHe'] = df_orig['MONTH']
df_orig['DAYe'] = df_orig['DAY']
df_orig['MOVE_CLASS'] = df_orig['MOVE_CLASS'].fillna('ND')

# Convert geometry to WKT format
df_orig['WKT_GEOM'] = df_orig['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")

# Drop rows where "WKT_GEOM" is invalid
df_orig = df_orig[df_orig['WKT_GEOM'] != "POINT (115.49309449355307 -89.99997319935751)"]

# Save to CSV
df_orig.to_csv(f"{root}/input/native_datasets/13_SLIDO_native.csv", sep=",", decimal=".", index=False)

