---
title: "Agronomic Intelligence platform: soil and climate screening"
date: "November 2026"
year: 2026
category: "Geospatial analysis"
topics:
  - "Geospatial analysis"
  - "Climate and environmental data"
  - "Agricultural modelling"
summary: "How the Agronomic Intelligence platform combines a global soil grid, a rainfall climatology, and a seasonal forecast to screen any location in Indonesia."
question: "From a single coordinate, what can global soil and climate data tell us, and where do they fall short?"
status: "exploratory"
featured: true
---

This page explains the method inside the [Agronomic Intelligence platform](../../projects/agronomic-intelligence/index.html): how a single click on the map becomes a soil and climate screen. It is a working method, not a peer-reviewed paper. You can [try the tool here](https://alfasisurya.github.io/agronomic-intelligence/).

## Data

- Soil class and layer properties: Harmonized World Soil Database version 2 (FAO/IIASA).
- Historical climate: monthly normals for 1991–2020 from the ERA5 reanalysis, through the Open-Meteo Historical Weather API.
- Six-month outlook: ECMWF SEAS5 ensemble mean, through the Open-Meteo seasonal API.
- Boundaries: Natural Earth.

## Method

The workflow is a lookup followed by a set of rules.

```text
cell = soil raster at the clicked coordinate
components = HWSD v2 attributes for that mapping unit
normals = ERA5 daily data for 1991-2020, averaged by month
outlook = Open-Meteo SEAS5 ensemble mean, next six months
vpd = calculated from temperature and relative humidity
label each month against the local normal
flag infertile if a listed constraint applies to a major component or the topsoil
```

Separate ratings for pH, organic carbon, total nitrogen, CEC, base saturation, and aluminium saturation stay visible, so a single fertile flag does not hide a moderate limitation. Long dry seasons (six or more months under 60 mm) and annual rainfall above 3,000 mm trigger a climate note.

## Result

The figure shows the tool centred on a point in East Java. For that mapping unit, the panel lists three soil components, Luvisols and Andosols, along with drainage, rooting depth, and available water.

<figure>
  <img src="/images/analysis/agronomic-intelligence.jpg" alt="Map of Indonesia with the Agronomic Intelligence soil panel open on Jawa Timur." />
  <figcaption>Agronomic Intelligence, November 2026, showing a single clicked cell.</figcaption>
</figure>

## Interpretation

The screen answers a desk question: given a coordinate, what constraints do global soil and climate data suggest? It does not certify land suitability or estimate yield.

## Limits

A mapping unit can contain several soils. The fertile flag is a screening rule, not an official FAO class. ERA5 is a coarse reanalysis and can miss local rainfall patterns, and the seasonal notes depend on a live forecast service. The screen should not be the only basis for a sourcing or compliance decision.

## References

FAO and IIASA (2023). Harmonized World Soil Database version 2.0. Rome and Laxenburg. https://doi.org/10.4060/cc3823en

Hersbach, H. et al. (2020). The ERA5 global reanalysis. Quarterly Journal of the Royal Meteorological Society, 146, 1999–2049.

ECMWF SEAS5, accessed through the Open-Meteo Seasonal Forecast API.

Natural Earth. Free vector and raster map data, naturalearthdata.com.
