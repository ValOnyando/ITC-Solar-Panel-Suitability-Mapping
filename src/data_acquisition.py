"""
Data Acquisition Module
Fetches building footprints, OSM attributes, solar irradiance, and 3D building data from external APIs.
"""

import requests
import geopandas as gpd
from typing import Dict, List, Optional
import json


def fetch_pdok_buildings(
    limit: int = 500,
    filter_bbox: Optional[Tuple[float, float, float, float]] = None,
    base_url: str = (
        "https://api.pdok.nl/kadaster/3d-basisvoorziening/ogc/v1/collections/hoogtestatistieken_gebouwen/items" )
) -> gpd.GeoDataFrame:
    """
    retrieving PDOK building features with height and roof attributes
    from 'hoogtestatistieken_gebouwen', using OGC API. 

    Parameters
    ----------
    limit : int
        Number of features per page.
    filter_bbox : tuple or None
        (min_lon, min_lat, max_lon, max_lat) in EPSG:4326.
        Applied client-side after download.
    base_url : str
        OGC API endpoint for the collection.

    Returns
    -------
    gpd.GeoDataFrame
    """

    params = {
        "limit": limit,
        "f": "json"
    }

    all_features = []
    url = base_url

    while url:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        all_features.extend(data.get("features", []))

        # OGC API link-based pagination
        next_url = None
        for link in data.get("links", []):
            if link.get("rel") == "next":
                next_url = link.get("href")
                break

        url = next_url
        params = None  # next URL already contains params

    # Build GeoDataFrame in native CRS (EPSG:28992)
    gdf = gpd.GeoDataFrame.from_features(
        all_features,
        crs="EPSG:28992"
    )

    # Client-side bbox filter (if provided)
    if filter_bbox:
        xmin, ymin, xmax, ymax = filter_bbox
        gdf = gdf.cx[xmin:xmax, ymin:ymax]

    return gdf

#==============================================================

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


