Golden Wikidata [WIP]
======

The very unrefactored code to create a dataset for numerical values of Wikidata, based on 50 given DBpedia properties. 
- **map-properties.py** maps DBpedia properties to Wikidata, assumes Wikidata and DBpedia share a set of triples. It reads from *properties.csv* and writes the mapping to *wdproperties.py*
- **make-dataset.py** creates the dataset (in theory). Using **wd-query.py** it calls the Wikidata endpoint to get classes used by items using the Wikidata properties in *wdproperties.py*. The resulting triples are passed to *data-structure.py*, which sorts them by property-object pairs to limit the possible triples to 50. **create-json.py** will write the resulting dataset and its annotation to a json file that can be used.

The two scripts (map-properties and make-dataset) can be run independently. 
