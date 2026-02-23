"""Clip a volume mesh (unstructured grid) with a plane using vtkTableBasedClipDataSet."""
import os
import sys

from vtkmodules.vtkCommonDataModel import vtkPlane, vtkQuadric
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
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

# Create a volume (vtkImageData) by sampling a quadric function.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()
sample.Update()

# Clip the volume with a plane.  vtkTableBasedClipDataSet works on any
# vtkDataSet (including vtkImageData, vtkUnstructuredGrid, etc.).
plane = vtkPlane()
plane.SetOrigin(sample.GetOutput().GetCenter())
plane.SetNormal(1, 0, 0)

clipper = vtkTableBasedClipDataSet()
clipper.SetInputConnection(sample.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.SetValue(0.0)

# Convert unstructured grid output to polydata for rendering.
surface = vtkGeometryFilter()
surface.SetInputConnection(clipper.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
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
