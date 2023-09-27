from setuptools import setup, find_packages

setup(
    name='GeoData Utils',
    version='0.1',
    description='Utilities for managing the GeoData@Wisconsin GeoBlacklight instance.',
    author='Hayden Elza',
    license='GPLv3',
    packages=find_packages(where='geodatautils'),
    install_requires=['python-dotenv','pyyaml'],
    entry_points={
        'console_scripts': [
            'update_solr=geodatautils.interfaces:update_solr',
        ]
    }
)