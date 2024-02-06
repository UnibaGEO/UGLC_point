
# <p align="center"> UGLC Project </p>
### <p align="center"> "Unified Global Landslides Catalog" </p>

----------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------
                                                        IN PROGRESS
----------------------------------------------------------------------------------------------------------------


## Authors

----------------------------------------------------------------------------------------------------------------
- [@Saverio Mancino](https://github.com/RavyHollow) - PhD Student (University of Bari).
- [@Anna Sblano](https://github.com/Anita2333) - Researcher (University of Bari).
- [@Francesco Paolo Lovergine](https://github.com/fpl) - PhD Researcher (CNR - IREA).
- [@Giuseppe Amatulli](https://github.com/selvaje) - PhD Researcher (Yale University).
- Domenico Capolongo - PhD Professor (University of Bari).

----------------------------------------------------------------------------------------------------------------

## Project description

The UGLC project aims to create a global landslide catalog as a unified dataframe from multiple global, national and regional dataframes.
inside contains information from catalogs:


----------------------------------------------------------------------------------------------------------------

## License
The whole code is published under the [MIT License](README_FILES/LICENSE.md).

----------------------------------------------------------------------------------------------------------------

## Attribute fields summary

|        | WKT_GEOM          | NEW DATASET   | ID     | OLD DATASET   | OLD ID | VERSION   | COUNTRY   | ACCURACY   | START DATE   | END DATE   | TYPE     | TRIGGER | AFFIDABILITY | RPSV     | DPCM     | FATALITIES | INJURIES | NOTES  | LINK   |
|--------|-------------------|---------------|--------|---------------|--------|-----------|-----------|------------|--------------|------------|----------|---------|--------------|----------|----------|------------|----------|--------|--------|
| TYPE   | Well known text   | String        | Int    | String        | String | String    | String    | String     | Date         | Date       | String   | String  | Int          | Bool     | Bool     | Int        | Int      | String | String |
| STATUS | active            | Active        | Active | Active        | Active | Active    | Active    | Active     | Active       | Active     | Active   | Active  | Active       | Inactive | inactive | Active     | Active   | Active | Active |

----------------------------------------------------------------------------------------------------------------

## Attributes description


- <b> WKT_GEOM: </b> The contents of this field contain information about the georeferencing of each point described in the dataframe using the WGS84 reference system.


- <b> NEW DATASET: </b> the content of this field represents the name of the new dataframe's identifying abbreviation: "UGLC".


- <b> ID: </b> the content of this field contains a unique ID for each landslide event int othe UGLC dataset.


- <b> OLD DATASET: </b> the contents of this field represent the name of the native dataset using an identification abbreviation:

    - [01_COOLR](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521):
        Cooperative Open Online Landslide Repository (NASA) (both Event Points and Report Points are used together, 
        eliminating overlapping points at same coordinates.
    
        <b>[TOTAL POINTS: 49718]</b>.  
    - [02_GFLD](https://maps.nccs.nasa.gov/arcgis/apps/MapAndAppGallery/index.html?appid=574f26408683485799d02e857e5d9521): 
        Global fatal landslide occurrence from 2004 to 2016 
    
        <b>[TOTAL POINTS: 5490]</b>. 

    - [03_ITALICA](https://zenodo.org/records/8009366): 
        ITAlian rainfall-induced LandslIdes CAtalogue (CNR - IRPI)

        <b>[TOTAL POINTS: 6312]</b>. 
    
    - [04_UAP](https://www.sciencebase.gov/catalog/item/61f326dfd34e622189b93308): 
        Landslide Inventories across the United States version2 (USGS)

        <b>[TOTAL POINTS: 176427]</b>. 

        ...



- <b> OLD ID: </b> the contents of this field represent the identifying id assigned to this row in the source dataset (if any)


- <b> VERSION: </b> the contents of this field represent the latest updated version of the original dataset used (if specified)


- <b> COUNTRY: </b> the content of this field represents the country where the event was located (where missing it was derived using its coordinates


- <b> ACCURACY: </b> the content of this field represents the precision in meters of the relative deviation of the georeferenced point from the actual landslide (if there is one)


- <b> START DATE: </b> the contents of this field represent the date of the event (if specified exactly in the source dataset) 
    and in that case it will coincide with the END DATE field (format:ISO 8601:YYYY/MM/DD).
    In case the date of the event is not present or clearly explicit, this field will contain the start date of the acquisition gap 
    of the information in the dataset, thus specifying its uncertainty.


- <b> END DATE: </b> the contents of this field represent the date of the event (if specified exactly in the source dataset) 
    and in that case it will coincide with the START DATE field (format:ISO 8601:YYYY/MM/DD).
    In case the date of the event is not present or clearly explicit, this field will contain the end date of the acquisition gap 
    of the information in the dataset, thus specifying its uncertainty.


- <b> TYPE: </b> the content of this field represents the kinematic type of the landslide event (if explicit), standardized using this reference table: 
  
    | LANDSLIDE CATEGORY   |
    |----------------------|
    | <i>(description)</i> |
    | complex              |
    | soil creep           | 
    | debris flow          |  
    | earth flow           |
    | lahar                |
    | slide                |
    | mudslide             |
    | riverbank collapse   |
    | rock slide           |
    | rock fall            |
    | rotational slide     |
    | translational slide  |
    | snow avalanche       |
    | ND                   |


- <b> TRIGGER: </b> the content of this field represents the trigger that triggered the landslide event (if explicit), standardized using this reference table:
  
    | TYPE OF TRIGGER                                | IDENTIFYING ABBREVIATION |
    |------------------------------------------------|--------------------------|
    | <i>(description)</i>                           | <i>(value)</i>           | 
    | Rainfall trigger                               | rainfall                 | 
    | Seismic trigger                                | seismic                  | 
    | Volcanic trigger                               | volcanic                 |  
    | Human-induced trigger                          | human                    | 
    | Climate temperatures trigger                   | climate                  | 
    | Postfire trigger                               | postfire                 |
    | Erosional/gravitational and biological trigger | natural                  | 
    | Unknown                                        | ND                       | 


- <b> AFFIDABILITY: </b> the content of this field represents the reliability of the data based on a decision table that takes into 
    account spatial accuracy (ACCURACY) and temporal accuracy (START DATE, END DATE):

    | SPATIAL AFFIDABILITY | TEMPORAL AFFIDABILITY          | AFFIDABILITY CLASS                | CODE           |
    |----------------------|--------------------------------|-----------------------------------|----------------|
    | <i>(meters)</i>      | <i>(START DATE = END DATE)</i> | <i>(Description)</i>              | <i>(value)</i> |
    | <100 m               | TRUE                           | Exact point                       | 1              | 
    | <100 m               | FALSE                          | Almost exact point                | 2              |
    | >100 m and <250 m    | TRUE                           | Very high reliability point       | 3              | 
    | >100 m and <250 m    | FALSE                          | High reliability point            | 4              |  
    | >250 m and <500 m    | TRUE                           | Medium reliability point          | 5              |
    | >250 m and <500 m    | FALSE                          | Low reliability point             | 6              | 
    | >500 m and <1000 m   | TRUE                           | Very low reliability point        | 7              | 
    | >500 m and <1000 m   | FALSE                          | Poor reliability point            | 8              |
    | >1000 m              | TRUE and FALSE                 | Point with uncertain reliability  | 9              | 
    | ND                   | TRUE and FALSE                 | Unreliable point                  | 10             | 


- <b> RPSV: </b> the content of this field contains the data validation flag through a comparison with the data from Radar Permanent Scatterers product from Sentinel 1 - Copernicus
    
      NOT YET IMPLEMENTED


- <b> DCMV: </b> the content of this field contains the data validation flag through a comparison with the data from DEM change maps TanDEM-X - DLR (approximately 2010 - 2022)
    
      NOT YET IMPLEMENTED


- <b> FATALITIES: </b> the content of this field contains the number of fatalities related to the event (if explicit)
  

- <b> INJURIES: </b> the content of this field contains the number of injuries related to the event (if explicit)


- <b> NOTES: </b> the content of this field contains the notes and information relate to the event (if explicit)


- <b> LINKS: </b>  the content of this field contains the link to the source of the event report or study (if explicit)

--------------------------------------------------------

## Folder Structure



--------------------------------------------------------
<img alt="Dataframe Folder Structure" src="README_FILES/Dataframe structure v1.png"/>
<p align="center"><i> Folder Structure Scheme </i></p>

--------------------------------------------------------


The entire UGLC structure is allocated in 3 main folders :
- 00.INPUT

      This folder contains the "DOWNLOADER.py" and "STANDARDIZER.py" scripts that allow the automatic download of 
      native datasets from the source sites (Entities, Government agencies, Universities, Various repositories etc.),
      the standardization of the file name (NN_DATASETNAME_NATIVE.csv format) and allocation in the subfolder named 
      "00.INPUT\NATIVE_DATAFRAMES\NN_DATASETNAME_NATIVE" sub folder.

- 01.CONVERSION_CSV

      This folder contains the different folders named after the native datasets ("NN_DATASETNAME") within the
      "NN_CONVERTER.py," "NN_FUNCTIONS.py," and "NN_LOOKUPTABLES.json" scripts which allow the filtering of the native 
      datasets and its conversion into a new dataset having the same format as the final UGLC dataframe, and will be 
      allocated in "02.OUTPUT\CONVERTED_DATAFRAMES" directory.

- 02.OUTPUT

      This folder contains the script "UNIFIER.py" that allows the union of all converted and adapted datasets 
      present in the  "02.OUTPUT\CONVERTED_DATAFRAMES" directory, into the final UGLC dataframe allocated into the 
      "FINAL_DATAFRAME" folder.

All the scripts are commanded by the "ORCHESTRATOR.py" master script in the main folder "UGLC".

Into the main folder there is also the README.txt and the sub-folder "README_FILES" wich contain all this informations and the 
pictures of the UGLC dataframe.

--------------------------------------------------------
## Requisiti

Specifica eventuali requisiti hardware o software necessari per eseguire gli script. Ad esempio:

- Python 3.6 o versioni successive
- Altri moduli o librerie specifici

--------------------------------------------------------
## Installazione

Spiega come installare eventuali dipendenze o configurare l'ambiente di lavoro per eseguire gli script.

```bash
pip install -r requirements.txt
