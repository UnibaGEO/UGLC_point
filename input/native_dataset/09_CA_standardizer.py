import zipfile
import geopandas as gpd
from dotenv import load_dotenv
import os
from shapely import wkt

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Access to the information into the geodatabase
# Load the zip files variables from config.env file
zip_file = f"{root}/input/download/09_CA/Capa_Descargada.zip"
extract_to = f"{root}/input/download/09_CA/extracted/"

# Create a destination folder (if is not present) for the unzipped file, then unzip it
if not os.path.exists(extract_to):
    os.makedirs(extract_to)
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

# Read the shapefile into a GeoDataFrame
shapefile_path = f"{extract_to}/Eventos_2024-03-04/Eventos_2024-03-04.shp"
df_orig = gpd.read_file(shapefile_path, decimal=".", low_memory=False, encoding="utf-8")

# Set the CRS to EPSG4326 if not already
if df_orig.crs != 'EPSG:4326':
    df_orig = df_orig.to_crs(epsg=4326)
df_orig['TYPE'] = df_orig.apply(lambda row: row['Detonante'] + row['Tipo'], axis=1)

# Crete a GeoDataFrame using 'geometry' column for generating the WKT_GEOM
df_orig['WKT_GEOM'] = df_orig['geometry'].apply(lambda geom: f"POINT ({geom.xy[0][0]} {geom.xy[1][0]})")
df_orig['geometry'] = df_orig['WKT_GEOM'].apply(wkt.loads)

# Fill the NaN values into "Notas" with "ND"
df_orig['Notas'] = df_orig['Notas'].fillna('ND')

# Save to CSV
csv_file = f"{root}/input/native_datasets/09_CA_native.csv"
df_orig.to_csv(csv_file, sep=",", decimal=".", index=False, encoding="utf-8")