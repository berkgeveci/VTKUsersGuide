#!/usr/bin/env python3
#
# This example demonstrates how to use the vtkImplicitPlaneWidget to clip
# an object. A "mace" is created from a sphere and cone glyphs located at
# the sphere points and oriented in the direction of the sphere normals.
# The mace is clipped with a plane that separates it into two parts, one
# of which is colored green.
#

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkImplicitPlaneWidget
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a mace out of filters.
sphere = vtkSphereSource()
cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

# The sphere and spikes are appended into a single polydata.
# This just makes things simpler to manage.
apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(apd.GetOutputPort())

mace_actor = vtkLODActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# This portion of the code clips the mace with the vtkPlane
# implicit function. The clipped region is colored green.
plane = vtkPlane()

clipper = vtkClipPolyData()
clipper.SetInputConnection(apd.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkLODActor()
select_actor.SetMapper(select_mapper)
select_actor.GetProperty().SetColor(0, 1, 0)
select_actor.VisibilityOff()
select_actor.SetScale(1.01, 1.01, 1.01)

# Create the RenderWindow, Renderer and both Actors
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Associate the plane widget with the interactor
plane_widget = vtkImplicitPlaneWidget()
plane_widget.SetInteractor(interactor)
plane_widget.SetPlaceFactor(1.25)
plane_widget.SetInputConnection(glyph.GetOutputPort())
plane_widget.PlaceWidget()


def my_callback(obj, event):
    obj.GetPlane(plane)
    select_actor.VisibilityOn()


plane_widget.AddObserver("InteractionEvent", my_callback)

renderer.AddActor(mace_actor)
renderer.AddActor(select_actor)

# Set the background and size
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(800, 800)

render_window.Render()

# Enable the widget by pressing 'i'
interactor.Start()
