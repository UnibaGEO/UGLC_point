import os
import geopandas as gpd
from dotenv import load_dotenv

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
input_shapefile = f"{root}/input/download/02_GFLD/Landslidepoints_04to17/Landslidepoints_04to17.shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
gdf['WKT_GEOM'] = gdf['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/02_GFLD_native.csv"
gdf.to_csv(output_csv, index=False)