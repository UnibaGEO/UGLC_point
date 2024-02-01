
  
# <p align="center"> UGLC Project </p>
<p align="center"> "Unified Global Landslides Catalog" </p>

----------------------------------------------------------------------------------------------------------------



## <p align="center"> AUTHORS  </p>
- [@Saverio Mancino](https://github.com/RavyHollow) - PhD Student (University of Bari).
- [@Anna Sblano](https://github.com/Anita2333) - Researcher (University of Bari).
- [@Francesco Paolo Lovergine](https://github.com/fpl) - Researcher (CNR - IREA).
- [@Giuseppe Amatulli](https://github.com/selvaje) - PhD Researcher (Yale University).

----------------------------------------------------------------------------------------------------------------
                                             IN PROGRESS
----------------------------------------------------------------------------------------------------------------

## <p align="center"> SUMMARY OF ATTRIBUTE FIELDS INCLUDED IN UGLC </p>

|        | WKT_GEOM          | NEW DATASET   | ID     | OLD DATASET   | OLD ID | VERSION   | COUNTRY   | ACCURACY   | START DATE   | END DATE   | TYPE     | TRIGGER | AFFIDABILITY | RPSV     | DPCM     | FATALITIES | INJURIES | NOTES  | LINK   |
|--------|-------------------|---------------|--------|---------------|--------|-----------|-----------|------------|--------------|------------|----------|---------|--------------|----------|----------|------------|----------|--------|--------|
| TYPE   | Well known text   | String        | Int    | String        | String | String    | String    | String     | Date         | Date       | String   | String  | Int          | Bool     | Bool     | Int        | Int      | String | String |
| STATUS | active            | Active        | Active | Active        | Active | Active    | Active    | Active     | Active       | Active     | Active   | Active  | Active       | Inactive | inactive | Active     | Active   | Active | Active |


### <p align="center"> ATTRIBUTES DESCRIPTION </p>

-----------
- <b> WKT_GEOM: </b> The contents of this field contain information about the georeferencing of each point described in the dataframe using the WGS84 reference system.
-----------
- <b> NEW DATASET: </b> the content of this field represents the name of the new dataframe's identifying abbreviation: "UGLC".
-----------
- <b> ID: </b> the content of this field represents the name of the new dataframe's identifying abbreviation: "UGLC".
-----------
  - <b> OLD DATASET: </b> the contents of this field represent the name of the native dataset using an identification abbreviation:

    - [02_COOLR](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521):
        Cooperative Open Online Landslide Repository (NASA), both Event Points and Report Points are used together, eliminating overlapping points at same coordinates [TOTAL POINTS: XXX].  
    - [03_GFLD](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521): 
        Global fatal landslide occurrence from 2004 to 2016 DA COMPLETARE

    - "04_ITALICA" eccc
   ...
-----------
- <b> OLD ID: </b> 
-----------
- <b> VERSION: </b> 
-----------
- <b> COUNTRY: </b> 
-----------
- <b> ACCURACY: </b> 
-----------
- <b> START DATE: </b> 

formato:ISO 8601:YYYY/MM/DD

-----------
- <b> END DATE: </b> 

formato:ISO 8601:YYYY/MM/DD

-----------
- <b> TYPE: </b> 
-----------
- <b> TRIGGER: </b> 
-----------
- <b> AFFIDABILITY: </b> 
-----------
- <b> RPSV: </b> 
-----------
- <b> DCMV: </b> 
-----------
- <b> FATALITIES: </b> 
-----------
- <b> INJURIES: </b> 
-----------
- <b> NOTES: </b> 
-----------
- <b> LINKS: </b> 
-----------
ID: Unique ID for each landslide

OLD DATASET: Name of the Native dataset

OLD_ID: ID point of the Native dataset

VERSION: Version of the Native dataset

COUNTRY: Country of the point

ACCURACY[m]: Accuracy in metres   

START DATE: Date of the landslides , 

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



### <p align="center"> FOLDER STRUCTURE </p>
-----------

![Dataframe Folder Structure](README_FILES/Dataframe structure v1.png)



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
