#!/usr/bin/env python3
#
# This simple example shows how to do basic rendering and pipeline
# creation. It also demonstrates the use of the LODActor.
#

import os

from vtkmodules.vtkIOGeometry import vtkSTLReader
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

# This reads a data file in STL format.
part = vtkSTLReader()
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
part.SetFileName(os.path.join(data_dir, "42400-IDGH.stl"))

# The mapper is responsible for pushing the geometry into the graphics
# library. It may also do color mapping, if scalars or other attributes
# are defined.
part_mapper = vtkPolyDataMapper()
part_mapper.SetInputConnection(part.GetOutputPort())

# The LOD actor is a special type of actor. It will change appearance in
# order to render faster. At the highest resolution, it renders everything
# just like an actor. The middle level is a point cloud, and the lowest
# level is a simple bounding box.
part_actor = vtkLODActor()
part_actor.SetMapper(part_mapper)
part_actor.GetProperty().SetColor(0.75, 0.75, 0.75)
part_actor.RotateX(30.0)
part_actor.RotateY(-45.0)

# Create the graphics structure. The renderer renders into the
# render window. The render window interactor captures mouse events
# and will perform appropriate camera or actor manipulation
# depending on the nature of the events.
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer, set the background and size
renderer.AddActor(part_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(600, 600)

# This starts the event loop and as a side effect causes an initial render.
interactor.Initialize()

# We'll zoom in a little by accessing the camera and invoking a "Zoom"
# method on it.
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)
render_window.Render()
interactor.Start()
