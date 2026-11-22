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

This page explains the method inside the [Agronomic Intelligence platform](../../projects/agronomic-intelligence/index.html): how a single click on the map becomes a soil and climate screen. It is a working method, not a peer-reviewed paper.

## Data

- Soil class and layer properties: Harmonized World Soil Database version 2 (FAO/IIASA).
- Historical rainfall: WorldClim v2.1 monthly precipitation.
- Six-month outlook: ECMWF SEAS5 ensemble mean, through the Open-Meteo seasonal API.
- Administrative boundaries: GADM v4.1.
- Optional: a Sentinel-2 surface-reflectance image supplied by the user.

## Method

The workflow is a lookup followed by a set of rules.

```text
cell = soil raster at the clicked coordinate
components = HWSD v2 attributes for that mapping unit
rain = WorldClim monthly precipitation at the cell
outlook = Open-Meteo SEAS5 ensemble mean, next six months
vpd = calculated from temperature and relative humidity
label each month against the local normal
flag infertile if a listed constraint applies to a major component or the topsoil
```

Separate ratings for pH, organic carbon, total nitrogen, CEC, base saturation, and aluminium saturation stay visible, so a single fertile flag does not hide a moderate limitation. Months with less than 60 mm of rain and years with more than 3,000 mm trigger a climate note. When a Sentinel-2 image is loaded, nutrient estimates use the regressions of Kaliana (2018), with leaf classes from Ochs and Olivin and soil classes from Goh (2011).

## Result

The figure shows the tool centred on a point in East Java. For that mapping unit, the panel lists three soil components, Luvisols and Andosols, along with drainage, rooting depth, and available water.

<figure>
  <img src="/images/analysis/agronomic-intelligence.jpg" alt="Map of Indonesia with the Agronomic Intelligence soil panel open on Jawa Timur." />
  <figcaption>Agronomic Intelligence, November 2026, showing a single clicked cell.</figcaption>
</figure>

## Interpretation

The screen answers a desk question: given a coordinate, what constraints do global soil and climate data suggest, and what extra detail would a satellite image add within a field? It does not certify land suitability or estimate yield.

## Limits

A mapping unit can contain several soils. The fertile flag is a screening rule, not an official FAO class. The seasonal notes depend on a live forecast service, and reflectance regressions are sensitive to cloud, scale, and sensor. The screen should not be the only basis for a sourcing or compliance decision.

## References

FAO/IIASA (2023). Harmonized World Soil Database version 2.0.

Fick, S.E. and Hijmans, R.J. (2017). WorldClim 2. International Journal of Climatology, 37, 4302–4315.

ECMWF SEAS5, accessed through the Open-Meteo Seasonal Forecast API.

GADM (2024). Database of Global Administrative Areas, version 4.1.

Kaliana, I. (2018). Development of a Decision Support System for Oil Palm Fertilizer Requirement Based on Precision Agriculture. MSc thesis, IPB University.
