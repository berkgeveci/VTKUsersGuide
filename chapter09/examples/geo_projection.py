#!/usr/bin/env python3
"""Visualize several cartographic projections side by side.

Creates a graticule (grid of lat/long lines) and projects it through
multiple cartographic projections, displaying each in its own viewport
with a label. Demonstrates vtkGeoProjection, vtkGeoTransform, and
vtkTransformPolyDataFilter.

Requires VTK built with GeovisCore support (libproj).
"""

import math

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkGeovisCore import vtkGeoProjection, vtkGeoTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTextActor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401


def create_graticule(lat_step=15, lon_step=15, samples_per_line=80):
    """Create a polydata graticule (grid of lat/long lines) in radians."""
    points = vtkPoints()
    lines = vtkCellArray()

    for lat in range(-90, 91, lat_step):
        lat_rad = math.radians(max(-89.9, min(89.9, lat)))
        ids = []
        for i in range(samples_per_line + 1):
            lon_rad = math.radians(-180 + i * 360.0 / samples_per_line)
            ids.append(points.InsertNextPoint(lon_rad, lat_rad, 0.0))
        lines.InsertNextCell(len(ids), ids)

    for lon in range(-180, 181, lon_step):
        lon_rad = math.radians(lon)
        ids = []
        for i in range(samples_per_line + 1):
            lat_rad = math.radians(-89.9 + i * 179.8 / samples_per_line)
            ids.append(points.InsertNextPoint(lon_rad, lat_rad, 0.0))
        lines.InsertNextCell(len(ids), ids)

    poly = vtkPolyData()
    poly.SetPoints(points)
    poly.SetLines(lines)
    return poly


def create_projected_actor(graticule, proj_string):
    """Project a graticule and return an actor for the result."""
    source_proj = vtkGeoProjection()
    source_proj.SetPROJ4String("+proj=latlong")

    dest_proj = vtkGeoProjection()
    dest_proj.SetPROJ4String(proj_string)

    transform = vtkGeoTransform()
    transform.SetSourceProjection(source_proj)
    transform.SetDestinationProjection(dest_proj)

    transform_filter = vtkTransformPolyDataFilter()
    transform_filter.SetInputData(graticule)
    transform_filter.SetTransform(transform)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.2, 0.4, 0.8)
    actor.GetProperty().SetLineWidth(1.5)
    return actor


# Projections to display: (label, PROJ4 string)
projections = [
    ("Robinson", "+proj=robin +R=1"),
    ("Mollweide", "+proj=moll +R=1"),
    ("Hammer", "+proj=hammer +R=1"),
    ("Sinusoidal", "+proj=sinu +R=1"),
    ("Eckert IV", "+proj=eck4 +R=1"),
    ("Winkel Tripel", "+proj=wintri +R=1"),
    ("Aitoff", "+proj=aitoff +R=1"),
    ("Natural Earth", "+proj=natearth +R=1"),
    ("Goode Homolosine", "+proj=goode +R=1"),
]

graticule = create_graticule()

# Layout: 3 columns x 3 rows
cols, rows = 3, 3
render_window = vtkRenderWindow()
render_window.SetSize(1200, 900)
render_window.SetWindowName("Cartographic Projections - vtkGeoProjection")

for idx, (label, proj_string) in enumerate(projections):
    col = idx % cols
    row = rows - 1 - idx // cols  # top to bottom

    x0 = col / cols
    x1 = (col + 1) / cols
    y0 = row / rows
    y1 = (row + 1) / rows

    renderer = vtkRenderer()
    renderer.SetViewport(x0, y0, x1, y1)
    renderer.SetBackground(1.0, 1.0, 1.0)

    actor = create_projected_actor(graticule, proj_string)
    renderer.AddActor(actor)

    # Add projection name as a label
    text_actor = vtkTextActor()
    text_actor.SetInput(label)
    text_actor.GetTextProperty().SetFontSize(16)
    text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
    text_actor.GetTextProperty().BoldOn()
    text_actor.SetPosition(10, 10)
    renderer.AddViewProp(text_actor)

    renderer.ResetCamera()
    render_window.AddRenderer(renderer)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
