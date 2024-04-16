check out this repo

run the workflow to download the data
* from standalone/worflows, run "snakemake --cores=all"
* snakemake --dag | dot -T png > workflow.png

start the standalone container to host redis and the api

bash into the container
and run load.py in a screen, it will probably take a while


check redis key count
* redis-cli info keyspace