"""Use vtkArrayCalculator to compute a derived scalar on elevation data."""
import sys

from vtkmodules.vtkFiltersCore import vtkArrayCalculator, vtkElevationFilter
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

# Create a high-resolution plane and compute elevation along Y.
plane = vtkPlaneSource()
plane.SetResolution(40, 40)

elevation = vtkElevationFilter()
elevation.SetInputConnection(plane.GetOutputPort())
elevation.SetLowPoint(0, 0, 0)
elevation.SetHighPoint(0, 1, 0)
elevation.SetScalarRange(0, 1)

# Use the calculator to derive a new scalar: sin(Elevation * pi).
calc = vtkArrayCalculator()
calc.SetInputConnection(elevation.GetOutputPort())
calc.AddScalarArrayName("Elevation")
calc.SetFunction("sin(Elevation * 3.14159265)")
calc.SetResultArrayName("SineElevation")

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(calc.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("SineElevation")
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
