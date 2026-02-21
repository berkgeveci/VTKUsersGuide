#!/usr/bin/env python
"""Manually create vtkPolyData with a triangle strip (Section 5.2)."""
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Define eight points for a triangle strip.
points = vtkPoints()
points.InsertPoint(0, 0.0, 0.0, 0.0)
points.InsertPoint(1, 0.0, 1.0, 0.0)
points.InsertPoint(2, 1.0, 0.0, 0.0)
points.InsertPoint(3, 1.0, 1.0, 0.0)
points.InsertPoint(4, 2.0, 0.0, 0.0)
points.InsertPoint(5, 2.0, 1.0, 0.0)
points.InsertPoint(6, 3.0, 0.0, 0.0)
points.InsertPoint(7, 3.0, 1.0, 0.0)

# Build the strip cell.
strips = vtkCellArray()
strips.InsertNextCell(8)
for i in range(8):
    strips.InsertCellPoint(i)

# Create the polydata.
profile = vtkPolyData()
profile.SetPoints(points)
profile.SetStrips(strips)

mapper = vtkPolyDataMapper()
mapper.SetInputData(profile)

strip_actor = vtkActor()
strip_actor.SetMapper(mapper)
strip_actor.GetProperty().SetColor(0.3800, 0.7000, 0.1600)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(strip_actor)
ren.SetBackground(1, 1, 1)

iren.Initialize()
ren_win.Render()
iren.Start()
