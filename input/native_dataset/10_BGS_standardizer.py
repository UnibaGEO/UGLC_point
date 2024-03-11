import os
import geopandas as gpd
from dotenv import load_dotenv

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the shp
input_shapefile = f"{root}/input/download/10_BGS/LANDSLIDE_INDEX_WEB.shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
gdf['WKT_GEOM'] = gdf['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")

gdf['LOCATION'] = gdf.apply(lambda row: f"{repr(row['LOCATION'])}", axis=1)

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/10_BGS_native.csv"
gdf.to_csv(output_csv, index=False)