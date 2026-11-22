---
title: "How Agronomic Intelligence flags fertile and infertile land"
date: "2026-11-22"
topics:
  - "Agronomic Intelligence"
  - "Geospatial analysis"
summary: "The constraint rules behind the fertile or infertile flag in the Agronomic Intelligence platform."
---

The [Agronomic Intelligence platform](../../projects/agronomic-intelligence/index.html) labels a clicked location with a simple rule set. The label is a screening aid, not an FAO land-suitability class.

A location is fertile when none of the main constraints apply. It is infertile when any of the following is true for a major soil component (at least 25 percent of the mapping unit) or for the topsoil:

- A problem soil in the World Reference Base: Histosol, Leptosol, Solonchak, Solonetz, Regosol, Arenosol, or Podzol.
- Very shallow rooting, organic carbon of 18 percent or more, or coarse fragments of 60 percent or more.
- Very poor drainage, organic carbon below 1 percent in a mineral soil, or CEC below 5 cmolc kg⁻¹.
- pH below 4.0 or above 8.5, aluminium saturation of 60 percent or more, ESP of 25 percent or more, or EC of 8 dS m⁻¹ or more.

Ratings for pH, organic carbon, total nitrogen, CEC, base saturation, and aluminium saturation are shown beside the flag. A dry month has less than 60 mm of rain in the 1991–2020 ERA5 normal, and a very wet year has more than 3,000 mm.

Because the soil grid is coarse and a mapping unit can mix several soils, the flag can be wrong for an individual farm block.

You can [try the tool yourself](https://alfasisurya.github.io/agronomic-intelligence/) by clicking any location in Indonesia.
