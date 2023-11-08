from setuptools import setup, find_packages

setup(
    name='geodatautils',
    version='0.1',
    description='Utilities for managing the GeoData@Wisconsin GeoBlacklight instance.',
    author='Hayden Elza',
    license='GPLv3',
    packages=find_packages(where='geodatautils'),
    package_data={
        "geodatautils.config": ["config.yml"],
        "geodatautils.config.schemas": ["*.json"],
    },
    install_requires=['pyyaml','requests','jsonschema'],
    entry_points={
        'console_scripts': [
            'update_solr=geodatautils.interfaces:update_solr',
        ]
    }
)