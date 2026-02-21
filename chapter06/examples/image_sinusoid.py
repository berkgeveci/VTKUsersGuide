#!/usr/bin/env python
"""Create a sinusoidal volume, cast to unsigned char, and volume render it."""

import os
import sys

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

# Create a sinusoidal source
sinusoid = vtkImageSinusoidSource()
sinusoid.SetWholeExtent(0, 99, 0, 99, 0, 99)
sinusoid.SetAmplitude(63)
sinusoid.SetDirection(1, 0, 0)
sinusoid.SetPeriod(25)

# Cast from double to unsigned char for volume rendering
cast = vtkImageCast()
cast.SetInputConnection(sinusoid.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Volume rendering
mapper = vtkFixedPointVolumeRayCastMapper()
mapper.SetInputConnection(cast.GetOutputPort())

# Transfer functions
color_tf = vtkColorTransferFunction()
color_tf.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(64, 1.0, 0.0, 0.0)
color_tf.AddRGBPoint(128, 1.0, 1.0, 0.0)
color_tf.AddRGBPoint(255, 1.0, 1.0, 1.0)

opacity_tf = vtkPiecewiseFunction()
opacity_tf.AddPoint(0, 0.0)
opacity_tf.AddPoint(64, 0.2)
opacity_tf.AddPoint(128, 0.5)
opacity_tf.AddPoint(255, 1.0)

volume_property = vtkVolumeProperty()
volume_property.SetColor(color_tf)
volume_property.SetScalarOpacity(opacity_tf)
volume_property.ShadeOff()

volume = vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volume_property)

# Outline bounding box
outline = vtkOutlineFilter()
outline.SetInputConnection(cast.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.ResetCamera()

interactor.Initialize()
render_window.Render()
interactor.Start()
