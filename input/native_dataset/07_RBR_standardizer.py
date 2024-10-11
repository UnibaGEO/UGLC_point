from dotenv import load_dotenv
import os
import geopandas as gpd
from lib.function_collection import convert_to_int

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
df_orig = gpd.read_file(f"{root}/input/download/07_RBR/landslide_data/08_RBR_REPUBBLICA DOMENICANA DEL CONGO.shp",decimal=".",low_memory=False,encoding="utf-8")

#Add the column WKT_GEOM
df_orig['WKT_GEOM'] = df_orig['geometry'].apply(lambda geom: geom.wkt)

df_orig['long'] = df_orig['geometry'].x
df_orig['lat'] = df_orig['geometry'].y
print(df_orig['long'].dtypes)

df_orig['ID'] = df_orig['ID'].apply(convert_to_int)
df_orig['Year']=df_orig['Year'].apply(convert_to_int)
df_orig['area']=df_orig['area'].apply(convert_to_int)
df_orig['dep_area']=df_orig['dep_area'].apply(convert_to_int)

# Create standardized columns from the old dataset
df_orig['Country']= "calc"

# Save the GeoDataFrame as a CSV
df_orig.to_csv(f"{root}/input/native_datasets/07_RBR_native.csv", sep=",", decimal=".", index=False)

