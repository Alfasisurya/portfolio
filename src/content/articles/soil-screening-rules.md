---
title: "Constraint rules in the soil and climate screen"
date: "November 2026"
year: 2026
topics:
  - "Geospatial processing"
  - "Agricultural data science"
summary: "The screening rules written for the Agronomic Intelligence tool, kept separate from the peer-reviewed archive."
---

These rules are the ones written down in the November 2026 note. They label a clicked location. They are not an FAO land-suitability class.

A location is marked fertile when none of the primary constraints fire. It is marked infertile when any of the following is true for a major component, meaning a share of at least 25 percent, or for the topsoil:

- A problem soil in the World Reference Base code: Histosol, Leptosol, Solonchak, Solonetz, Regosol, Arenosol, or Podzol.
- Very shallow rooting, organic carbon of at least 18 percent, or coarse fragments of at least 60 percent.
- Very poor drainage, organic carbon below 1 percent where the soil is not peat, or CEC below 5 cmolc kg⁻¹.
- pH below 4.0 or above 8.5, aluminium saturation of at least 60 percent, ESP of at least 25 percent, or EC of at least 8 dS m⁻¹.

Ratings for pH, organic carbon, total nitrogen, CEC, base saturation, and aluminium saturation stay visible beside the flag. A dry month is under 60 mm in the WorldClim year. A very wet year is over 3,000 mm.

The note is explicit that the flag can be wrong for a farm block, because the grid is coarse and a mapping unit can mix soils.
