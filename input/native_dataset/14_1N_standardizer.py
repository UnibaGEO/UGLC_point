from dotenv import load_dotenv
import os
import geopandas as gpd
import pandas as pd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the GeoDataFrame
gdf_orig = gpd.read_file(f"{root}/input/download/14_1N/1N_downloaded.csv", sep=';', low_memory=False, encoding="utf-8")

# Convert 'Longitude' and 'Latitude' columns to numeric, handling errors and create a WKT_GEOM column
gdf_orig["Longitude"] = pd.to_numeric(gdf_orig["Longitude"], errors='coerce')
gdf_orig["Latitude"] = pd.to_numeric(gdf_orig["Latitude"], errors='coerce')
gdf_orig['WKT_GEOM'] = gdf_orig.apply(lambda row: f"POINT ({row['Longitude']} {row['Latitude']})", axis=1)

# Duplicate the Station column for reassign it later as location reference name
gdf_orig["SiteName"] = gdf_orig["Station"]

# Drop rows with missing 'Latitude' or 'Longitude' after creating WKT_GEOM column
gdf_orig = gdf_orig.dropna(subset=['Latitude', 'Longitude'])

# Drop duplicate rows based on 'Station' column
gdf_unique_station = gdf_orig.drop_duplicates(subset=["Station"])

# Save the GeoDataFrame as a CSV
gdf_unique_station.to_csv(f"{root}/input/native_datasets/14_1N_native.csv", index=False)
