"""Demonstrate volume cropping using cropping region planes.

Reads the iron protein dataset and renders it with cropping enabled,
showing only a subvolume defined by six axis-aligned planes.

See Chapter 7, Section 7.10.
"""

import os

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
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

# Read the iron protein dataset
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(data_dir, "ironProt.vtk"))

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

# Create the mapper with cropping enabled
xmin, xmax = 10.0, 50.0
ymin, ymax = 0.0, 33.0
zmin, zmax = 21.0, 47.0

volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())
volume_mapper.CroppingOn()
volume_mapper.SetCroppingRegionPlanes(xmin, xmax, ymin, ymax, zmin, zmax)
volume_mapper.SetCroppingRegionFlagsToSubVolume()

# Create the volume
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Standard rendering setup
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

render_window.SetWindowName("Volume Cropping")
render_window.Render()
interactor.Start()
