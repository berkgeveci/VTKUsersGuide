"""Cut an unstructured grid with multiple planes and display the cross-sections."""
import os
import sys

from vtkmodules.vtkCommonDataModel import vtkPlane, vtkQuadric
from vtkmodules.vtkFiltersCore import vtkCutter, vtkAppendPolyData
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a volume dataset by sampling a quadric function.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(40, 40, 40)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()
sample.Update()

center = sample.GetOutput().GetCenter()

# Cut with three orthogonal planes passing through the center.
append = vtkAppendPolyData()

for normal in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
    plane = vtkPlane()
    plane.SetOrigin(center)
    plane.SetNormal(normal)

    cutter = vtkCutter()
    cutter.SetInputConnection(sample.GetOutputPort())
    cutter.SetCutFunction(plane)
    append.AddInputConnection(cutter.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(append.GetOutputPort())
mapper.SetScalarRange(sample.GetOutput().GetScalarRange())

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
