# Solar Panel Suitability API Documentation

Version: 0.1.0

## Overview

The Solar Panel Suitability API provides programmatic access to solar panel installation suitability analysis results for buildings. Query individual buildings, get priority lists, and access neighborhood-level aggregations for visualization.

**Base URL:** `http://localhost:5000`

---

## Endpoints

### 1. API Information

#### `GET /`

Returns API information and available endpoints.

**Response:**
```json
{
  "name": "Solar Panel Suitability API",
  "version": "0.1.0",
  "endpoints": {
    "/buildings": "Get all buildings with suitability scores",
    "/buildings/<id>": "Get specific building details",
    "/buildings/<id>/suitability": "Get suitability analysis for a building",
    "/map/neighborhood": "Get aggregated data by neighborhood",
    "/priority": "Get priority list of top buildings"
  }
}
```

---

### 2. List All Buildings

#### `GET /buildings`

Get a list of all buildings with basic information.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `min_score` | float | No | Minimum suitability score (0-100) |
| `limit` | integer | No | Maximum number of results (default: 100) |

**Example Request:**
```bash
curl "http://localhost:5000/buildings?min_score=80&limit=50"
```

**Example Response:**
```json
{
  "count": 45,
  "buildings": [
    {
      "building_id": "12345",
      "suitability_score": 92.5,
      "roof_area_m2": 250,
      "category": "Excellent"
    }
  ]
}
```

---

### 3. Get Building Details

#### `GET /buildings/<building_id>`

Get detailed information for a specific building.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `building_id` | string | Yes | Unique building identifier |

**Example Request:**
```bash
curl "http://localhost:5000/buildings/12345"
```

**Example Response:**
```json
{
  "building_id": "12345",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[5.0, 52.0], [5.1, 52.0], [5.1, 52.1], [5.0, 52.1], [5.0, 52.0]]]
  },
  "roof_area_m2": 250,
  "orientation_degrees": 185,
  "height_m": 8.5
}
```

---

### 4. Get Building Suitability Analysis

#### `GET /buildings/<building_id>/suitability`

Get comprehensive solar panel suitability analysis for a specific building.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `building_id` | string | Yes | Unique building identifier |

**Example Request:**
```bash
curl "http://localhost:5000/buildings/12345/suitability"
```

**Example Response:**
```json
{
  "building_id": "12345",
  "suitability_score": 85.5,
  "energy_potential_kwh": 12000,
  "roof_area_m2": 150,
  "orientation_degrees": 180,
  "shading_factor": 0.15,
  "roi_percentage": 8.5,
  "payback_years": 7.2,
  "category": "Excellent",
  "installation_cost_eur": 30000,
  "annual_revenue_eur": 3000
}
```

---

### 5. Get Priority List

#### `GET /priority`

Get a priority-ranked list of buildings for solar panel installation.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `top_n` | integer | No | Number of top buildings to return (default: 100) |

**Example Request:**
```bash
curl "http://localhost:5000/priority?top_n=10"
```

**Example Response:**
```json
{
  "count": 10,
  "buildings": [
    {
      "rank": 1,
      "building_id": "98765",
      "suitability_score": 95.2,
      "energy_potential_kwh": 25000,
      "category": "Excellent"
    }
  ]
}
```

---

### 6. Get Neighborhood Aggregation

#### `GET /map/neighborhood`

Get aggregated solar suitability data by neighborhood for choropleth visualization.

**Example Request:**
```bash
curl "http://localhost:5000/map/neighborhood"
```

**Example Response:**
```json
{
  "neighborhoods": [
    {
      "neighborhood_id": "centrum",
      "name": "Centrum",
      "avg_suitability_score": 72.5,
      "total_buildings": 450,
      "total_energy_potential_kwh": 5400000,
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    }
  ]
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource does not exist |
| 500 | Internal Server Error |

---

## Error Response Format

```json
{
  "error": "Error message description",
  "status_code": 404
}
```

---

## Running the API

### Development Server

```bash
# From project root
python src/api.py
```

The API will be available at `http://localhost:5000`

### Production Deployment

```bash
# Using gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider implementing rate limiting using Flask-Limiter.

---

## Authentication

Currently no authentication is required. For production use, consider implementing API keys or OAuth.

---

## Examples

### Python (requests)

```python
import requests

# Get building suitability
response = requests.get('http://localhost:5000/buildings/12345/suitability')
data = response.json()
print(f"Suitability Score: {data['suitability_score']}")
```

### JavaScript (fetch)

```javascript
fetch('http://localhost:5000/buildings/12345/suitability')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL

```bash
# Get priority list
curl -X GET "http://localhost:5000/priority?top_n=20" \
     -H "Content-Type: application/json"
```

---

## Support

For issues or questions, please open an issue on the GitHub repository.
