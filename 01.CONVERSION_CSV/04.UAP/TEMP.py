
import pandas as pd
import json
import numpy as np
from opencage.geocoder import OpenCageGeocode



# Native Dataframe 02_GFLD_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/04_UAP_NATIVE/04_UAP_NATIVE.csv",low_memory=False)

print((df_OLD).columns.values)

print(df_OLD['Inventory'].unique())

print(df_OLD['Date'].unique())