# Update Solr

A tool used to update the Solr index using local JSON files that are pushed to a specified Solr instance. The JSON files first checked for errors and will exit if any are found.

The below workflow is from JL and JM.



## Workflow

1. Must not be null:  
  `dc_title_s`  
  `dc_identifier_s`  
  `layer_slug_s`  
  `solr_geom`  
  `dct_provenance_s`  
  `dc_rights_s`  
  `geoblacklight_version`  
  `dc_creator_sm`  
  `dc_description_s`  
  `dct_references_s`  
  `dct_temporal_sm`  
  `solr_year_i`  
  `layer_modified_dt`

  - If any fields are empty then: STOP and print out list of fields missing data.

2. Check that `dc_identifier_s` and `layer_slug_s` match.

  - If different: STOP and print values.

3. Year QA

  - Do `solr_year_i` and `dct_temporal_sm` match? If not: STOP and print values.

  - Does `dc_title_s` contain `solr_year_i`? If not: STOP and print values.

  - Is the zip file named correctly? Meaning, check that `dct_references_s` `http://schema.org/downloadUrl\` key contains `solr_year_i`. Why? Sometimes mistakes happen where a file is not named correctly. If not: STOP and print values.

  - Allow for other error/QA checks in the future. Make error checking modular.

4. Check for existing UID (`dc_identifier_s`) in current Solr index. 

  - If the UID already exists, ask: Do you want to overwrite record? (yes/no/all)  
  `yes` = overwrite, check next record  
  `no` = stop  
  `all` = overwrite this and all subsequent records  



## Wish List

1. Check URLs for validity (healthy response):  
  `dc_description_s`  
  `uw_supplemental_s`  
  `dct_references_s`

  - Look for URLs in text strings and use something like curl to check.

2. Spell check on:  
  `dc_title_s`  
  `dc_description_s`  
  `uw_supplemental_s`

## Tool Arguments/Options
```
- dc = delete collection
- a  = add all JSON in folder
- r  = recursive
- dp = delete provenance
- i  = instance (prod, test, dev)
- d  = delete
- p  = purge

Removed:
- s  = scan folder for errors
- as = add single file
```