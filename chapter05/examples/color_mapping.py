#!/usr/bin/env python
"""Custom lookup table for color mapping (Figure 5-1)."""
import os
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a sampled quadric to provide scalar data.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)

contours = vtkContourFilter()
contours.SetInputConnection(sample.GetOutputPort())
contours.GenerateValues(5, 0.0, 1.2)

# Build a custom lookup table.
lut = vtkLookupTable()
lut.SetNumberOfColors(64)
lut.SetHueRange(0.0, 0.667)
lut.Build()

# Replace every group of four colors with red, green, blue, black.
red = [1.0, 0.0, 0.0, 1.0]
green = [0.0, 1.0, 0.0, 1.0]
blue = [0.0, 0.0, 1.0, 1.0]
black = [0.0, 0.0, 0.0, 1.0]
for i in range(16):
    lut.SetTableValue(i * 4, *red)
    lut.SetTableValue(i * 4 + 1, *green)
    lut.SetTableValue(i * 4 + 2, *blue)
    lut.SetTableValue(i * 4 + 3, *black)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetLookupTable(lut)
plane_mapper.SetInputConnection(contours.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(plane_actor)
ren.SetBackground(1, 1, 1)

iren.Initialize()
ren_win.Render()
iren.Start()
