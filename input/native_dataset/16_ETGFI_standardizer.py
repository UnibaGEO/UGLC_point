import os
import geopandas as gpd
from dotenv import load_dotenv
from shapely import wkt

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
input_shapefile = f"{root}/input/download/16_ETGFI/GFDB_V4_shapefiles/24_ETGFI .shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
gdf['WKT_GEOM'] = gdf['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")
gdf['geometry'] = gdf['WKT_GEOM'].apply(wkt.loads)

# Estrai latitudine e longitudine
gdf['lat'] = gdf['geometry'].apply(lambda geom: geom.centroid.y)
gdf['long'] = gdf['geometry'].apply(lambda geom: geom.centroid.x)

# Fields NaN correction and fields merging for a easier conversion
gdf['descriptio'] = gdf['descriptio'].fillna("ND")
gdf['TYPE'] = gdf.apply(lambda row: row['type'] + row['descriptio'], axis=1)
gdf['ACCURACY'] = gdf['source_lin'].fillna('-99999')

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/16_ETGFI_native.csv"
gdf.to_csv(output_csv, index=False)
