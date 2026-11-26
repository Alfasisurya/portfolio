---
title: "Agronomic Intelligence"
period: "2026"
status: "Live web tool"
domains:
  - "Geospatial analytics"
  - "Agricultural data science"
summary: "Click anywhere in Indonesia to see the soil, the rainfall year, and a six-month climate outlook for that spot."
role: "Designer and developer"
organization: "Independent project"
featured: true
demo: "https://alfasisurya.github.io/agronomic-intelligence/"
repo: "https://github.com/Alfasisurya/agronomic-intelligence"
stack:
  - "HWSD v2"
  - "ERA5 via Open-Meteo"
  - "ECMWF SEAS5 via Open-Meteo"
  - "Leaflet"
---

**[Open the tool](https://alfasisurya.github.io/agronomic-intelligence/)** · [Source code on GitHub](https://github.com/Alfasisurya/agronomic-intelligence)

Agronomic Intelligence is a map-based tool for a quick first look at a location in Indonesia. Click a point, or paste coordinates, and it returns the soil profile from the Harmonized World Soil Database (version 2), the 1991–2020 monthly rainfall normal from the ERA5 reanalysis, and a six-month outlook from the ECMWF SEAS5 ensemble, both through Open-Meteo. It also calculates vapour-pressure deficit and compares each coming month with the local normal.

The tool flags a location as fertile or infertile with a simple constraint screen. A location is marked infertile when a major soil component (at least 25 percent of the mapping unit) or the topsoil has a serious limitation: a problem soil type in the World Reference Base, very shallow rooting, very high organic carbon, coarse fragments of 60 percent or more, very poor drainage, organic carbon below 1 percent in a mineral soil, CEC below 5 cmolc kg⁻¹, pH below 4.0 or above 8.5, aluminium saturation of 60 percent or more, ESP of 25 percent or more, or EC of 8 dS m⁻¹ or more. This is a screening rule, not an FAO land-evaluation class or a yield model.

Everything runs in the browser, with no server. The basemap is the Sentinel-2 cloudless 2016 mosaic by EOX, and the boundaries come from Natural Earth.

<figure>
  <img src="/images/analysis/agronomic-intelligence.jpg" alt="Agronomic Intelligence on a satellite basemap of Indonesia with city labels, and the soil panel open for Batu, East Java." />
  <figcaption>The interface on the satellite basemap, with the HWSD v2 soil reading for the default point at Jurang Kuali, Batu, East Java (SMU 4573).</figcaption>
</figure>

## Limits

The soil grid is coarse compared with a farm block, and one mapping unit can contain several soils. The rainfall normal and the seasonal outlook depend on a live forecast service. The screen is meant for an early desk assessment and should not be the only basis for sourcing or compliance decisions.
