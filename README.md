# GeoData Utilities

Utilities for managing GeoData@Wisconsin.



## Setup

### Virtual Environment

You'll need to create a virtual environment to ensure compatibility with dependencies. To do this, open the "Python Command Prompt" that comes with ArcGIS Pro:

```bash
conda create --name geodata-utils python=3.11.5 --yes
activate geodata-utils
```

### Install

Install `geodatautils` using Pip directly from the GitHub repository using:

```bash
python -m pip install --upgrade https://github.com/WIStCart/geodata-utils/archive/main.tar.gz
```

### Configure Settings

Run the following to open and set `config.yml`:

```bash
for /f "delims=" %i in ('python -c "from distutils.sysconfig import get_python_lib; from os.path import join; print(join(get_python_lib(),'geodatautils','config'))"') do set configpath=%i
ren %configpath%\config-template.yml config.yml
notepad %configpath%\config.yml
```

When notepad opens, edit the 'solr instances' to fit your needs and save.



## How to Reopen Environment

When you need to open this environment in the future, open "Python Command Prompt" and run:

```bash
activate geodata-utils
```



## Tools

### `update_solr`

```text
update_solr [-h] -i INSTANCE (-a ADDFOLDER | -d DELETE | -dc DELETE_COLLECTION | -dp DELETE_PROVENANCE | -p) [-r] [--version]   

options:
  -h, --help            show this help message and exit                                                                --purge is required
  -i INSTANCE, --instance INSTANCE
                        Identify which instance of Solr to use.                                                        ecursively.
  -a ADDFOLDER, --addFolder ADDFOLDER
                        Indicate path to a single file or folder with GeoBlacklight JSON files that will be uploaded. 
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
update_solr -i geodata-test -a record.json

# Add records in directory and all subdirectories
update_solr -i geodata-test -a path/to/directory/

# Purge all records
update_solr -i geodata-test -p
```



## Development Mode

Clone the repository and change and run:

```bash
python -m pip install --editable
```



## Uninstall

To uninstall an installation of `geodatautils` run:

```bash
python -m pip uninstall geodatautils
```
