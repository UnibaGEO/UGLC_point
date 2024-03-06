import zipfile
import geopandas as gpd
from dotenv import load_dotenv
import os
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")
import fiona

zip_file =  f"{root}/input/download/13_SLIDO/SLIDO R4_4.zip"

def decompress_folder(zip_file, extract_to):
    # Verifica se il file zip esiste
    if not os.path.exists(zip_file):
        print(f"Il file {zip_file} non esiste.")
        return

    # Crea la cartella di destinazione se non esiste già
    os.makedirs(extract_to, exist_ok=True)

    # Decomprimi il file zip nella cartella di destinazione
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"La cartella è stata decompressa con successo in {extract_to}")

extract_to =  f"{root}/input/download/13_SLIDO/SLIDO R4_4"
decompress_folder(zip_file, extract_to)

# Definisci il percorso del file geodatabase e il nome del layer
gdb_path = f"{root}/input/download/13_SLIDO/SLIDO R4_4/SLIDO R4_4/SLIDO Release 4_4.gdb"

layer_name = "Historic_Landslide_Points"

# Definisci il percorso di destinazione e il nome del file shapefile
output_shp = f"{root}/input/download/13_SLIDO/Historic_Landslide_Points.shp"

# Crea il file shapefile
with fiona.open(gdb_path, layer=layer_name) as src:
    # Ottieni i metadati del layer di origine
    meta = src.meta
    # Aggiungi il driver per il formato shapefile
    meta['driver'] = 'ESRI Shapefile'
    # Apri il file shapefile in modalità scrittura
    with fiona.open(output_shp, 'w', **meta) as dst:
        # Copia le caratteristiche (features) da un file all'altro
        for feature in src:
            dst.write(feature)

print("Conversione completata!")

df_orig = gpd.read_file(f"{root}/input/download/13_SLIDO/Historic_Landslide_Points.shp",decimal=".",low_memory=False,encoding="utf-8")

df_orig.to_csv(f"{root}/input/native_datasets/13_SLIDO_native.csv", sep=",", decimal=".", index=False)


print(df_orig['LOC_METHOD'].unique())
#_________________________
print(df_orig['TYPE_MOVE'].unique())
#_________________________
print(df_orig['MOVE_CLASS'].unique())
