[![Build Status](https://travis-ci.com/TranslatorIIPrototypes/NodeNormalization.svg?branch=master)](https://travis-ci.com/TranslatorIIPrototypes/NodeNormalization)

# NodeNormalization

## Introduction

Node normalization takes a CURIE, and returns:

* The preferred CURIE for this entity
* All other known equivalent identifiers for the entity
* Semantic types for the entity as defined by the [Biolink Model](https://biolink.github.io/biolink-model/)

The data currently served by Node Normalization is created by the prototype project
[Babel](https://github.com/TranslatorSRI/Babel), which attempts to find identifier equivalences,
and makes sure that CURIE prefixes are BioLink Model compliant.  The NodeNormalization service, however,
is independent of Babel and as improved identifier equivalence tools are developed, their results
can be easily incorporated.

To determine whether Node Normalization is likely to be useful, check /get_semantic_types, which lists the BioLink
semantic types for which normalization has been attempted, and /get_curie_prefixes,
which lists the number of times each prefix is used for a semantic type.

For examples of service usage, see the example [notebook](documentation/NodeNormalization.ipynb).

The Node normalization website leverages the [R3 (Redis-REST with referencing)](https://github.com/TranslatorSRI/r3) Redis data design and configuration. 

Users can find the publicly available website at [service](https://nodenormalization-sri.renci.org/docs).

## Installation

Create a virtual environment

    > python -m venv nodeNormalization-env

Activate the virtual environment

    # on Linux
    $ source nodeNodemaization-env/bin/activate
    # on Windows
    > source nodeNormalization-env/Scripts/activate 

Install requirements 

    > pip install -r requirements.txt

## Fetching equivalence data

The equivalence data can be generated by running [Babel](https://github.com/TranslatorSRI/Babel).

An example of the contents of a compendia file is shown below:

    {"id": {"identifier": "PUBCHEM:50986940"}, "equivalent_identifiers": [{"identifier": "PUBCHEM:50986940"}, {"identifier": "INCHIKEY:CYMOSKLLKPIPCD-UHFFFAOYSA-N"}], "type": ["chemical_substance", "named_thing", "biological_entity", "molecular_entity"]}
    {"id": {"identifier": "CHEMBL.COMPOUND:CHEMBL1546789", "label": "CHEMBL1546789"}, "equivalent_identifiers": [{"identifier": "CHEMBL.COMPOUND:CHEMBL1546789", "label": "CHEMBL1546789"}, {"identifier": "PUBCHEM:4879549"}, {"identifier": "INCHIKEY:FUIYIXDZTPMQEH-UHFFFAOYSA-N"}], "type": ["chemical_substance", "named_thing", "biological_entity", "molecular_entity"]}

## Creating and loading a Redis container with data 

A running instance of Redis is needed to house the node normalization data. a Redis Docker container image can be downloaded from [Docker hub](https://hub.docker.com/_/redis). The Redis caonteriner can be started with thie following docker command:

Note that the dataset for Node normalization is quite large and 256Gb of memory and disk space should be made available to the Redis instance to insure proper loading of the complete compendia.

    docker run --name node-norm -p 6379:6379 -d redis redis-server --appendonly yes

### Configuration
Insure that the `./config.json` file is created and contains the parameters for the node normalization load specific to your environment. 

The configuration parameters `compendium_directory` and `data_files` specify the location of the compendia files. An example of the files' contents  
are listed below:

    {
        "compendium_directory": "<path to files>",
        "data_files": "anatomy.txt,BiologicalProcess.txt,cell.txt,cellular_component.txt,disease.txt,gene_compendium.txt,gene_family_compendium.txt,MolecularActivity.txt,pathways.txt,phenotypes.txt,taxon_compendium.txt",
        "redis_host": "<Redis host server name>",
        "redis_port": <Redis connection port>,
        "redis_password": "<Redis password",
        "test_mode": 1,
        "debug_messages": 0
    }

### Loading of the Redis server with compendia data

The load.py script reads the configuration file for load parameters and the loads the compendia data into the Redis instance. 

#### The redis command line can be used to monitor various aspects of the load.

It is possible to observer the progress of the load opening a command line _within the container_ and issuing Redis commands.

_View the number of keys loaded so far._
 ```
    redis-cli info keyspace
```

_Once the database has completed loading it is recommended that the Redis database be persisted to disk._ 

```
    redis-cli save
```

_Monitor the database to determine if the save has completed._

```
    redis-cli info persistence
```

### Starting the FASTAPI webserver

The web server can be started after successful completion of the load.

```
pip install -r requirements.txt

uvicorn --host 0.0.0.0 --port 8000 --workers 1 node_normalizer.server:app
```

Then navigate to http://localhost:8000/docs

### Kubernetes configurations
    kubernetes configurations and helm charts for this project can be found at: 

    https://github.com/helxplatform/translator-devops/helm/r3
  
