# UGLC Project
UNIFIED GLOBAL LANDSLIDES CATALOG

Authors: Saverio Mancino, Anna Sblano
--------------------------------------------------------
                   IN PROGRESS
--------------------------------------------------------

## SUMMARY OF FIELDS INCLUDED IN UGLC
--------------------------------------------------------
WKT_GEOM: POINT (LONG LAT)

NEW DATASET: UGLC (name of our new dataset)

ID: Unique ID for each landslide

OLD DATASET: Name of the Native dataset

OLD_ID: ID point of the Native dataset

VERSION: Version of the Native dataset

COUNTRY: Country of the point

ACCURACY[m]: Accuracy in metres   

START DATE: Date of the landslides , formato:ISO 8601:YYYY/MM/DD

END DATE: Date of the landslides, format: ISO 8601: YYYY/MM/DD. If we have the exact date of the landslides we will have the start date = end date,
however if we only have the year or period of acquisition of the landslide we will have the start date different from the end date and therefore we
will have the interval in the time in which the landslide probably occurred

TYPE: Type of landsdlise if known and include: complex,soil creep,debris flow,earth flow,lahar,slide,mudslide,riverbank collapse,rock slide,rock fall,rotational slide,
translational slide,snow avalanche,not defined

TRIGGER:Type of trigger if known and include: rainfall,seismic,volcanic,human,climate,not defined

AFFIDABILITY: 1:exact point , 2:Almost exact point , 3:Very high reliability point, 4:High reliability point, 5:Medium reliability point, 6:Low reliability point,
7:Very low reliability point, 8:Poor reliability point, 9: Uncertain reliability point, 10:Not reliable point

PSV:

DCMV:

FATALITIES:

INJURIES:

NOTES:

LINK:

--------------------------------------------------------

# UGLC Project

Unified Global Landslides Catalog.
--------------------------------------------------------
                   IN PROGRESS
--------------------------------------------------------

## Descrizione

The UGLC project aims to create a global landslide catalog as a unified dataframe from multiple global, national and regional dataframes.
inside contains information from catalogs:
- 
-
-


## Requisiti

Specifica eventuali requisiti hardware o software necessari per eseguire gli script. Ad esempio:

- Python 3.6 o versioni successive
- Altri moduli o librerie specifici

## Installazione

Spiega come installare eventuali dipendenze o configurare l'ambiente di lavoro per eseguire gli script.

```bash
pip install -r requirements.txt
