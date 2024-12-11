import os
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Directory contenente i file CSV standardizzati
directory = f"{root}/output/converted_csv/"

# List sll CSV files into the dir
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
df_combined = pd.DataFrame()

# Verifica se ci sono file CSV nella directory specificata
if csv_files:
    # Read CSV files from the list then merge em as a single dataframe
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df_temp = pd.read_csv(file_path, dtype={'VERSION': object})   # Set datatype of the col "VERSION as obj str (hotfix)
        df_combined = pd.concat([df_combined, df_temp], ignore_index=True)
else:
    print("No CSV file found in the directory.")

## ------------------ DATA CLEANING ------------------

# Data Cleaning: removes records with 'TYPE' == "snow avalanche"
df_combined = df_combined[df_combined['TYPE'] != "snow avalanche"]

## ------------------ DIRECTORY SELECTION ------------------
## G-Cloud directory
## (keep this commented when is not used)
print(f"> Saving on cloud directory")
output_file_root = f"{root}/output/"

## Local directory
## (insert your local directory)
## (keep this commented when is not used)
# print(f"> Saving on local directory")
# output_file_root = f"C:/Users/microzonazione_05/Desktop/UGLC Dataset/UGLC_point" # <--SET YOUR LOCAL DIRECTORY

## ------------------ NO DUPLICATES ------------------
# Removes duplicates based on having same 'WKT_GEOM', 'START DATE', 'END DATE' keeping the ones wth more RELIABILITY
df_cleaned = df_combined.loc[df_combined.groupby(['WKT_GEOM', 'START DATE', 'END DATE'])['RELIABILITY'].idxmin()]
df_cleaned['ID'] = [str(i) for i in range(1, len(df_cleaned) + 1)] # Generates ID

# ------------------ SINGLE CSV
# Save the duplicate-free dataframe as a csv file [FEATURE REMOVED]
output_file = f"{output_file_root}/UGLC_point.csv"
df_cleaned.to_csv(output_file, index=False, sep='|')
print(f"UGLC dataset cleaned created on '{output_file}' path with '|' as separator.")

# ------------------ TILED GPKG

# Convert the dataframe to GeoDataFrame
# Define global limits
min_lon, max_lon = -180, 180
min_lat, max_lat = -90, 90

# Calculate tile dimension (8x8 grid)
lon_step = (max_lon - min_lon) / 16
lat_step = (max_lat - min_lat) / 8

# Convert the dataframe as GeoDataFrame
gdf = gpd.GeoDataFrame(df_cleaned, geometry=gpd.GeoSeries.from_wkt(df_combined['WKT_GEOM']))

# Set the CRS to EPSG:4326 (WGS 84)
gdf.set_crs(epsg=4326, inplace=True)

# Loop on 8x8 grid's row and columns
for i in range(8):
    for j in range(8):
        # Tile frame limit
        tile_min_lon = min_lon + i * lon_step
        tile_max_lon = tile_min_lon + lon_step
        tile_min_lat = min_lat + j * lat_step
        tile_max_lat = tile_min_lat + lat_step

        # Filters points that fall within tile boundaries
        tile_gdf = gdf.cx[tile_min_lon:tile_max_lon, tile_min_lat:tile_max_lat]

        # Check if the tile contains data
        if not tile_gdf.empty:
            # Save the result as GeoPackage
            output_file_gpkg = f"{output_file_root}/UGLC_point_tile_{i}_{j}.gpkg"
            tile_gdf.to_file(output_file_gpkg, driver='GPKG')
            print(f"GeoDataFrame Tile ({i}, {j}) saved on '{output_file_gpkg}' as GeoPackage.")
        else:
            print(f"GeoDataFrame Tile ({i}, {j}) was not saved because it's empty.")

## ------------------ DUPLICATES ------------------

# Find duplicates based on having same 'WKT_GEOM', 'START DATE', 'END DATE' (same event)
duplicates = df_combined[~df_combined.index.isin(df_cleaned.index)].copy()
duplicates['ID'] = [str(i) for i in range(1, len(duplicates) + 1)] # Generates ID

# Save the duplicates as a separate csv file
duplicates_file = f"{output_file_root}/UGLC_point_duplicates.csv"
duplicates.to_csv(duplicates_file, index=False, sep='|')
print(f"Duplicates file created on '{duplicates_file}' as CSV with '|' as separator.")
