# GeoData Utilities

Utilities for managing GeoData@Wisconsin.



## Setup

### Virtual Environment

This is optional, but necessary if you have conflicting packages on your system that you need for other projects.

Change directories to the repository, then run:

```bash
conda create --name geodata-utils python=3.11.5
conda activate geodata-utils
```

### Install

Pip Install via Git
```bash

```

Change to this directory and run:

```bash
python setup.py install
```

### Configure Settings

Using `config/config-template.yml` as a starting point, edit the 'solr instances' to fit your needs and save as `config/config.yml`.



## Tools

### `update_solr`

```text
update_solr [-h] -i INSTANCE
            (-a ADDFOLDER | -d DELETE | -dc DELETE_COLLECTION | -dp DELETE_PROVENANCE | -p) [-r] [--version]    

options:
  -h, --help            show this help message and exit
  -i INSTANCE, --instance INSTANCE
                        Identify which instance of Solr to use.
  -a ADDFOLDER, --addFolder ADDFOLDER
                        Indicate path to folder with GeoBlacklight JSON files that will be uploaded.
  -d DELETE, --delete DELETE
                        Delete the provided unique record ID (layer_slug) from the Solr index.
  -dc DELETE_COLLECTION, --delete-collection DELETE_COLLECTION
                        Remove an entire collection from the Solr index.
  -dp DELETE_PROVENANCE, --delete-provenance DELETE_PROVENANCE
                        Remove all records from Solr index that belong to the specified provenance.
  -p, --purge           Delete the entire Solr index.
  -r, --recursive       Recurse into subfolders when adding JSON files.
  --version             show program's version number and exit
```

Examples:
```bash
# Add record from file
update_solr -i geodata-test -a record.json

# Add records in directory
update_solr -i geodata-test -a path/to/directory/

# Purge all records
update_solr -i geodata-test -p
```



## Development Mode

Change to this directory and run:

```bash
python setup.py develop
```