#!/usr/bin/env python3
#
# This simple example shows how to do basic rendering and pipeline
# creation. It also demonstrates the use of a procedural source object
# (vtkCylinderSource).
#

from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# This creates a polygonal cylinder model with eight circumferential
# facets.
cylinder = vtkCylinderSource()
cylinder.SetResolution(8)

# The mapper is responsible for pushing the geometry into the graphics
# library. It may also do color mapping, if scalars or other
# attributes are defined.
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

# The actor is a grouping mechanism: besides the geometry (mapper), it
# also has a property, transformation matrix, and/or texture map.
# Here we set its color and rotate it.
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(1.0, 0.3882, 0.2784)  # tomato
cylinder_actor.RotateX(30.0)
cylinder_actor.RotateY(-45.0)

# Create the graphics structure. The renderer renders into the render
# window. The render window interactor captures mouse events and will
# perform appropriate camera or actor manipulation depending on the
# nature of the events.
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer, set the background and size
renderer.AddActor(cylinder_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(200, 200)

# This allows the interactor to initialize itself. It has to be
# called before an event loop.
interactor.Initialize()

# We'll zoom in a little by accessing the camera and invoking a "Zoom"
# method on it.
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)
render_window.Render()

# Start the event loop.
interactor.Start()
