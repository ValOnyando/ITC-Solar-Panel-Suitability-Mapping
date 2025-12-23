"""
Data Acquisition Module
Fetches building footprints, OSM attributes, solar irradiance, and 3D building data from external APIs.
"""

import requests
import geopandas as gpd
from typing import Dict, List, Optional
import json

# tests 
print ("test12")

def fetch_building_footprints(bbox: tuple, source: str = "osm") -> gpd.GeoDataFrame:
    """
    Fetch building footprints from various sources.
    
    Parameters
    ----------
    bbox : tuple
        Bounding box (min_lon, min_lat, max_lon, max_lat)
    source : str
        Data source: 'osm', 'microsoft', etc.
    
    Returns
    -------
    gpd.GeoDataFrame
        Building footprint geometries
    """
    # TODO: Implement API call to fetch building footprints
    pass


def fetch_solar_irradiance(lat: float, lon: float) -> Dict:
    """
    Fetch solar irradiance data from PVGIS API.
    
    Parameters
    ----------
    lat : float
        Latitude
    lon : float
        Longitude
    
    Returns
    -------
    dict
        Solar irradiance data in GeoJSON format
    """
    url = f"https://re.jrc.ec.europa.eu/api/PVcalc"
    params = {
        'lat': lat,
        'lon': lon,
        'outputformat': 'json',
        'browser': 0
    }
    
    # TODO: Implement PVGIS API call
    pass


def fetch_3d_bag_data(bbox: tuple) -> gpd.GeoDataFrame:
    """
    Fetch 3D building data from PDOK 3D BAG.
    
    Parameters
    ----------
    bbox : tuple
        Bounding box (min_lon, min_lat, max_lon, max_lat)
    
    Returns
    -------
    gpd.GeoDataFrame
        3D building data with roof heights
    """
    # TODO: Implement 3D BAG API call
    pass


def fetch_osm_building_attributes(bbox: tuple) -> gpd.GeoDataFrame:
    """
    Fetch building attributes from OpenStreetMap.
    
    Parameters
    ----------
    bbox : tuple
        Bounding box (min_lon, min_lat, max_lon, max_lat)
    
    Returns
    -------
    gpd.GeoDataFrame
        Building attributes (height, type, etc.)
    """
    # TODO: Implement OSM Overpass API call
    pass
