from dotenv import load_dotenv
import os
import geopandas as gpd

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the shp
df_orig = gpd.read_file(f"{root}/input/download/04_UAP/us_ls_2_points.shp")

# Crete a GeoDataFrame using 'lon' and 'lat' columns for generating the WKT_GEOM
gdf_orig = gpd.GeoDataFrame(df_orig,
                             geometry=gpd.points_from_xy(df_orig['long'], df_orig['lat']),
                             crs='EPSG:4326')  # Imposta il CRS su EPSG:4326
gdf_orig['WKT_GEOM'] = gdf_orig.geometry.apply(lambda geom: geom.wkt)

# Create standardized columns from the old dataset
gdf_orig['TRIGGER']=gdf_orig['Inventory']
gdf_orig['DATEf']=gdf_orig['Date']

# Save the GeoDataFrame as a CSV
gdf_orig.to_csv(f"{root}/input/native_datasets/04_UAP_native.csv", index=False)

print(gdf_orig['Fatalities'].unique())
