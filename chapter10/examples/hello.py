#!/usr/bin/env python3
"""Implicit modeling from lines spelling the word 'hello'.

Reads hello.vtk (polylines forming the word HELLO), uses
vtkImplicitModeller to compute a distance field, and contours
the result to create a smooth 3D surface around the text.
"""

import os

from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Create lines which serve as the "seed" geometry
reader = vtkPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "hello.vtk"))

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(reader.GetOutputPort())
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
line_actor.GetProperty().SetLineWidth(2)

# Create implicit model with distance field and contour it
imp = vtkImplicitModeller()
imp.SetInputConnection(reader.GetOutputPort())
imp.SetSampleDimensions(110, 40, 20)
imp.SetMaximumDistance(0.25)
imp.SetModelBounds(-1.0, 10.0, -1.0, 3.0, -1.0, 1.0)

contour = vtkContourFilter()
contour.SetInputConnection(imp.GetOutputPort())
contour.SetValue(0, 0.25)

imp_mapper = vtkPolyDataMapper()
imp_mapper.SetInputConnection(contour.GetOutputPort())
imp_mapper.ScalarVisibilityOff()

imp_actor = vtkActor()
imp_actor.SetMapper(imp_mapper)
imp_actor.GetProperty().SetColor(0.2, 0.6, 0.6)
imp_actor.GetProperty().SetOpacity(0.5)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(imp_actor)
renderer.AddActor(line_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(1000, 600)
renderer.ResetCamera()

render_window.Render()
interactor.Start()
