"""
Data Acquisition Module
Fetches building footprints, OSM attributes, solar irradiance, and 3D building data from external APIs.
"""
# area of intereast 

AOI = r'D:\\Master\\Q2\sci Programming for Geospatial\\Project 1\\Git clone\\ITC-Solar-Panel-Suitability-Mapping\\Data\\Raw\\AOI.geojson'
Buildings = r'D:/Master/Q2/sci Programming for Geospatial//Project 1/Git clone/ITC-Solar-Panel-Suitability-Mapping/Data/Raw/Buildings_Amsterdam.geojson'


import requests
import geopandas as gpd
from typing import Dict, List, Optional, Tuple
import json
import numpy as np
import time

def fetch_pdok_buildings(buidlings): # enter Buildsing file (shp, geojson)
    buidlings = gpd.read_file(Buildings)
    return buidlings
    


#==============================================================
# solar 
class PVGISPVCalcClient:
    """
      PV Energy = Radiation × Panel Physics × System Assumptions

   fetch Solar PV engery data from number of inputs (cordinates ,  bounding box)
    """

    BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"

    def __init__(self, peakpower=1, loss=14, timeout=30):
        self.peakpower = peakpower
        self.loss = loss
        self.timeout = timeout

    def _fetch_point(self, lat, lon):
        """
        Internal method: fetch PVGIS data for a single point.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "peakpower": self.peakpower,
            "loss": self.loss,
            "outputformat": "json",
        }

        r = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def fetch_bbox_geojson(self, bbox, step_km=1.0, sleep=0.05):
        """
        Fetch PVGIS PVcalc results for a bounding box
        and return a GeoJSON FeatureCollection.

        bbox = (min_lon, min_lat, max_lon, max_lat)
        """

        min_lon, min_lat, max_lon, max_lat = bbox
        step_deg = step_km / 111.0  # km → degrees (approx)

        features = []
        feature_id = 1

        lats = np.arange(min_lat, max_lat, step_deg)
        lons = np.arange(min_lon, max_lon, step_deg)

        for lat in lats:
            for lon in lons:
                data = self._fetch_point(lat, lon)

                feature = {
                    "type": "Feature",
                    "id": feature_id,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "E_y": data["outputs"]["totals"]["fixed"]["E_y"],
                        "loss": self.loss,
                        "source": "PVGIS PVcalc"
                    }
                }

                features.append(feature)
                feature_id += 1
                time.sleep(sleep)

        return {
            "type": "FeatureCollection",
            "features": features
        }

    def save_geojson(self, geojson, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2)


client = PVGISPVCalcClient()

bbox = (4.728, 52.278, 5.079, 52.431)  # Amsterdam

geojson = client.fetch_bbox_geojson(
    bbox=bbox,
    step_km=1.0
)

