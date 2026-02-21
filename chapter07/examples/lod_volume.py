"""Demonstrate vtkLODProp3D with multiple volume rendering techniques.

Creates a vtkLODProp3D with three levels of detail:
  - Low resolution: GPU ray casting on downsampled data
  - Medium resolution: GPU ray casting on full data
  - High resolution: fixed-point (software) ray casting on full data

The LOD prop automatically selects the appropriate level based on
the allocated rendering time.

See Chapter 7, Section 7.21.
"""

import os

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkLODProp3D,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import (
    vtkFixedPointVolumeRayCastMapper,
    vtkGPUVolumeRayCastMapper,
)

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

# Read the iron protein dataset
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(data_dir, "ironProt.vtk"))

# Resample the data at half resolution for the low-res LOD
resampler = vtkImageResample()
resampler.SetInputConnection(reader.GetOutputPort())
resampler.SetAxisMagnificationFactor(0, 0.5)
resampler.SetAxisMagnificationFactor(1, 0.5)
resampler.SetAxisMagnificationFactor(2, 0.5)

# Create transfer functions
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(20, 0.0)
opacity_transfer_function.AddPoint(255, 0.2)

color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
color_transfer_function.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

# Low-res LOD: GPU ray casting on downsampled data
lowres_mapper = vtkGPUVolumeRayCastMapper()
lowres_mapper.SetInputConnection(resampler.GetOutputPort())

# Medium-res LOD: GPU ray casting on full data
medres_mapper = vtkGPUVolumeRayCastMapper()
medres_mapper.SetInputConnection(reader.GetOutputPort())

# High-res LOD: software ray casting on full data
hires_mapper = vtkFixedPointVolumeRayCastMapper()
hires_mapper.SetInputConnection(reader.GetOutputPort())

# Create the LOD prop with three levels
volume_lod = vtkLODProp3D()
volume_lod.AddLOD(lowres_mapper, volume_property, 0.0)
volume_lod.AddLOD(medres_mapper, volume_property, 0.0)
volume_lod.AddLOD(hires_mapper, volume_property, 0.0)

# Standard rendering setup
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume_lod)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

render_window.SetWindowName("LOD Volume Rendering")
render_window.Render()
interactor.Start()
