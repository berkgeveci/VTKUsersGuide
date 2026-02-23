"""Threshold a dataset to extract cells within a scalar range."""
import sys

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkThreshold, vtkThresholdPoints
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a 3D scalar field by sampling a quadric.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

# --- Cell-based threshold: keep cells with scalars between 0.5 and 1.0 ---
thresh = vtkThreshold()
thresh.SetInputConnection(sample.GetOutputPort())
thresh.SetThresholdFunction(thresh.THRESHOLD_BETWEEN)
thresh.SetLowerThreshold(0.5)
thresh.SetUpperThreshold(1.0)

surface = vtkGeometryFilter()
surface.SetInputConnection(thresh.GetOutputPort())

mapper1 = vtkPolyDataMapper()
mapper1.SetInputConnection(surface.GetOutputPort())
mapper1.SetScalarRange(0.5, 1.0)

actor1 = vtkActor()
actor1.SetMapper(mapper1)

# --- Point-based threshold: keep only points with scalars > 0.8 ---
thresh_pts = vtkThresholdPoints()
thresh_pts.SetInputConnection(sample.GetOutputPort())
thresh_pts.SetThresholdFunction(thresh_pts.THRESHOLD_UPPER)
thresh_pts.SetUpperThreshold(0.8)

mapper2 = vtkPolyDataMapper()
mapper2.SetInputConnection(thresh_pts.GetOutputPort())
mapper2.SetScalarRange(0.8, 1.2)

actor2 = vtkActor()
actor2.SetMapper(mapper2)
actor2.SetPosition(2, 0, 0)

renderer = vtkRenderer()
renderer.AddActor(actor1)
renderer.AddActor(actor2)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
if "--non-interactive" not in sys.argv:
    interactor.Start()
