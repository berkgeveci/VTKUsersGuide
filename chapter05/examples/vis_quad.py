#!/usr/bin/env python
"""Contour filter on a sampled implicit function (Figure 5-2)."""
import os
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Create an implicit quadric function and sample it.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)

# Generate five contour surfaces.
contours = vtkContourFilter()
contours.SetInputConnection(sample.GetOutputPort())
contours.GenerateValues(5, 0.0, 1.2)

cont_mapper = vtkPolyDataMapper()
cont_mapper.SetInputConnection(contours.GetOutputPort())
cont_mapper.SetScalarRange(0.0, 1.2)

cont_actor = vtkActor()
cont_actor.SetMapper(cont_mapper)

# Outline for context.
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.SetBackground(1, 1, 1)
ren.AddActor(cont_actor)
ren.AddActor(outline_actor)

iren.Initialize()
ren_win.Render()
iren.Start()
