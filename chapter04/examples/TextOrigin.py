#!/usr/bin/env python3
#
# This example demonstrates the use of vtkVectorText and vtkFollower.
# vtkVectorText is used to create 3D annotation. vtkFollower is used to
# position the 3D text and to ensure that the text always faces the
# renderer's active camera (i.e., the text is always readable).
#

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkFollower,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create simple axes using cones pointing in x, y, z directions
# X axis (red)
x_cone = vtkConeSource()
x_cone.SetResolution(20)
x_cone.SetHeight(0.5)
x_cone.SetRadius(0.05)
x_cone.SetDirection(1, 0, 0)
x_cone.SetCenter(0.25, 0, 0)
x_mapper = vtkPolyDataMapper()
x_mapper.SetInputConnection(x_cone.GetOutputPort())
x_actor = vtkActor()
x_actor.SetMapper(x_mapper)
x_actor.GetProperty().SetColor(1, 0, 0)

# Y axis (green)
y_cone = vtkConeSource()
y_cone.SetResolution(20)
y_cone.SetHeight(0.5)
y_cone.SetRadius(0.05)
y_cone.SetDirection(0, 1, 0)
y_cone.SetCenter(0, 0.25, 0)
y_mapper = vtkPolyDataMapper()
y_mapper.SetInputConnection(y_cone.GetOutputPort())
y_actor = vtkActor()
y_actor.SetMapper(y_mapper)
y_actor.GetProperty().SetColor(0, 1, 0)

# Z axis (blue)
z_cone = vtkConeSource()
z_cone.SetResolution(20)
z_cone.SetHeight(0.5)
z_cone.SetRadius(0.05)
z_cone.SetDirection(0, 0, 1)
z_cone.SetCenter(0, 0, 0.25)
z_mapper = vtkPolyDataMapper()
z_mapper.SetInputConnection(z_cone.GetOutputPort())
z_actor = vtkActor()
z_actor.SetMapper(z_mapper)
z_actor.GetProperty().SetColor(0, 0, 1)

# Create the 3D text and the associated mapper and follower (a type of
# actor). Position the text so it is displayed over the origin of the axes.
a_text = vtkVectorText()
a_text.SetText("Origin")

text_mapper = vtkPolyDataMapper()
text_mapper.SetInputConnection(a_text.GetOutputPort())

text_actor = vtkFollower()
text_actor.SetMapper(text_mapper)
text_actor.SetScale(0.2, 0.2, 0.2)
text_actor.AddPosition(0, -0.1, 0)

# Create the Renderer, RenderWindow, and RenderWindowInteractor.
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer.
renderer.AddActor(x_actor)
renderer.AddActor(y_actor)
renderer.AddActor(z_actor)
renderer.AddActor(text_actor)

# Zoom in closer.
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.6)

# Reset the clipping range of the camera; set the camera of the follower;
# render.
renderer.ResetCameraClippingRange()
text_actor.SetCamera(renderer.GetActiveCamera())
render_window.Render()
interactor.Start()
