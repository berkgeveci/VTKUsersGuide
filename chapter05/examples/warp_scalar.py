"""Warp a plane by its scalar elevation values to create a 3D surface."""
import sys

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a plane and add scalar elevation along the Y direction.
plane = vtkPlaneSource()
plane.SetResolution(40, 40)

elevation = vtkElevationFilter()
elevation.SetInputConnection(plane.GetOutputPort())
elevation.SetLowPoint(0, 0, 0)
elevation.SetHighPoint(0, 1, 0)
elevation.SetScalarRange(0, 1)

# Warp the plane in Z by the scalar value.
warp = vtkWarpScalar()
warp.SetInputConnection(elevation.GetOutputPort())
warp.SetScaleFactor(0.3)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(0, 1)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
if "--non-interactive" not in sys.argv:
    interactor.Start()
