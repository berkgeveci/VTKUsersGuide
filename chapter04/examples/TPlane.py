#!/usr/bin/env python3
#
# This simple example shows how to do basic texture mapping.
#

import os

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTexture,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Load in the texture map. A texture is any unsigned char image. If it
# is not of this type, you will have to map it through a lookup table
# or by using vtkImageShiftScale.
bmp_reader = vtkBMPReader()
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

a_texture = vtkTexture()
a_texture.SetInputConnection(bmp_reader.GetOutputPort())
a_texture.InterpolateOn()

# Create a plane source and actor. The vtkPlaneSource generates
# texture coordinates.
plane = vtkPlaneSource()
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.SetTexture(a_texture)

# Create the RenderWindow, Renderer and both Actors
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer, set the background and size
renderer.AddActor(plane_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(500, 500)

# Render the image
render_window.Render()

renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(-30)
camera.Roll(-20)
renderer.ResetCameraClippingRange()
render_window.Render()
interactor.Start()
