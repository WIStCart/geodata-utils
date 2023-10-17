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

    def delete(self, q:str="*:*") -> dict:
        """Delete records based on query."""

        data = str({'delete': {'query': q}})

        raw_response = self.update(data)

        return raw_response

    def select(self, q:str='', fl:str='') -> dict:
        """Select records based on query and field list."""

        select_url = urljoin(self.url, 'select/')

        parameters = [
            ('q', q),
            ('fl', fl)
        ]
        
        raw_response = requests.get(select_url, params=parameters, auth=(self.username, self.password)).json()

        return raw_response
    
    def update(self, data:str, commit:bool=True) -> dict:
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
        raw_response = requests.post(update_url, data=str(data), headers=headers, auth=(self.username, self.password)).json()

        return raw_response