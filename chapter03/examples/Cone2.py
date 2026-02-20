#!/usr/bin/env python
#
# This example shows how to add an observer to a Python program.
#
# VTK uses a command/observer design pattern. That is, observers watch for
# particular events that any vtkObject (or subclass) may invoke on
# itself. For example, the vtkRenderer invokes a "StartEvent" as it begins
# to render. Here we add an observer that invokes a command when this event
# is observed.
#

import time

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401


def my_callback(obj, event):
    print("Starting a render")


# Create the pipeline
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)

renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Add the observer here
renderer.AddObserver("StartEvent", my_callback)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)

# Loop over 360 degrees and render the cone each time
for i in range(360):
    time.sleep(0.03)
    render_window.Render()
    renderer.GetActiveCamera().Azimuth(1)
