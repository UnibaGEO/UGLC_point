from dotenv import load_dotenv
import os
import geopandas as gpd

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
df_orig = gpd.read_file(f"{root}/input/download/05_ALC/LandslideAustraliaCatalogue/AusLandCat.shp")
df_orig = df_orig.rename(columns=lambda x: x.replace('\n', ' '))

# Create a GeoDataFrame using 'lon' and 'lat' columns for generating the WKT_GEOM
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['Longitude'], df_orig['Latitude']),
                             crs='EPSG:4326')  # Imposta il CRS su EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Create standardized columns from the old dataset


# Save the GeoDataFrame as a CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/05_ALC_native.csv", index=False)

