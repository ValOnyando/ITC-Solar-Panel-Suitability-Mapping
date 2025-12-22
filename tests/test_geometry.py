"""
Unit tests for geometry module.
"""

import pytest
import numpy as np
from shapely.geometry import Polygon
from src.geometry import (
    calculate_roof_area,
    calculate_roof_orientation,
    calculate_roof_slope,
    get_roof_vertices
)


def test_calculate_roof_area_square():
    """Test roof area calculation for a square building."""
    # Create a 10x10 meter square
    square = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    area = calculate_roof_area(square)
    
    assert area == pytest.approx(100.0, rel=1e-2)


def test_calculate_roof_area_rectangle():
    """Test roof area calculation for a rectangular building."""
    # Create a 20x10 meter rectangle
    rectangle = Polygon([(0, 0), (20, 0), (20, 10), (0, 10)])
    area = calculate_roof_area(rectangle)
    
    assert area == pytest.approx(200.0, rel=1e-2)


def test_calculate_roof_area_complex():
    """Test roof area calculation for an L-shaped building."""
    # Create an L-shaped polygon
    l_shape = Polygon([
        (0, 0), (10, 0), (10, 5),
        (5, 5), (5, 10), (0, 10)
    ])
    area = calculate_roof_area(l_shape)
    
    # Area = 10*5 + 5*5 = 75
    assert area == pytest.approx(75.0, rel=1e-2)


def test_get_roof_vertices():
    """Test extraction of roof vertices."""
    square = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    vertices = get_roof_vertices(square)
    
    assert isinstance(vertices, np.ndarray)
    assert len(vertices) == 5  # 4 corners + closing point


def test_calculate_roof_area_invalid():
    """Test handling of invalid geometry."""
    # Empty polygon should have zero area
    empty_polygon = Polygon()
    area = calculate_roof_area(empty_polygon)
    
    assert area == 0.0
