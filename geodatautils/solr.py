"""Solr Interface

Connect to a Solr instance so that you can select or update documents.
"""


import requests  # I chose requests over urllib because although it adds another dependency, it greatly simplifies working with solr
from requests.compat import urljoin
from geodatautils import config


class Solr:
    """Create an object representing a connection to a Solr instance."""

    def __init__(self, instance_name:str) -> None:
        """Initiate Solr object with settings from config."""

        self.url = config['solr instances'][instance_name]['url']
        self.username = config['solr instances'][instance_name]['username']
        self.password = config['solr instances'][instance_name]['password']
        self.name = instance_name
        
        """Max URI size in Kilobytes (KB)
        8 Kilobytes is max, but give 1KB wiggle room for headers
        TODO: I could not figure out the exact amount need for headers, adjust if you can figure it out -HE
        """
        self.max_uri_size = 7*1024

    def build_query_chunks(self, items:list[str], target_chunk_size:int) -> list[str]:
        """For queries that exceed max URI size, chunk out query into smaller pieces."""

        # Initialize chunks
        chunks = []
        
        # Loop until all items are chunked
        while items:

            # Initialize chunk
            chunk = items.pop(0)

            # Build chunks
            while items:

                # If next item fits, add it
                if len(chunk + items[0]) < target_chunk_size:
                    chunk += " " + items.pop(0)
                
                # Oterwise finish chunk
                else:
                    break
            
            # Store chunk in list
            chunks.append(chunk)
            
        return chunks
    
    def delete(self, q:str="*:*") -> requests.models.Response:
        """Delete records based on query."""

        data = str({'delete': {'query': q}})

        raw_response = self.update(data)

        return raw_response

    def select(self, q:str='*:*', fq:str=None, rows:int=None, fl:str=None) -> requests.models.Response:
        """Select records based on query and field list."""

        select_url = urljoin(self.url, 'select/')

        parameters = [
            ('q', q),
            ('fq', fq),
            ('rows', rows),
            ('fl', fl)
        ]

        # Query solr instance
        raw_response = requests.get(select_url, params=parameters, auth=(self.username, self.password))

        return raw_response
    
    def update(self, data:str, commit:bool=True) -> requests.models.Response:
        """Use supplied list of records to update Solr instance."""

        # Build parameters
        parameters = []
        
        if commit:
            parameters.append("commit={}".format(str(bool(commit)).lower()))

        # Put parameters together with path
        if parameters:
            path = "update?{}".format("&".join(parameters))

        # Construct update url
        update_url = urljoin(self.url, path)
      
        # Set headers
        headers = {"Content-Type":"application/json"}
        
        # Post records to solr
        raw_response = requests.post(update_url, data=str(data).encode(), headers=headers, auth=(self.username, self.password))
        
        return raw_response
        