#!/usr/bin/env python3
"""Model an ice cream cone using boolean combinations of implicit functions.

Demonstrates vtkImplicitBoolean with intersection and difference operations
to combine a cone, planes, and spheres into an ice cream cone with a bite
taken out of it.
"""

from vtkmodules.vtkCommonDataModel import (
    vtkCone, vtkImplicitBoolean, vtkPlane, vtkSphere,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create implicit function primitives
cone = vtkCone()
cone.SetAngle(20)
vert_plane = vtkPlane()
vert_plane.SetOrigin(0.1, 0, 0)
vert_plane.SetNormal(-1, 0, 0)
base_plane = vtkPlane()
base_plane.SetOrigin(1.2, 0, 0)
base_plane.SetNormal(1, 0, 0)
ice_cream = vtkSphere()
ice_cream.SetCenter(1.333, 0, 0)
ice_cream.SetRadius(0.5)
bite = vtkSphere()
bite.SetCenter(1.5, 0, 0.5)
bite.SetRadius(0.25)

# Combine primitives to build ice-cream cone
the_cone = vtkImplicitBoolean()
the_cone.SetOperationTypeToIntersection()
the_cone.AddFunction(cone)
the_cone.AddFunction(vert_plane)
the_cone.AddFunction(base_plane)

# Take a bite out of the ice cream
the_cream = vtkImplicitBoolean()
the_cream.SetOperationTypeToDifference()
the_cream.AddFunction(ice_cream)
the_cream.AddFunction(bite)

# Sample and contour the cone
cone_sample = vtkSampleFunction()
cone_sample.SetImplicitFunction(the_cone)
cone_sample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
cone_sample.SetSampleDimensions(60, 60, 60)
cone_sample.ComputeNormalsOff()

cone_surface = vtkContourFilter()
cone_surface.SetInputConnection(cone_sample.GetOutputPort())
cone_surface.SetValue(0, 0.0)
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_surface.GetOutputPort())
cone_mapper.ScalarVisibilityOff()
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(0.82, 0.41, 0.12)

# Sample and contour the ice cream
cream_sample = vtkSampleFunction()
cream_sample.SetImplicitFunction(the_cream)
cream_sample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
cream_sample.SetSampleDimensions(60, 60, 60)
cream_sample.ComputeNormalsOff()

cream_surface = vtkContourFilter()
cream_surface.SetInputConnection(cream_sample.GetOutputPort())
cream_surface.SetValue(0, 0.0)
cream_mapper = vtkPolyDataMapper()
cream_mapper.SetInputConnection(cream_surface.GetOutputPort())
cream_mapper.ScalarVisibilityOff()
cream_actor = vtkActor()
cream_actor.SetMapper(cream_mapper)
cream_actor.GetProperty().SetColor(0.74, 0.99, 0.79)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(cone_actor)
renderer.AddActor(cream_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)

renderer.ResetCamera()
renderer.GetActiveCamera().Roll(90)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

render_window.Render()
interactor.Start()
