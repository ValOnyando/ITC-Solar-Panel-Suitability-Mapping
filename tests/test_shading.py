"""
Unit tests for shading analysis.
"""

import pytest
import numpy as np
from src.shading import calculate_shadow_length


def test_calculate_shadow_length_45_degrees():
    """Test shadow length at 45° sun elevation."""
    building_height = 10  # meters
    sun_elevation = 45  # degrees
    
    shadow_length = calculate_shadow_length(building_height, sun_elevation)
    
    # At 45°, shadow length equals building height
    assert shadow_length == pytest.approx(10.0, rel=1e-2)


def test_calculate_shadow_length_30_degrees():
    """Test shadow length at 30° sun elevation."""
    building_height = 10
    sun_elevation = 30
    
    shadow_length = calculate_shadow_length(building_height, sun_elevation)
    
    # shadow = height / tan(30°) = 10 / 0.577 ≈ 17.32
    assert shadow_length == pytest.approx(17.32, rel=1e-2)


def test_calculate_shadow_length_60_degrees():
    """Test shadow length at 60° sun elevation."""
    building_height = 10
    sun_elevation = 60
    
    shadow_length = calculate_shadow_length(building_height, sun_elevation)
    
    # shadow = height / tan(60°) = 10 / 1.732 ≈ 5.77
    assert shadow_length == pytest.approx(5.77, rel=1e-2)


def test_calculate_shadow_length_zero_elevation():
    """Test shadow length at zero sun elevation (horizon)."""
    shadow_length = calculate_shadow_length(10, 0)
    assert shadow_length == 0.0


def test_calculate_shadow_length_90_degrees():
    """Test shadow length at 90° (sun directly overhead)."""
    shadow_length = calculate_shadow_length(10, 90)
    assert shadow_length == 0.0
