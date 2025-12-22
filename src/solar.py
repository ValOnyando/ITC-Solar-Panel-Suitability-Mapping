"""
Solar Energy Module
Calculates solar energy potential for buildings.
"""

import numpy as np
from typing import Optional


def calculate_solar_potential(
    area: float,
    irradiance: float,
    efficiency: float = 0.18,
    shading_factor: float = 0.0
) -> float:
    """
    Calculate annual solar energy production potential.
    
    Mathematical formula:
    E = A × H × η × (1 - S)
    
    Parameters
    ----------
    area : float
        Roof area in m²
    irradiance : float
        Annual solar irradiance in kWh/m²/year
    efficiency : float
        Panel efficiency (default 18% = 0.18)
    shading_factor : float
        Shading factor between 0 (no shade) and 1 (full shade)
    
    Returns
    -------
    float
        Annual energy production in kWh
    """
    if area <= 0 or irradiance <= 0:
        return 0.0
    
    if not 0 <= shading_factor <= 1:
        raise ValueError("Shading factor must be between 0 and 1")
    
    energy = area * irradiance * efficiency * (1 - shading_factor)
    return energy


def calculate_roi(
    energy_kwh: float,
    energy_price: float = 0.25,
    installation_cost_per_m2: float = 200,
    area: float = 0
) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Mathematical formula:
    ROI = (E × Price - Cost) / Cost
    
    Parameters
    ----------
    energy_kwh : float
        Annual energy production in kWh
    energy_price : float
        Energy price per kWh (default €0.25)
    installation_cost_per_m2 : float
        Installation cost per m² (default €200)
    area : float
        Roof area in m²
    
    Returns
    -------
    float
        ROI as a percentage
    """
    if area <= 0:
        return 0.0
    
    cost = area * installation_cost_per_m2
    annual_revenue = energy_kwh * energy_price
    
    if cost == 0:
        return 0.0
    
    roi = (annual_revenue - cost) / cost
    return roi * 100  # Convert to percentage


def calculate_payback_period(
    energy_kwh: float,
    energy_price: float = 0.25,
    installation_cost_per_m2: float = 200,
    area: float = 0
) -> float:
    """
    Calculate payback period in years.
    
    Parameters
    ----------
    energy_kwh : float
        Annual energy production in kWh
    energy_price : float
        Energy price per kWh
    installation_cost_per_m2 : float
        Installation cost per m²
    area : float
        Roof area in m²
    
    Returns
    -------
    float
        Payback period in years
    """
    if area <= 0 or energy_kwh <= 0:
        return float('inf')
    
    cost = area * installation_cost_per_m2
    annual_revenue = energy_kwh * energy_price
    
    if annual_revenue == 0:
        return float('inf')
    
    return cost / annual_revenue
