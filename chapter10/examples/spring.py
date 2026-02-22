#!/usr/bin/env python3
"""Model a spring using rotational extrusion.

Demonstrates vtkRotationalExtrusionFilter by sweeping an octagonal
profile along a helical path to create a spring shape.
"""

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create spring profile (an octagonal approximation to a disk)
points = vtkPoints()
points.InsertPoint(0, 1.0, 0.0, 0.0)
points.InsertPoint(1, 1.0732, 0.0, -0.1768)
points.InsertPoint(2, 1.25, 0.0, -0.25)
points.InsertPoint(3, 1.4268, 0.0, -0.1768)
points.InsertPoint(4, 1.5, 0.0, 0.0)
points.InsertPoint(5, 1.4268, 0.0, 0.1768)
points.InsertPoint(6, 1.25, 0.0, 0.25)
points.InsertPoint(7, 1.0732, 0.0, 0.1768)

poly = vtkCellArray()
poly.InsertNextCell(8, [0, 1, 2, 3, 4, 5, 6, 7])

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetPolys(poly)

# Extrude profile to make spring
extrude = vtkRotationalExtrusionFilter()
extrude.SetInputData(profile)
extrude.SetResolution(360)
extrude.SetTranslation(6)
extrude.SetDeltaRadius(1.0)
extrude.SetAngle(2160.0)  # six revolutions

normals = vtkPolyDataNormals()
normals.SetInputConnection(extrude.GetOutputPort())
normals.SetFeatureAngle(60)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

spring = vtkActor()
spring.SetMapper(mapper)
spring.GetProperty().SetColor(0.69, 0.77, 0.87)
spring.GetProperty().SetDiffuse(0.7)
spring.GetProperty().SetSpecular(0.4)
spring.GetProperty().SetSpecularPower(20)
spring.GetProperty().BackfaceCullingOn()

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(spring)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)
renderer.ResetCamera()

render_window.Render()
interactor.Start()
