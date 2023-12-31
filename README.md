# GeoData Utilities

Utilities for managing GeoData@Wisconsin.



## Setup

If you are on Windows and have ArcGIS Pro installed you can follow the directions below. For all other cases, follow the directions for a [manual setup](docs/manual-setup.md).

Open the "Python Command Prompt" that comes with ArcGIS Pro and run the following:

```bash
cd /d %USERPROFILE%/Desktop && curl -LJO https://github.com/WIStCart/geodata-utils/archive/main.tar.gz && tar -xf geodata-utils-main.tar.gz --strip=1 "geodata-utils-main/install scripts" && cd "install scripts" && install.bat && cd .. && del /s /q "geodata-utils-main.tar.gz" && rd /s /q "install scripts"
```

When notepad opens, edit the 'solr instances' to fit your needs and save. You can then close notepad.



## How to Reopen Environment

When you need to open this environment in the future, open "Python Command Prompt" and run:

```bash
activate geodata-utils
```



## Update `geodatautils` Library

```bash
python -m pip install --upgrade https://github.com/WIStCart/geodata-utils/archive/main.tar.gz
```



## Tools

### `update_solr`

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

# Purge all records
update_solr -i test -p
```



## Development Mode

Clone the repository and change and run:

```bash
python -m pip install --editable .
```



## Uninstall

To uninstall environment:

```bash
conda env remove --name geodata-utils
```

You can check what environments are installed with:

```bash
conda env list
```

If you just want to uninstall the `geodatautils` python library run:

```bash
python -m pip uninstall geodatautils
```
