#!/usr/bin/env python
"""Reslice a BMP image with a 45-degree rotation using vtkImageReslice."""

import os
import sys

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Read the BMP image
reader = vtkBMPReader()
reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

# Create a 45-degree rotation with scaling
transform = vtkTransform()
transform.RotateZ(45)
transform.Scale(1.414, 1.414, 1.414)

# Reslice the image using the transform
reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToCubic()
reslice.WrapOn()
reslice.AutoCropOutputOn()

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(reslice.GetOutputPort())
viewer.SetSlice(0)
viewer.SetColorWindow(256.0)
viewer.SetColorLevel(127.5)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
