"""Indexed Dataset Tools

Tools for indexed datasets used in geodata@wisc.
"""

import os
import logging, datetime
import json
import requests
from requests.exceptions import *
from urllib.parse import urlparse
      
def get_datasets_list(in_path:str) -> list[str]:
    """Get list of GeoJSON filenames from an input path."""

    # Datasets to check
    datasets = []

    # If input path is single file
    if os.path.isfile and os.path.splitext(in_path)[1] == ".geojson":
        datasets.append(in_path)

    # If input path is directory
    else: 
        for filename in os.listdir(in_path):

            # Get file name and extension
            f = os.path.join(in_path, filename)
            extension = os.path.splitext(filename)[1]

            # If geojson, add dataset to list
            if extension == ".geojson":
                datasets.append(f)
    
    if datasets == []:
        logging.warning("Empty dataset list. Either the file does not exist or no GeoJSONs in directory.")


    datasets_sorted = sorted(datasets)    
    return datasets_sorted

def coordinate_precision(in_path:str, out_path:str, precision:int, indentation:int, skip_feature:bool, verbose:bool) -> None:
    """Read indexed dataset GeoJSON, reduce coordinate precision, and output to specified directory."""

    def reduce_precision(dataset:str) -> None:

        # Open geojson
        with open(dataset, 'r') as f:
            data = json.load(f)

        # Lower precision of tile coordinates
        for feature in data['features']:

            # Polygon
            if feature['geometry']['type'] == 'Polygon':
                feature['geometry']['coordinates'][0] = [[round(coord, precision) for coord in coords] for coords in feature['geometry']['coordinates'][0]]

            # MultiPolygon
            elif feature['geometry']['type'] == 'MultiPolygon':
                feature['geometry']['coordinates'][0][0] = [[round(coord, precision) for coord in coords] for coords in feature['geometry']['coordinates'][0][0]]

            # Point
            elif feature['geometry']['type'] == 'Point':
                feature['geometry']['coordinates'] = [round(coord, precision) for coord in feature['geometry']['coordinates']]
            
            # Other
            else:

                # If flag to skip only feature is used
                if skip_feature:
                    logging.warning(f"{os.path.basename(dataset)} feature {data['features'].index(feature)}: Feature type {feature['geometry']['type']} is not supported. Skipping!")

                # Else skip entire dataset
                else:
                    logging.warning(f"{os.path.basename(dataset)} feature {data['features'].index(feature)}: Feature type {feature['geometry']['type']} is not supported. Skipping Dataset!")
                    return

        # Log dataset
        logging.debug(f"Updated precision of {os.path.basename(dataset)} to {precision}.")

        # Write updated json to file
        with open(os.path.join(out_path, os.path.basename(dataset)), 'w') as f:
            json.dump(data, f, indent=indentation)

        return

    # Start log
    logging.info(f"Reducing coordinate precision of datasets in {in_path}")

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Datasets to process
    datasets = get_datasets_list(in_path)

    # Make sure output path exists
    if not os.path.exists(out_path):

        # If it does not yet exist, make it
        os.mkdir(out_path)
        logging.info(f"Creating directory: {out_path}.")


    for dataset in datasets:
        reduce_precision(dataset)
    
    logging.info("Process complete.")

def check_urls(search_path:str, verbose:bool=False) -> None:
    """Check URLs in GeoJSON of indexed datasets to confirm they resolve."""
    
    # Start log
    logging.info(f"Checking URLs in {search_path}")

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Datasets to check
    datasets = get_datasets_list(search_path)
        
    # For each dataset
    for dataset in datasets:

        # Load dataset
        with open(dataset, 'r') as f:
            data = json.load(f)

        # Generate list of urls to check
        urls = []
        for feature in data['features']:
            urls.append(feature['properties']['downloadUrl'])
        
        # Create a session for this check.  This seems to avoid creating security/DDOS concerns 
        # by re-using the same connection.
        session = requests.Session()
               
        # Check each url
        logging.info(f"Checking links in {os.path.basename(dataset)}...")
        
        for url in urls:           
            try:
                response = session.head(url, timeout=5) 
                if response.status_code == 200:
                    if verbose:
                        logging.debug(f"{url}: Success")
                    else:
                        pass
                else: 
                    logging.warning(f"Not Found: {url}")
            except requests.RequestException as e:
                # exception will be thrown if the server can't be reached
                logging.error(f"Error connecting to server {urlparse(url).netloc}")
        
        session.close()

    logging.info("URL check complete.")

def minify_geojson(path:str, indentation:int):
    """Minify geojson to have no return/new lines and no indentation. Optionally choose an indentation level."""

    # Datasets to process
    datasets = get_datasets_list(path)

    # For each dataset
    for dataset in datasets:

        # Read geojson
        with open(dataset, 'r') as f:
            data = json.load(f)

        # Write with desired indent
        with open(dataset, 'w') as f:
            json.dump(data, f, indent=indentation)

def update_url(path:str, new_url:str) -> None:
    """Update websiteUrl of geojson to specified new URL."""

    # Datasets to process
    datasets = get_datasets_list(path)

    # For each dataset
    for dataset in datasets:

        # Read geojson
        with open(dataset, 'r') as f:
            data = json.load(f)
        
        # For each feature
        for feature in data['features']:

            # Update websiteUrl
            feature['properties']['websiteUrl'] = new_url

    # Write update geojson to file
    with open(dataset, 'w') as f:
            json.dump(data, f)

def remove_missing_tiles(in_path:str, out_path:str, indentation:int) -> None:
    """Remove tiles from index geojson where downloadUrl returns 404."""

    from copy import deepcopy

    # Start log
    log = logger('remove_missing_tiles_{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H%M')))
    log.start()

    # Datasets to process
    datasets = get_datasets_list(in_path)

    # For each dataset
    for dataset in datasets:

        # Open dataset
        with open(dataset, "r") as f:
            data = json.load(f)

        # Create a copy of the data to edit
        temp_data = deepcopy(data)
        
        logging.info(f"Processing {os.path.basename(dataset)}...")
        print(f"Processing {os.path.basename(dataset)}...")
        
        # Create a session for this check.  This seems to avoid creating security/DDOS concerns 
        # by re-using the same connection.
        session = requests.Session()
        
        # Iterate through each feature of data
        for feature in data['features']:                
            url = feature['properties']['downloadUrl']           
            try:
                # Check downloadUrl of each feature; HEAD request (faster than GET request as we are ignoring the body)
                response = session.head(url, timeout=5) 
                       
                # If not good, give warning and remove from geojson
                # This assumes the user has already run a url check, and is ready to pull tiles that give a 404!
                if response.status_code == 404:
                    temp_data['features'].remove(feature)
                    logging.info(f"{url} >>> Tile removed from GeoJSON index.")
                    print(f"{url} >>> Tile removed from GeoJSON index.")
            except requests.RequestException as e:
                # exception will be thrown if the server can't be reached
                print(f"Error connecting to server {urlparse(url).netloc}")
                logging.info(f"Error connecting to server {urlparse(url).netloc}")
         
        session.close()
            
        # Save updated index geojson to file
        with open(os.path.join(out_path, os.path.basename(dataset)), 'w') as f:
            json.dump(temp_data, f, indent=indentation)
    
    # End log
    log.end()