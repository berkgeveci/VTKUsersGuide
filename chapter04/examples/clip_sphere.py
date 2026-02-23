"""Clip a sphere with a plane, showing the clipped and remaining portions."""
import sys

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a sphere source.
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)

# Define a clip plane through the origin.
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 0, 0)

# Clip the sphere; generate the clipped-away output too.
clipper = vtkClipPolyData()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClippedOutputOn()

# The kept portion (solid).
kept_mapper = vtkPolyDataMapper()
kept_mapper.SetInputConnection(clipper.GetOutputPort())

kept_actor = vtkActor()
kept_actor.SetMapper(kept_mapper)
kept_actor.GetProperty().SetColor(0.26, 0.44, 0.56)

# The clipped-away portion (wireframe).
clipped_mapper = vtkPolyDataMapper()
clipped_mapper.SetInputConnection(clipper.GetClippedOutputPort())

clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetRepresentationToWireframe()
clipped_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

# Render
renderer = vtkRenderer()
renderer.AddActor(kept_actor)
renderer.AddActor(clipped_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
