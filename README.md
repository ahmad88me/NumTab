NumTab
======

The following code is used for the creation of a dataset focusing on Numerical Values for, among other things, disambiguation of CSV tables to RDF. 

We base our approach on a given number of properties from DBpedia and disambiguate those to Wikidata properties, semi-automatically. We use values from Wikidata and keep the DBpedia properties. We limit the number of bags of values (columns) per property to a maximum of twenty.

The created files can be found in **gold/numtab.txt**, where each DBpedia property is followed by the number of rows of numerical values and the respective Wikidata values. In **gold/files** each bag of values gets a CSV file with an abritary ID and the property URI, encoded with + for each / in the URI. The files contain only the values. In those files, values for the property `routeNumber` are missing since they mix numerical and textual values.

** Specifications of NumTab **

| --------------------------|:----:|
| Properties used  		    | 22   |
| Max occurrences/property  | 20   |
| Total bag of values       | 224  |
| Median values/bag 		| 216  |
| Min values/bag 			| 5    |
| Min values/bag 			| 4552 |



**Used Properties and occurence**

| --------------------------|:----:|
| http://dbpedia.org/ontology/numberOfPages | 22   |
| http://dbpedia.org/ontology/routeNumber | 20   |
| http://dbpedia.org/ontology/postalCode': 7, 'http://dbpedia.org/ontology/numberOfEpisodes | 224  |
| Median values/bag 		| 216  |
| Min values/bag 			| 5    |
| Min values/bag 			| 4552 |

|DBpedia property 		   | Number of bag of values |
|--------------------------|:-----------------------:|
|http://dbpedia.org/ontology/numberOfPages | 5 |
|http://dbpedia.org/ontology/routeNumber | 11|
|http://dbpedia.org/ontology/postalCode | 7|
|http://dbpedia.org/ontology/numberOfEpisodes | 18 |
|http://dbpedia.org/ontology/runtime | 14 |
|http://dbpedia.org/ontology/elevation | 20 |
|http://dbpedia.org/ontology/deathYear | 5 |
|http://dbpedia.org/ontology/topSpeed | 2 |
|http://dbpedia.org/ontology/populationTotal | 20 |
|http://dbpedia.org/ontology/width | 20 |
|http://dbpedia.org/ontology/oclc | 11 |
|http://dbpedia.org/ontology/height | 20 |
|http://dbpedia.org/ontology/length | 20 |
|http://dbpedia.org/ontology/numberOfEmployees | 5 |
|http://dbpedia.org/ontology/numberOfGoals | 3 |
|http://dbpedia.org/ontology/number | 1 |
|http://dbpedia.org/ontology/numberOfSeasons | 9 |
|http://dbpedia.org/ontology/numberOfMatches | 3 |
|http://dbpedia.org/ontology/activeYearsEndYear | 2 |
|http://dbpedia.org/ontology/activeYearsStartYear | 2 |
|http://dbpedia.org/ontology/capacity | 7 |
|http://dbpedia.org/ontology/areaCode | 19|


## Using the code

The very unrefactored code to create a dataset for numerical values of Wikidata, based on 50 given DBpedia properties. 
- **map-properties.py** maps DBpedia properties to Wikidata, assumes Wikidata and DBpedia share a set of triples. It reads from *properties.csv* and writes the mapping to *wdproperties.py*
- **make-dataset.py** creates the dataset (in theory). Using **wd-query.py** it calls the Wikidata endpoint to get classes used by items using the Wikidata properties in *wdproperties.py*. The resulting triples are passed to *data-structure.py*, which sorts them by property-object pairs to limit the possible triples to 50. **create-json.py** will write the resulting dataset and its annotation to a json file that can be used.

The two scripts (map-properties and make-dataset) can be run independently. 

Two files are created from Wikidata dumps. In order to run **map-properties.py** with the way of creating a dump with only numerical values as in **numerical-dump.py** 80 GB of RAM are needed. (The dump created is still 10GB and is loaded in memory)

**create-dump-for-values.py** creates the dump that is needed for the creation of the dataset to look up values for the entities and the given properties.

## Mapping 

NumTab utilizes the fact that many DBpedia items are connected to Wikidata by `owl:sameAs`. However, the properties of those two ontologies are only partially connected. We chose to connect the properties with a very simplistic approach: For a given set of properties we check which triples have the same subject and object in both Wikidata and DBpedia. To test this, we chose 46 properties provided in **properties/properties.csv**.

There are quite a few limitations to map properties like this. Usually, the scope of Wikidata properties is much broader. For example, the DBpedia properties `foundingYear`, `yearOfConstruction`, `openingYear`, and `formationYear` can all be summarized by the Wikidata property *inception* (`P571`). Very broad properties such as `year` in DBpedia do not have an equivalent in Wikidata. Beside being only able to look for values that have a subject that is disambiguated to Wikidata in DBpedia, another limitation is the way how statements in Wikidata are formed compared to Wikidata. Those rather broad properties in Wikidata are usually limited by so called *qualifier*, that make a statement valid for a certain condition. So can for example multiple population numbers for a city be limited in their validation to a certain time frame (using *start time* (`P580`) and *end time* (`P582`). Another example is the DBpedia property `service start year`. While DBpedia describes such cases with a dedicated property, Wikidata makes use of its properties to describe the enrolment in a service and qualifies it with an end and start time.

## Building the dataset
To build NumTab, we used the automatic mappings between Wikidata and DBpedia, enriched by manual mappings, which can be found in **properties/properties-all**.
We limited them to only those properties that we could unambiguously match to DBpedia. Therefore we base our work on those $22$ Wikidata properties. Those can be found in **properties/properties-unambigious**.
The goal for NumTab is to archive a dataset, where the values in one column are strongly interconnected. That means, they should have the same context. For example, we are not only looking for values, that use the property *height* (`P2048`) and are of the same *instance of* (`P31`), such as sculpture (`Q860861`). We look into more connections. 
That means, we cluster all triples, that use the given properties by their types. We limit the classes, to such that have between 100 and 5000 instances using [Wikidata's SPARQL endpoint](https://query.wikidata.org/) and select 20 of those clusters. For each cluster, we look at the most common property-object pair. In the previous mentioned example of sculptures, that could be all *sculptures* (`Q860861`) that are *part of the movement* (`P135`) *Art Nouveau* (`Q34636`). From all items sharing the most common property-object pair, we extract the numerical value for the one of our 17 properties and add them to a column labelled by the corresponding DBpedia property.



