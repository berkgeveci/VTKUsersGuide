#!/usr/bin/env python3
#
# This example demonstrates the use of vtkAssembly. In an assembly,
# the motion of one actor affects the position of other actors.
#

from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAssembly,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create four parts: a top level assembly (in this case, a vtkCylinder)
# and three primitives (using vtkSphereSource, vtkCubeSource, and
# vtkConeSource). Set up mappers and actors for each part of the
# assembly to carry information about material properties and
# associated geometry.
sphere = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetOrigin(2, 1, 3)
sphere_actor.RotateY(6)
sphere_actor.SetPosition(2.25, 0, 0)
sphere_actor.GetProperty().SetColor(1, 0, 1)

cube = vtkCubeSource()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.SetPosition(0.0, 0.25, 0)
cube_actor.GetProperty().SetColor(0, 0, 1)

cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 0.25)
cone_actor.GetProperty().SetColor(0, 1, 0)

# Top part of the assembly
cylinder = vtkCylinderSource()
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())
cylinder_mapper.SetResolveCoincidentTopologyToPolygonOffset()
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(1, 0, 0)

# Create the assembly and add the 4 parts to it. Also set the origin,
# position and orientation in space.
assembly = vtkAssembly()
assembly.AddPart(cylinder_actor)
assembly.AddPart(sphere_actor)
assembly.AddPart(cube_actor)
assembly.AddPart(cone_actor)
assembly.SetOrigin(5, 10, 15)
assembly.AddPosition(5, 0, 0)
assembly.RotateX(15)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer, set the background and size
renderer.AddActor(assembly)
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(600, 600)

# Set up the camera to get a particular view of the scene
camera = vtkCamera()
camera.SetClippingRange(21.9464, 30.0179)
camera.SetFocalPoint(3.49221, 2.28844, -0.970866)
camera.SetPosition(3.49221, 2.28844, 24.5216)
camera.SetViewAngle(30)
camera.SetViewUp(0, 1, 0)
renderer.SetActiveCamera(camera)

render_window.Render()
interactor.Start()
