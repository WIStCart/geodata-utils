# GeoData Utilities

Utilities for managing GeoData@Wisconsin.


## Manange Installation

See [Manage Geodata Utilities Installation](docs/manage-installation.md) for information on installing, updating, and uninstalling Geodata Utils and virtual environments.


## Usage

### Reopen Environment

When you need to open this environment in the future, open "Python Command Prompt" and run:

```bash
activate geodata-utils
```

### Config

See [Configure Geodata Utilities](docs/config.md) to learn about configuring your install. You can configure Solr connections, what error checks are run, logging, and metadata schemas. 

### Tools

#### `update_solr`

```text
update_solr [-h] -i INSTANCE (-a ADD | -d DELETE | -dc DELETE_COLLECTION | -dp DELETE_PROVENANCE | -p) 
                   [-r] [--version]

options:
  -h, --help            show this help message and exit
  -i INSTANCE --instance INSTANCE
                        Identify which instance of Solr to use.
  -a ADD, --add ADD     Indicate path to a single file or folder with GeoBlacklight JSON files that will be uploaded.
  -d DELETE, --delete DELETE
                        Delete the provided unique record ID (layer_slug_s) from the Solr index.
  -dc DELETE_COLLECTION, --delete-collection DELETE_COLLECTION
                        Remove an entire collection from the Solr index.
  -dp DELETE_PROVENANCE, --delete-provenance DELETE_PROVENANCE
                        Remove all records from Solr index that belong to the specified provenance.
  -p, --purge           Delete the entire Solr index.
  -r, --recursive       [Deprecated] Recurse into subfolders when adding JSON files.
  --version             show program's version number and exit
```

Examples:
```bash
# Add record from file
update_solr -i test -a record.json

# Add records in directory and all subdirectories
update_solr -i test -a path/to/directory/

# Delete a record where layer_slug_s is a45fea1d-a45a-4cb4-85d8-4054ef70fd7f
update_solr -i test -d a45fea1d-a45a-4cb4-85d8-4054ef70fd7f

# Delete records that are part of a specific collection
update_solr -i test -dc Statewide

# Delete records of a specified provenance
update_solr -i test -dp "Some Agency"

# Purge all records
update_solr -i test -p
```

#### `gu_config`

```text
gu_config [-h] -e

options:
  -h, --help  show this help message and exit
  -e, --edit  Open Geodata Utilities config file for editing.
```

Examples:
```bash
# Open config file for editing
gu_config -e
```