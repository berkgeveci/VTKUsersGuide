#!/usr/bin/env python
"""Sample a quadric function over a volume, extract a slice, and contour it."""

import os
import sys

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Quadric definition — coefficients set the shape of the implicit function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

# Evaluate the quadric over a regular 30x30x30 lattice
sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()
sample.Update()

# Extract a single slice from the volume
extract = vtkExtractVOI()
extract.SetInputConnection(sample.GetOutputPort())
extract.SetVOI(0, 29, 0, 29, 15, 15)
extract.SetSampleRate(1, 2, 3)

# Contour the slice to produce 2D contour lines
contours = vtkContourFilter()
contours.SetInputConnection(extract.GetOutputPort())
contours.GenerateValues(13, 0.0, 1.2)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contours.GetOutputPort())
contour_mapper.SetScalarRange(0.0, 1.2)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Create an outline of the sampled data
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.SetBackground(1, 1, 1)
renderer.AddActor(contour_actor)
renderer.AddActor(outline_actor)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
render_window.Render()
interactor.Start()
