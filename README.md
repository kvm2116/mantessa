# MANTESSA Pipeline

`pipeline.py` orchastrates the zmap scanning, data base insertion, bit torrent style score computation and data aggregation for mapping. 

## Database

Running pipeline requires a database to be configured as specified in `resources/scheme.txt`.
It is also important to configure the connections in the python files to work with your enviornment. 

## TODOs 

There are lots of TODOs marked in the code. Nothing is too critical, but I imagine we will need to make 
a few optimizations for this to work efficiently on 75 million records. 

List of major TODOs
* Run scan on full whitelist 
* Writeback whitelist to scan at time + 1 (when we have more data!)
* Use larger GeoJSON districts 
