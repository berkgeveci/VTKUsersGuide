#!/usr/bin/env python3
#
# This example demonstrates the use of 2D text.
#

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTextActor,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a sphere source, mapper, and actor
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkLODActor()
sphere_actor.SetMapper(sphere_mapper)

# Create a scaled text actor.
# Set the text, font, justification, and properties (bold, italics, etc.).
text_actor = vtkTextActor()
text_actor.SetTextScaleModeToProp()
text_actor.SetDisplayPosition(90, 50)
text_actor.SetInput("This is a sphere")

# Set coordinates to match the old vtkScaledTextActor default value
text_actor.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
text_actor.GetPosition2Coordinate().SetValue(0.6, 0.1)

tprop = text_actor.GetTextProperty()
tprop.SetFontSize(18)
tprop.SetFontFamilyToArial()
tprop.SetJustificationToCentered()
tprop.BoldOn()
tprop.ItalicOn()
tprop.ShadowOn()
tprop.SetColor(0, 0, 1)

# Create the Renderer, RenderWindow, RenderWindowInteractor
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer; set the background and size; zoom in;
# and render.
renderer.AddViewProp(text_actor)
renderer.AddActor(sphere_actor)

renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)
render_window.Render()
interactor.Start()
