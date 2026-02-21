#!/usr/bin/env python
"""Perform XOR boolean logic on two ellipsoid images."""

import os
import sys

from vtkmodules.vtkImagingMath import vtkImageLogic
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create two overlapping ellipsoid images
sphere1 = vtkImageEllipsoidSource()
sphere1.SetCenter(95, 100, 0)
sphere1.SetRadius(70, 70, 70)

sphere2 = vtkImageEllipsoidSource()
sphere2.SetCenter(161, 100, 0)
sphere2.SetRadius(70, 70, 70)

# Perform XOR operation
xor = vtkImageLogic()
xor.SetInputConnection(0, sphere1.GetOutputPort())
xor.SetInputConnection(1, sphere2.GetOutputPort())
xor.SetOutputTrueValue(150)
xor.SetOperationToXor()

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(xor.GetOutputPort())
viewer.SetColorWindow(255)
viewer.SetColorLevel(127.5)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
