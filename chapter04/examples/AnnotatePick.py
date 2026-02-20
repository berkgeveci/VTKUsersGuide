#!/usr/bin/env python3
#
# This example demonstrates cell picking using vtkCellPicker. It displays
# the results of picking using a vtkTextMapper.
#

from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkCellPicker,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTextMapper,
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

# Create the spikes by glyphing the sphere with a cone. Create the mapper
# and actor for the glyphs.
cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

spike_actor = vtkLODActor()
spike_actor.SetMapper(spike_mapper)

# Create a cell picker.
picker = vtkCellPicker()

# Create a text mapper and actor to display the results of picking.
text_mapper = vtkTextMapper()
tprop = text_mapper.GetTextProperty()
tprop.SetFontFamilyToArial()
tprop.SetFontSize(10)
tprop.BoldOn()
tprop.ShadowOn()
tprop.SetColor(1, 0, 0)

text_actor = vtkActor2D()
text_actor.VisibilityOff()
text_actor.SetMapper(text_mapper)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetPicker(picker)

# Add the actors to the renderer, set the background and size
renderer.AddViewProp(text_actor)
renderer.AddActor(sphere_actor)
renderer.AddActor(spike_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(600, 600)

# Get the camera and zoom in closer to the image.
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)


# Create a callback to annotate the pick.
def annotate_pick(obj, event):
    if picker.GetCellId() < 0:
        text_actor.VisibilityOff()
    else:
        sel_pt = picker.GetSelectionPoint()
        pick_pos = picker.GetPickPosition()
        text_mapper.SetInput(
            f"({pick_pos[0]:.6g}, {pick_pos[1]:.6g}, {pick_pos[2]:.6g})"
        )
        text_actor.SetPosition(sel_pt[0], sel_pt[1])
        text_actor.VisibilityOn()
    render_window.Render()


picker.AddObserver("EndPickEvent", annotate_pick)

interactor.Initialize()
render_window.Render()

# Pick the cell at this location.
picker.Pick(85, 126, 0, renderer)

interactor.Start()
