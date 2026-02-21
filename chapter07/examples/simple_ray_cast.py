"""Simple volume rendering example using vtkGPUVolumeRayCastMapper.

Reads the iron protein dataset and renders it using GPU-accelerated
ray casting with composite blending. Demonstrates the basic volume
rendering pipeline: reader -> mapper -> volume (with property).

See Chapter 7, Section 7.2.
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

# Create transfer mapping scalar value to opacity
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(20, 0.0)
opacity_transfer_function.AddPoint(255, 0.2)

# Create transfer mapping scalar value to color
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
color_transfer_function.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# The property describes how the data will look
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

# The mapper knows how to render the data
volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Standard rendering setup
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

render_window.SetWindowName("Simple Volume Rendering")
render_window.Render()
interactor.Start()
