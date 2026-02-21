#!/usr/bin/env python3
#
# This example demonstrates the use of vtkScalarBarActor to create a
# color-coded key that relates color values to numerical data values.
#

import os

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401

# Create a sphere and apply an elevation filter to generate scalar
# data. The elevation filter colors the sphere from bottom to top.
sphere = vtkSphereSource()
sphere.SetThetaResolution(32)
sphere.SetPhiResolution(32)

elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())
elevation.SetLowPoint(0, -0.5, 0)
elevation.SetHighPoint(0, 0.5, 0)

# Create the mapper. The mapper will use the elevation scalars to
# color the sphere via a lookup table.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Create a scalar bar to display the color legend. Reference the
# mapper's lookup table so the colors and range match.
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(mapper.GetLookupTable())
scalar_bar.SetTitle("Elevation")
scalar_bar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.01)
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetWidth(0.8)
scalar_bar.SetHeight(0.17)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer
renderer.AddActor(actor)
renderer.AddViewProp(scalar_bar)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(600, 600)

renderer.ResetCamera()
render_window.Render()
interactor.Start()
