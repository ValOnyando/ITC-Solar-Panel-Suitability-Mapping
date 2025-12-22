from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solar-panel-suitability",
    version="0.1.0",
    author="Val Onyando",
    description="A geospatial analysis toolkit for identifying optimal rooftops for solar panel installation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Val-Onyando/ITC-Solar-Panel-Suitability-Mapping",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "geopandas>=0.14.0",
        "rasterio>=1.3.0",
        "shapely>=2.0.0",
        "folium>=0.15.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "requests>=2.31.0",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "solar-api=src.api:main",
        ],
    },
)
