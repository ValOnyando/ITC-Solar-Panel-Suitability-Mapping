"""
Spatial Search Module
Implements spatial search algorithms including KD-tree for efficient nearest neighbor queries.
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
from scipy.spatial import KDTree
from typing import List, Tuple, Optional


class SpatialIndex:
    """
    Spatial index using KD-tree for efficient spatial queries.
    
    The KD-tree algorithm organizes points in k-dimensional space (2D for geographic coordinates)
    for efficient nearest neighbor and range searches.
    
    Time Complexity:
    - Construction: O(n log n)
    - Query: O(log n) average case
    """
    
    def __init__(self, buildings_gdf: gpd.GeoDataFrame):
        """
        Initialize spatial index with building centroids.
        
        Parameters
        ----------
        buildings_gdf : gpd.GeoDataFrame
            GeoDataFrame containing building geometries
        """
        self.buildings_gdf = buildings_gdf.copy()
        
        # Extract centroids for KD-tree
        self.buildings_gdf['centroid'] = self.buildings_gdf.geometry.centroid
        self.buildings_gdf['x'] = self.buildings_gdf.centroid.x
        self.buildings_gdf['y'] = self.buildings_gdf.centroid.y
        
        # Build KD-tree from centroids
        self.coordinates = np.column_stack([
            self.buildings_gdf['x'].values,
            self.buildings_gdf['y'].values
        ])
        self.kdtree = KDTree(self.coordinates)
        
    def find_nearest_neighbors(
        self,
        point: Point,
        k: int = 5
    ) -> gpd.GeoDataFrame:
        """
        Find k nearest buildings to a given point using KD-tree.
        
        Algorithm: KD-tree nearest neighbor search
        Time Complexity: O(log n) average case
        
        Parameters
        ----------
        point : Point
            Query point
        k : int
            Number of nearest neighbors to find
        
        Returns
        -------
        gpd.GeoDataFrame
            k nearest buildings sorted by distance
        """
        query_point = np.array([point.x, point.y])
        
        # KD-tree query: finds k nearest neighbors
        distances, indices = self.kdtree.query(query_point, k=k)
        
        # Return corresponding buildings
        nearest_buildings = self.buildings_gdf.iloc[indices].copy()
        nearest_buildings['distance'] = distances
        
        return nearest_buildings
    
    def find_within_radius(
        self,
        point: Point,
        radius: float
    ) -> gpd.GeoDataFrame:
        """
        Find all buildings within a given radius using KD-tree range query.
        
        Algorithm: KD-tree range search
        Time Complexity: O(log n + m) where m is number of results
        
        Parameters
        ----------
        point : Point
            Query point (building centroid)
        radius : float
            Search radius in coordinate units (meters for projected CRS)
        
        Returns
        -------
        gpd.GeoDataFrame
            Buildings within radius
        """
        query_point = np.array([point.x, point.y])
        
        # KD-tree range query: finds all points within radius
        indices = self.kdtree.query_ball_point(query_point, radius)
        
        if len(indices) == 0:
            return gpd.GeoDataFrame()
        
        # Return buildings within radius
        nearby_buildings = self.buildings_gdf.iloc[indices].copy()
        
        # Calculate actual distances
        nearby_buildings['distance'] = nearby_buildings.apply(
            lambda row: point.distance(row.centroid),
            axis=1
        )
        
        return nearby_buildings.sort_values('distance')


def binary_search_building_by_score(
    buildings_gdf: gpd.GeoDataFrame,
    target_score: float,
    score_column: str = 'suitability_score'
) -> Optional[int]:
    """
    Binary search to find building index with score closest to target.
    
    Requires: buildings_gdf must be sorted by score_column in ascending order
    
    Algorithm: Binary search
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Parameters
    ----------
    buildings_gdf : gpd.GeoDataFrame
        GeoDataFrame sorted by score column
    target_score : float
        Target score to search for
    score_column : str
        Column name containing scores
    
    Returns
    -------
    int or None
        Index of building with closest score, or None if empty
    """
    if len(buildings_gdf) == 0:
        return None
    
    scores = buildings_gdf[score_column].values
    left, right = 0, len(scores) - 1
    closest_idx = 0
    min_diff = float('inf')
    
    while left <= right:
        mid = (left + right) // 2
        current_score = scores[mid]
        diff = abs(current_score - target_score)
        
        # Track closest match
        if diff < min_diff:
            min_diff = diff
            closest_idx = mid
        
        if current_score < target_score:
            left = mid + 1
        elif current_score > target_score:
            right = mid - 1
        else:
            return mid  # Exact match found
    
    return closest_idx


def quicksort_buildings(
    buildings_gdf: gpd.GeoDataFrame,
    sort_column: str = 'suitability_score',
    ascending: bool = False
) -> gpd.GeoDataFrame:
    """
    Sort buildings using quicksort algorithm (for demonstration purposes).
    
    Algorithm: Quicksort
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) due to recursion
    
    Note: In production, use pandas built-in sort which is optimized.
    This implementation is for educational/demonstration purposes.
    
    Parameters
    ----------
    buildings_gdf : gpd.GeoDataFrame
        Buildings to sort
    sort_column : str
        Column to sort by
    ascending : bool
        Sort order
    
    Returns
    -------
    gpd.GeoDataFrame
        Sorted buildings
    """
    def quicksort_indices(arr, indices):
        """Recursive quicksort implementation."""
        if len(arr) <= 1:
            return indices
        
        pivot = arr[len(arr) // 2]
        left_indices = [indices[i] for i, x in enumerate(arr) if x < pivot]
        middle_indices = [indices[i] for i, x in enumerate(arr) if x == pivot]
        right_indices = [indices[i] for i, x in enumerate(arr) if x > pivot]
        
        left_arr = [x for x in arr if x < pivot]
        right_arr = [x for x in arr if x > pivot]
        
        return (quicksort_indices(left_arr, left_indices) + 
                middle_indices + 
                quicksort_indices(right_arr, right_indices))
    
    values = buildings_gdf[sort_column].values
    original_indices = list(buildings_gdf.index)
    
    sorted_indices = quicksort_indices(list(values), original_indices)
    
    if not ascending:
        sorted_indices = sorted_indices[::-1]
    
    return buildings_gdf.loc[sorted_indices]


def linear_search_building_by_id(
    buildings_gdf: gpd.GeoDataFrame,
    building_id: str,
    id_column: str = 'building_id'
) -> Optional[gpd.GeoDataFrame]:
    """
    Linear search to find building by ID.
    
    Algorithm: Linear search
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Parameters
    ----------
    buildings_gdf : gpd.GeoDataFrame
        Buildings to search
    building_id : str
        Building ID to find
    id_column : str
        Column name for building IDs
    
    Returns
    -------
    gpd.GeoDataFrame or None
        Building with matching ID, or None if not found
    """
    for idx, row in buildings_gdf.iterrows():
        if str(row[id_column]) == str(building_id):
            return buildings_gdf.loc[[idx]]
    
    return None


def find_top_k_buildings(
    buildings_gdf: gpd.GeoDataFrame,
    k: int,
    score_column: str = 'suitability_score'
) -> gpd.GeoDataFrame:
    """
    Find top k buildings using heap-based selection (via pandas).
    
    Algorithm: Heap-based partial sort (nth-element)
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    
    More efficient than full sort when k << n.
    
    Parameters
    ----------
    buildings_gdf : gpd.GeoDataFrame
        Buildings to search
    k : int
        Number of top buildings to return
    score_column : str
        Column to rank by
    
    Returns
    -------
    gpd.GeoDataFrame
        Top k buildings by score
    """
    return buildings_gdf.nlargest(k, score_column)
