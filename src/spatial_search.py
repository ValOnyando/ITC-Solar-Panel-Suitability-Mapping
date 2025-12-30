"""
Spatial Search Module
Implements spatial search algorithms including KD-tree for efficient nearest neighbor queries.
"""
from src.data_acquisition import fetch_pdok_buildings
import numpy as np
import pandas as pd 
import geopandas as gpd
from shapely import Point
from shapely.geometry import Point, Polygon
from scipy.spatial import KDTree
from scipy.spatial import cKDTree
from typing import List, Tuple, Optional

#temp 
import networkx as nx 
import matplotlib as plt 

#=============================================
# Testing and dubbaging 
#=============================================

Buildings = r'D:/Master/Q2/sci Programming for Geospatial//Project 1/Git clone/ITC-Solar-Panel-Suitability-Mapping/Data/Raw/Buildings_Amsterdam.geojson'

buildings_gdf  =   fetch_pdok_buildings(Buildings)



buildings_gdf2 = buildings_gdf.copy()

buildings_gdf2['centroid'] = buildings_gdf.geometry.centroid
buildings_projected  = buildings_gdf2.to_crs(28992)
buildings_projected.crs
   # Extract centroids for KD-tree


buildings_projected['centroid'] = buildings_gdf2.geometry.centroid
buildings_projected['x'] = buildings_gdf2.centroid.x
buildings_projected['y'] = buildings_gdf2.centroid.y
buildings_projected.crs        
search = SpatialIndex(buildings_projected)

y = 52.37918055583675
x = 4.892828083995229
point = Point(y,x)
buildings_projected.columns
search.find_within_radius(point , 10000000)





search.find_nearest_neighbors(point , k = 10)
search.find_within_radius(point, radius = 100)

G = nx.graph
#============================r==========================================================

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
        x = self.buildings_gdf['x'].to_numpy(dtype=float)
        y = self.buildings_gdf['y'].to_numpy(dtype=float)
        self.coordinates = np.column_stack((x, y))
        
        self.kdtree = KDTree(self.coordinates)
        
        

        
    def find_nearest_neighbors(
        self,
        point: Point,
        k: int = 5
    ) -> gpd.GeoDataFrame:
        """
        Find kd nearest buildings to a given point using KD-tree.
        
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
        result = self.buildings_gdf.iloc[indices].copy()
        if result.empty:
           print("No buildings found within radius.")
        return result


        
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



#============================

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import KDTree


class SpatialSearch:
    """
    Spatial nearest-neighbour search for building-based analysis.
    """

    def __init__(self, buildings):
        """
        Initialise the spatial search using building reference locations.

        Parameters
        ----------
        buildings :
            GeoDataFrame, GeoSeries, DataFrame with x/y,
            iterable of shapely Points, or NumPy array (n, 2).
        """

        # Normalise building reference points once
        self.buildings = self._normalise_points(buildings)

        # Build spatial index once
        self.kdtree = KDTree(self.buildings)

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------
    def _normalise_points(self, points):
        """
        Convert supported point formats into a NumPy array of shape (n, 2).
        """

        # GeoDataFrame → use centroids
        if isinstance(points, gpd.GeoDataFrame):
            return np.column_stack(
                (points.geometry.centroid.x, points.geometry.centroid.y)
            )

        # GeoSeries (Point geometry)
        if isinstance(points, gpd.GeoSeries):
            return np.column_stack((points.x, points.y))

        # pandas DataFrame with x/y columns
        if isinstance(points, pd.DataFrame):
            if {"x", "y"}.issubset(points.columns):
                return points[["x", "y"]].to_numpy()

        # Single shapely Point
        if isinstance(points, Point):
            return np.array([[points.x, points.y]])

        # Tuple / list → single point
        if isinstance(points, (tuple, list)) and len(points) == 2:
            if all(np.isscalar(v) for v in points):
                return np.array([[points[0], points[1]]])

        # NumPy array
        if isinstance(points, np.ndarray):
            if points.ndim == 1 and points.shape[0] == 2:
                return points.reshape(1, 2)
            if points.ndim == 2 and points.shape[1] == 2:
                return points

        raise TypeError(
            "Points must be a GeoDataFrame, GeoSeries, DataFrame with x/y, "
            "shapely Point, (x, y) tuple, or NumPy array of shape (n, 2)."
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def find_nearest_neighbors(self, points, k=1):
        """
        Find k nearest building neighbours for given query points.

        Parameters
        ----------
        points :
            Query locations in any supported point format.
        k : int
            Number of nearest neighbours.

        Returns
        -------
        distances : np.ndarray
            Distances to nearest buildings (shape: n x k).
        indices : np.ndarray
            Indices of nearest buildings (shape: n x k).
        """

        if k < 1:
            raise ValueError("k must be >= 1")

        # Normalise query points
        query_points = self._normalise_points(points)

        # KDTree query
        distances, indices = self.kdtree.query(query_points, k=k)

        # Ensure consistent 2D output
        distances = np.atleast_2d(distances)
        indices = np.atleast_2d(indices)

        return distances, indices



search = SpatialSearch(buildings_projected)
neighbors = search.find_nearest_neighbors(buildings_projected['x' , 'y'].to_numpy)
len( neighbors)

