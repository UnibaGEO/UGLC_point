from dotenv import load_dotenv
import os
import geopandas as gpd
from shapely.wkt import loads

# Load the environment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Load the shp
df_orig = gpd.read_file(f"{root}/input/download/07_RBR/landslide_data/08_RBR_REPUBBLICA DOMENICANA DEL CONGO.shp",decimal=".",low_memory=False,encoding="utf-8")

#Add the column WKT_GEOM
df_orig['WKT_GEOM'] = df_orig['geometry'].apply(lambda geom: geom.wkt)

df_orig['long'] = df_orig['geometry'].x
df_orig['lat'] = df_orig['geometry'].y
print(df_orig['long'].dtypes)
def convert_to_int(value):
    if isinstance(value, str):
        return int(value.split('.')[0])
    elif isinstance(value, (int, float)):
        return int(value)
    else:
        return value  # Se il tipo non è una stringa, un intero o un float, mantieni il valore originale

df_orig['ID'] = df_orig['ID'].apply(convert_to_int)
df_orig['Year']=df_orig['Year'].apply(convert_to_int)
df_orig['area']=df_orig['area'].apply(convert_to_int)
df_orig['dep_area']=df_orig['dep_area'].apply(convert_to_int)

# Create standardized columns from the old dataset
df_orig['Country']= "calc"
row_with_id=df_orig.loc[df_orig['ID'] == 1513]
print(row_with_id)

# Save the GeoDataFrame as a CSV
df_orig.to_csv(f"{root}/input/native_datasets/07_RBR_native.csv", sep=",", decimal=".", index=False)

