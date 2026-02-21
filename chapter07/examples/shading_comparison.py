"""Compare geometric and volumetric shading with colored lights.

Renders a geometric sphere (right) and a volumetric sphere (left) with
the same lighting coefficients and three colored lights (red, green, blue)
to show that volume rendering can reproduce geometric shading.

See Chapter 7, Section 7.8.
"""

import os

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

# --- Geometric sphere (right side) ---
sphere = vtkSphereSource()
sphere.SetRadius(20)
sphere.SetCenter(70, 25, 25)
sphere.SetThetaResolution(50)
sphere.SetPhiResolution(50)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 1, 1)
actor.GetProperty().SetAmbient(0.01)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetSpecularPower(70.0)

# --- Volumetric sphere (left side) ---
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
reader = vtkSLCReader()
reader.SetFileName(os.path.join(data_dir, "sphere.slc"))

# Use a constant white transfer function for both opacity and color
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddSegment(0, 1.0, 255, 1.0)

# Make the volume property match the geometric one
volume_property = vtkVolumeProperty()
volume_property.SetColor(opacity_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()
volume_property.SetDiffuse(0.7)
volume_property.SetAmbient(0.01)
volume_property.SetSpecular(0.5)
volume_property.SetSpecularPower(70.0)

volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# --- Rendering setup ---
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.AddActor(actor)

# Create red, green, and blue lights
red_light = vtkLight()
red_light.SetColor(1, 0, 0)
red_light.SetPosition(1000, 25, 25)
red_light.SetFocalPoint(25, 25, 25)
red_light.SetIntensity(0.5)

green_light = vtkLight()
green_light.SetColor(0, 1, 0)
green_light.SetPosition(25, 1000, 25)
green_light.SetFocalPoint(25, 25, 25)
green_light.SetIntensity(0.5)

blue_light = vtkLight()
blue_light.SetColor(0, 0, 1)
blue_light.SetPosition(25, 25, 1000)
blue_light.SetFocalPoint(25, 25, 25)
blue_light.SetIntensity(0.5)

renderer.AddLight(red_light)
renderer.AddLight(green_light)
renderer.AddLight(blue_light)

renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

render_window.SetWindowName("Shading Comparison")
render_window.Render()
interactor.Start()
