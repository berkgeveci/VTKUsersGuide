#!/usr/bin/env python3
#
# This example demonstrates the use of vtkCubeAxesActor2D to indicate
# the position in space that the camera is currently viewing. The
# vtkCubeAxesActor2D draws axes on the bounding box of the data set
# and labels the axes with x-y-z coordinates.
#

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401

# Create a superquadric source and compute normals for nice shading.
superquadric = vtkSuperquadricSource()
superquadric.SetPhiResolution(32)
superquadric.SetThetaResolution(32)

normals = vtkPolyDataNormals()
normals.SetInputConnection(superquadric.GetOutputPort())

# Set up the associated mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())
actor = vtkLODActor()
actor.SetMapper(mapper)

# Create a camera and set the camera parameters.
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(5, 3, 3)
camera.SetViewUp(0, 1, 0)

# Create a light.
light = vtkLight()
light.SetFocalPoint(0, 0, 0)
light.SetPosition(5, 3, 3)

# Create the Renderers. Assign them the appropriate viewport
# coordinates, active camera, and light.
renderer = vtkRenderer()
renderer.SetViewport(0, 0, 0.5, 1.0)
renderer.SetActiveCamera(camera)
renderer.AddLight(light)

renderer2 = vtkRenderer()
renderer2.SetViewport(0.5, 0, 1.0, 1.0)
renderer2.SetActiveCamera(camera)
renderer2.AddLight(light)

# Create the RenderWindow and RenderWindowInteractor.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.AddRenderer(renderer2)
render_window.SetWindowName("VTK - Cube Axes")
render_window.SetSize(600, 300)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderers.
renderer.AddViewProp(actor)
renderer2.AddViewProp(actor)

renderer.SetBackground(0.1, 0.2, 0.4)
renderer2.SetBackground(0.1, 0.2, 0.4)

# Create a text property for both cube axes
tprop = vtkTextProperty()
tprop.SetColor(1, 1, 1)
tprop.ShadowOn()

# Create a vtkCubeAxesActor2D. Use the outer edges of the bounding box to
# draw the axes. Add the actor to the renderer.
axes = vtkCubeAxesActor2D()
axes.SetInputConnection(normals.GetOutputPort())
axes.SetCamera(renderer.GetActiveCamera())
axes.SetLabelFormat("%6.4g")
axes.SetFlyModeToOuterEdges()
axes.SetFontFactor(0.8)
axes.SetAxisTitleTextProperty(tprop)
axes.SetAxisLabelTextProperty(tprop)
renderer.AddViewProp(axes)

# Create a vtkCubeAxesActor2D. Use the closest vertex to the camera to
# determine where to draw the axes. Add the actor to the renderer.
axes2 = vtkCubeAxesActor2D()
axes2.SetViewProp(actor)
axes2.SetCamera(renderer2.GetActiveCamera())
axes2.SetLabelFormat("%6.4g")
axes2.SetFlyModeToClosestTriad()
axes2.SetFontFactor(0.8)
axes2.ScalingOff()
axes2.SetAxisTitleTextProperty(tprop)
axes2.SetAxisLabelTextProperty(tprop)
renderer2.AddViewProp(axes2)

interactor.Initialize()
render_window.Render()
interactor.Start()
