#!/usr/bin/env python3
"""2D Delaunay triangulation of random points.

Generates random points, triangulates them with vtkDelaunay2D, and
visualizes the result with tubes around edges and spheres at vertices.
"""

from vtkmodules.vtkCommonCore import vtkMath, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay2D, vtkExtractEdges, vtkGlyph3D, vtkTubeFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Generate some random points
math = vtkMath()
points = vtkPoints()
for i in range(50):
    points.InsertPoint(i, math.Random(0, 1), math.Random(0, 1), 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Perform a 2D Delaunay triangulation
delny = vtkDelaunay2D()
delny.SetInputData(profile)
delny.SetTolerance(0.001)

mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(delny.GetOutputPort())
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(0.1, 0.2, 0.4)

# Wrap edges in tubes
extract = vtkExtractEdges()
extract.SetInputConnection(delny.GetOutputPort())
tubes = vtkTubeFilter()
tubes.SetInputConnection(extract.GetOutputPort())
tubes.SetRadius(0.01)
tubes.SetNumberOfSides(6)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(0.2, 0.6, 0.6)
edge_actor.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor.GetProperty().SetSpecular(0.3)
edge_actor.GetProperty().SetSpecularPower(20)

# Place spheres at the points
ball = vtkSphereSource()
ball.SetRadius(0.025)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)
balls = vtkGlyph3D()
balls.SetInputConnection(delny.GetOutputPort())
balls.SetSourceConnection(ball.GetOutputPort())

ball_mapper = vtkPolyDataMapper()
ball_mapper.SetInputConnection(balls.GetOutputPort())
ball_actor = vtkActor()
ball_actor.SetMapper(ball_mapper)
ball_actor.GetProperty().SetColor(1.0, 0.38, 0.68)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(ball_actor)
renderer.AddActor(edge_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

render_window.Render()
interactor.Start()
