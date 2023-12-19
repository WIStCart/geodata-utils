# Library Structure

Structure of the `geodatautils` library.

## Interfaces
`interfaces` module provides command line interfaces for Geodata utilites.

- `update_solr`  
  Interface to update a solr instance. Add records, remove records.

## Tools
These modules can be used directly if desired or indirectly using interfaces.

- `manage`  
  Manage Solr instance by updating the index.
- `schema`  
  Tools relating to the schema of geoblacklight records.

## Meta Modules
These modules are not meant to be used directly but are shared between multiple tool modules.

- `helpers`  
  Small bits of code that are common to many modules.
- `logging_config`  
  Filters and helpers to format logging as desired.
- `solr`  
  Connect to a Solr instance so that you can select or update documents.

## Proposed Modules
- `gbl`  
  GBL JSON tools
- `template`  
  templating
- `ingest`  
  gets metadata to create GBL file
- `collect`  
  data collection, download data
