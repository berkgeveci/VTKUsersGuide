"""Resample an unstructured dataset onto a regular image grid."""
import sys

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkResampleToImage, vtkThreshold
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

# Create an unstructured grid by thresholding a sampled quadric.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

thresh = vtkThreshold()
thresh.SetInputConnection(sample.GetOutputPort())
thresh.SetThresholdFunction(thresh.THRESHOLD_BETWEEN)
thresh.SetLowerThreshold(0.5)
thresh.SetUpperThreshold(1.5)

# Resample the unstructured grid onto a uniform image grid.
resample = vtkResampleToImage()
resample.SetInputConnection(thresh.GetOutputPort())
resample.SetSamplingDimensions(40, 40, 40)

# Threshold the resampled image to show only valid data.
thresh2 = vtkThreshold()
thresh2.SetInputConnection(resample.GetOutputPort())
thresh2.SetInputArrayToProcess(0, 0, 0, 0, "vtkValidPointMask")
thresh2.SetThresholdFunction(thresh2.THRESHOLD_UPPER)
thresh2.SetUpperThreshold(1)

surface = vtkGeometryFilter()
surface.SetInputConnection(thresh2.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarRange(0.5, 1.5)

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
