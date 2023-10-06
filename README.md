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

## Development Mode

Change to this directory and run:

```bash
python setup.py develop
```