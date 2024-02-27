from dotenv import load_dotenv
import os
import geopandas as gpd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

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

