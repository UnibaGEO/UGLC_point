
import pandas as pd
import json


import pandas as pd
import json

# Native Dataframe 02_COOLR_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/02_GFLD_NATIVE/02_UGLC_NATIVE.csv",low_memory=False)

print(df_OLD.columns.values)
print(df_OLD['Trigger'].unique())
