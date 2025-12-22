"""
Unit tests for solar energy calculations.
"""

import pytest
from src.solar import (
    calculate_solar_potential,
    calculate_roi,
    calculate_payback_period
)


def test_calculate_solar_potential_basic():
    """Test basic solar potential calculation."""
    area = 100  # m²
    irradiance = 1000  # kWh/m²/year
    efficiency = 0.18  # 18%
    shading = 0.0  # No shading
    
    energy = calculate_solar_potential(area, irradiance, efficiency, shading)
    
    # E = 100 * 1000 * 0.18 * (1 - 0) = 18,000 kWh
    assert energy == pytest.approx(18000.0, rel=1e-2)


def test_calculate_solar_potential_with_shading():
    """Test solar potential with shading factor."""
    area = 100
    irradiance = 1000
    efficiency = 0.18
    shading = 0.3  # 30% shading
    
    energy = calculate_solar_potential(area, irradiance, efficiency, shading)
    
    # E = 100 * 1000 * 0.18 * (1 - 0.3) = 12,600 kWh
    assert energy == pytest.approx(12600.0, rel=1e-2)


def test_calculate_solar_potential_zero_area():
    """Test with zero roof area."""
    energy = calculate_solar_potential(0, 1000, 0.18, 0)
    assert energy == 0.0


def test_calculate_solar_potential_invalid_shading():
    """Test with invalid shading factor."""
    with pytest.raises(ValueError):
        calculate_solar_potential(100, 1000, 0.18, 1.5)  # Shading > 1


def test_calculate_roi():
    """Test ROI calculation."""
    energy_kwh = 18000
    energy_price = 0.25  # €0.25 per kWh
    cost_per_m2 = 200
    area = 100
    
    roi = calculate_roi(energy_kwh, energy_price, cost_per_m2, area)
    
    # Annual revenue = 18000 * 0.25 = 4500
    # Cost = 100 * 200 = 20000
    # ROI = (4500 - 20000) / 20000 = -77.5%
    assert roi == pytest.approx(-77.5, rel=1e-2)


def test_calculate_payback_period():
    """Test payback period calculation."""
    energy_kwh = 18000
    energy_price = 0.25
    cost_per_m2 = 200
    area = 100
    
    payback = calculate_payback_period(energy_kwh, energy_price, cost_per_m2, area)
    
    # Cost = 20000, Annual revenue = 4500
    # Payback = 20000 / 4500 ≈ 4.44 years
    assert payback == pytest.approx(4.44, rel=1e-2)


def test_calculate_payback_period_zero_energy():
    """Test payback period with zero energy production."""
    payback = calculate_payback_period(0, 0.25, 200, 100)
    assert payback == float('inf')
