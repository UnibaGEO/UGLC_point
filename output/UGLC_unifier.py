import os
import pandas as pd
from dotenv import load_dotenv

# Load the environment variables from config.env file
load_dotenv("../config.env")
root = os.getenv("FILES_REPO")

# Directory contenente i file CSV standardizzati
directory = f"{root}/output/converted_csv/"

# Lista dei file CSV nella directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# DataFrame iniziale vuoto
df_combined = pd.DataFrame()

# Leggi tutti i file CSV e uniscili in un unico DataFrame
for file in csv_files:
    file_path = os.path.join(directory, file)
    df_temp = pd.read_csv(file_path, dtype={'VERSION': object})  # Imposta il tipo di dati della colonna "VERSION" come object (stringa)
    df_combined = pd.concat([df_combined, df_temp], ignore_index=True)

df_combined['ID'] = ['P-' + str(i) for i in range(1, len(df_combined) + 1)]

# Verifica se ci sono file CSV nella directory specificata
if csv_files:
    # Salva il DataFrame combinato in un nuovo file CSV
    output_file = f"{root}/output/UGLC.csv"
    df_combined.to_csv(output_file, index=False)
    print(f"UGLC dataset created on '{output_file}' path")
else:
    print("No CSV file found tino the directory.")
