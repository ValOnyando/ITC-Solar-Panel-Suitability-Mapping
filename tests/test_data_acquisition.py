"""
Unit tests for data acquisition module.
"""

import pytest
from src.data_acquisition import (
    fetch_building_footprints,
    fetch_solar_irradiance,
    fetch_3d_bag_data,
    fetch_osm_building_attributes
)


def test_fetch_solar_irradiance():
    """Test PVGIS API data fetching."""
    # Utrecht coordinates
    lat, lon = 52.0907, 5.1214
    
    # TODO: Implement test
    # result = fetch_solar_irradiance(lat, lon)
    # assert result is not None
    # assert 'irradiance' in result
    pass


def test_fetch_building_footprints():
    """Test building footprint fetching."""
    bbox = (5.0, 52.0, 5.2, 52.2)  # Example bbox
    
    # TODO: Implement test
    # gdf = fetch_building_footprints(bbox)
    # assert not gdf.empty
    # assert 'geometry' in gdf.columns
    pass


def test_invalid_bbox():
    """Test handling of invalid bounding box."""
    invalid_bbox = (180, 90, 0, 0)  # Invalid order
    
    # TODO: Implement test to verify error handling
    pass
