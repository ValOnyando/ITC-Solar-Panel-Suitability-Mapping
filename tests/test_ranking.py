"""
Unit tests for ranking and suitability scoring.
"""

import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from src.ranking import (
    calculate_suitability_score,
    classify_building_suitability,
    rank_buildings
)


def test_calculate_suitability_score_excellent():
    """Test suitability score for an excellent building."""
    score = calculate_suitability_score(
        roof_area=500,        # Large roof
        energy_potential=50000,  # High energy
        shading_factor=0.0,   # No shading
        orientation=180       # South-facing
    )
    
    # Should get high score
    assert score >= 80


def test_calculate_suitability_score_poor():
    """Test suitability score for a poor building."""
    score = calculate_suitability_score(
        roof_area=20,         # Small roof
        energy_potential=1000,   # Low energy
        shading_factor=0.8,   # Heavy shading
        orientation=0         # North-facing
    )
    
    # Should get low score
    assert score < 40


def test_classify_building_suitability_excellent():
    """Test classification of excellent buildings."""
    category = classify_building_suitability(85)
    assert category == "Excellent"


def test_classify_building_suitability_good():
    """Test classification of good buildings."""
    category = classify_building_suitability(65)
    assert category == "Good"


def test_classify_building_suitability_moderate():
    """Test classification of moderate buildings."""
    category = classify_building_suitability(50)
    assert category == "Moderate"


def test_classify_building_suitability_poor():
    """Test classification of poor buildings."""
    category = classify_building_suitability(25)
    assert category == "Poor"


def test_classify_building_suitability_unsuitable():
    """Test classification of unsuitable buildings."""
    category = classify_building_suitability(10)
    assert category == "Unsuitable"


def test_rank_buildings():
    """Test building ranking functionality."""
    # Create sample GeoDataFrame
    data = {
        'building_id': [1, 2, 3, 4, 5],
        'suitability_score': [85, 45, 92, 30, 67],
        'geometry': [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)]
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")
    
    ranked = rank_buildings(gdf)
    
    # Check that buildings are ranked correctly
    assert ranked.iloc[0]['building_id'] == 3  # Score 92
    assert ranked.iloc[1]['building_id'] == 1  # Score 85
    assert ranked.iloc[2]['building_id'] == 5  # Score 67
    assert ranked.iloc[3]['building_id'] == 2  # Score 45
    assert ranked.iloc[4]['building_id'] == 4  # Score 30
    
    # Check rank column
    assert list(ranked['rank']) == [1, 2, 3, 4, 5]
