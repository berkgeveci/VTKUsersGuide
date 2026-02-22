#!/usr/bin/env python3
"""List available cartographic projections and demonstrate vtkGeoProjection.

Enumerates all projections provided by the PROJ library through VTK's
vtkGeoProjection class, then shows details for a specific projection.

Requires VTK built with GeovisCore support (libproj).
"""

from vtkmodules.vtkGeovisCore import vtkGeoProjection

# List all available projections
num_projections = vtkGeoProjection.GetNumberOfProjections()
print(f"VTK supports {num_projections} cartographic projections:\n")

for i in range(num_projections):
    name = vtkGeoProjection.GetProjectionName(i)
    desc = vtkGeoProjection.GetProjectionDescription(i)
    print(f"  {name:12s}  {desc}")

# Demonstrate creating a specific projection
print("\n--- Projection details ---")
proj = vtkGeoProjection()
proj.SetName("robin")
print(f"Name: robin")
print(f"Description: {proj.GetDescription()}")
print(f"Index: {proj.GetIndex()}")
