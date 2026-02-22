#!/usr/bin/env python3
"""Transform a lat-long grid through a cartographic projection.

Creates a regular grid in latitude-longitude space, applies the
Mollweide projection using vtkGeoTransform, and visualizes the
projected grid.

Requires VTK built with GeovisCore support (libproj).
"""

import math

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkGeovisCore import vtkGeoProjection, vtkGeoTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401


def create_graticule(lat_step=10, lon_step=10, samples_per_line=100):
    """Create a polydata graticule (grid of lat/long lines) in radians."""
    points = vtkPoints()
    lines = vtkCellArray()

    # Lines of constant latitude (avoid exact poles for projection stability)
    for lat in range(-90, 91, lat_step):
        lat_clamped = max(-89.9, min(89.9, lat))
        lat_rad = math.radians(lat_clamped)
        line_ids = []
        for i in range(samples_per_line + 1):
            lon_rad = math.radians(-180 + i * 360.0 / samples_per_line)
            pid = points.InsertNextPoint(lon_rad, lat_rad, 0.0)
            line_ids.append(pid)
        lines.InsertNextCell(len(line_ids), line_ids)

    # Lines of constant longitude (avoid exact poles for projection stability)
    for lon in range(-180, 181, lon_step):
        lon_rad = math.radians(lon)
        line_ids = []
        for i in range(samples_per_line + 1):
            lat_deg = -89.9 + i * 179.8 / samples_per_line
            lat_rad = math.radians(lat_deg)
            pid = points.InsertNextPoint(lon_rad, lat_rad, 0.0)
            line_ids.append(pid)
        lines.InsertNextCell(len(line_ids), line_ids)

    poly = vtkPolyData()
    poly.SetPoints(points)
    poly.SetLines(lines)
    return poly


# Create graticule in lat-long (radian) coordinates
graticule = create_graticule(lat_step=15, lon_step=15)

# Set up source projection (lat-long in radians)
source_proj = vtkGeoProjection()
source_proj.SetPROJ4String("+proj=latlong")

# Set up destination projection (Mollweide)
dest_proj = vtkGeoProjection()
dest_proj.SetPROJ4String("+proj=moll +R=1")

# Create the transform
transform = vtkGeoTransform()
transform.SetSourceProjection(source_proj)
transform.SetDestinationProjection(dest_proj)

# Apply the transform to the graticule
transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputData(graticule)
transform_filter.SetTransform(transform)

# Create visualization pipeline
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(transform_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.4, 0.8)
actor.GetProperty().SetLineWidth(1.5)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.ResetCamera()

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 600)
render_window.SetWindowName("Mollweide Projection - vtkGeoTransform")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
