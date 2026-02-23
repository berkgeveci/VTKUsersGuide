"""Threshold a sampled implicit function to extract cells within a scalar range."""
import os
import sys

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
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

# Create a quadric implicit function and sample it on a 3D grid.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

# Threshold: keep only cells whose scalar value is between 0.5 and 1.0.
thresh = vtkThreshold()
thresh.SetInputConnection(sample.GetOutputPort())
thresh.SetThresholdFunction(thresh.THRESHOLD_BETWEEN)
thresh.SetLowerThreshold(0.5)
thresh.SetUpperThreshold(1.0)

# Convert the unstructured grid output to polydata for rendering.
surface = vtkGeometryFilter()
surface.SetInputConnection(thresh.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarRange(0.5, 1.0)

actor = vtkActor()
actor.SetMapper(mapper)

# Render
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
