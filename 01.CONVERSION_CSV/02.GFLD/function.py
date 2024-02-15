from shapely.wkt import loads
import numpy as np
import pandas as pd
import geopandas as gpd

#1
def apply_affidability_calculator(df):
    # Convert 'ACCURACY' column to numbers, treating 'ND' as NaN
    df['ACCURACY'] = pd.to_numeric(df['ACCURACY'], errors='coerce')

    # Transformation function to assign a value from 1 to 10 to the 'AFFIDABILITY' column
    def assign_affidability(row):
        accuracy = row['ACCURACY']
        start_date = pd.to_datetime(row['START DATE'])
        end_date = pd.to_datetime(row['END DATE'])

        if pd.notna(accuracy):
            if accuracy <= 100:
                if start_date == end_date:
                    return 1
                else:
                    return 2
            elif 100 < accuracy <= 250:
                if start_date == end_date:
                    return 3
                else:
                    return 4
            elif 250 < accuracy <= 500:
                if start_date == end_date:
                    return 5
                else:
                    return 6
            elif 500 < accuracy <= 1000:
                if start_date == end_date:
                    return 7
                else:
                    return 8
            elif accuracy > 1000:
                return 9
        else:  # 'ND' case
            return 10

    # Applies the transformation function to the column 'AFFIDABILITY'
    df['AFFIDABILITY'] = df.apply(assign_affidability, axis=1)

    # Reconvert the 'ACCURACY' column into strings, turning NaNs into 'NDs'
    df['ACCURACY'] = df['ACCURACY'].fillna('ND')

    print("________________________________________________________________________________________")
    print("                            AFFIDABILITY calculation: DONE                              ")
    print("________________________________________________________________________________________")

# -----------------------------------------------------------------------------------------------------------------------