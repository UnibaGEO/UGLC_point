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
input_shapefile = f"{root}/input/download/12_VLS/Landslides/18_VLS_VERMONT AGENCY OF NATURAL RESOURCES.shp"
gdf = gpd.read_file(input_shapefile)

# Set the CRS to EPSG4326
crs_shapefile = gdf.crs
if crs_shapefile != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)

# Fields NaN correction and fields merging for a easier conversion
gdf['FIELD_VISI'] = gdf['FIELD_VISI'].fillna("100")
gdf['START DATE'] = gdf.apply(lambda row: pd.to_datetime(row['FAIL_DATE'] if row['FAIL_DATE'] is not None else '1899-12-30'), axis=1)
gdf['START DATE'] = gdf['START DATE'].dt.strftime('%Y/%m/%d')
gdf['END DATE'] = gdf.apply(lambda row: pd.to_datetime(row['FAIL_DATE'] if row['FAIL_DATE'] is not None else row['VISIT_DATE'] if row['VISIT_DATE'] is not None else '2020-09-22'), axis=1)
gdf['END DATE'] = gdf['END DATE'].dt.strftime('%Y/%m/%d')
gdf['TRIGGER'] = gdf.apply(lambda row: row['CAUSE1'] if row['CAUSE1'] is not None else row['CAUSE2'] if row['CAUSE2'] is not None else 'ND', axis=1)

# Save the GeoDataFrame as a CSV
output_csv = f"{root}/input/native_datasets/12_VLS_native.csv"
gdf.to_csv(output_csv, index=False)