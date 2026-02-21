#!/usr/bin/env python
"""Create a sinusoidal image volume using vtkImageSinusoidSource."""

import os
import sys

from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a sinusoidal source
sinusoid = vtkImageSinusoidSource()
sinusoid.SetWholeExtent(0, 99, 0, 99, 0, 99)
sinusoid.SetAmplitude(63)
sinusoid.SetDirection(1, 0, 0)
sinusoid.SetPeriod(25)

# Create an outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sinusoid.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.ResetCamera()

interactor.Initialize()
render_window.Render()
interactor.Start()
