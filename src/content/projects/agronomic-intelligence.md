---
title: "Agronomic Intelligence"
period: "2026"
status: "Working prototype"
domains:
  - "Geospatial analytics"
  - "Agricultural data science"
summary: "A standalone map for Indonesia. A click returns a public soil reading, a rainfall year, and a six-month climate outlook."
role: "Author of the tool and of the November 2026 note that describes it"
organization: "Independent working note. Not an employer project."
featured: true
stack:
  - "HWSD v2"
  - "WorldClim v2.1"
  - "Open-Meteo seasonal API"
  - "Sentinel-2, when the user supplies a GeoTIFF"
---

The November 2026 note describes a screen for one clicked location in Indonesia. The soil reading comes from Harmonized World Soil Database version 2. Historical rain comes from WorldClim v2.1. The outlook is the ECMWF SEAS5 ensemble mean through the Open-Meteo seasonal API, not a copy of the climatology. Vapour-pressure deficit is calculated from temperature and humidity. Each of the next six months is compared with the local normal.

The fertile or infertile flag is a constraint screen written for the tool. It is not an FAO land-evaluation class and it is not a yield model. A location is marked infertile when a listed constraint is true for a major soil component, defined as a share of at least 25 percent, or for the topsoil. The constraints named in the note are problem soils in the World Reference Base, very shallow rooting, very high organic carbon, coarse fragments of at least 60 percent, very poor drainage, organic carbon below 1 percent where the soil is not peat, CEC below 5 cmolc kg⁻¹, pH below 4.0 or above 8.5, aluminium saturation of at least 60 percent, ESP of at least 25 percent, and EC of at least 8 dS m⁻¹.

A user-supplied Sentinel-2 surface-reflectance image can be sampled with published leaf and soil nutrient regressions. The note does not reproduce those equations. The satellite number is a screen. It does not replace a laboratory analysis.

The soil and climate databases are not redistributed with this website. The figure is the interface.

<figure>
  <img src="/images/analysis/agronomic-intelligence.jpg" alt="Agronomic Intelligence interface centred on East Java, with a soil-unit reading for Jawa Timur." />
  <figcaption>Interface from the November 2026 note. The panel is an HWSD v2 reading for one mapping unit in East Java. Basemap: OpenFreeMap.</figcaption>
</figure>

## Limits

The soil grid is coarse relative to a farm block, and one mapping unit can mix several soils. Seasonal notes depend on a live forecast API. Cloud, scale, and sensor differences move a satellite nutrient estimate. The note says the screen should not be used alone for a sourcing or compliance decision.
