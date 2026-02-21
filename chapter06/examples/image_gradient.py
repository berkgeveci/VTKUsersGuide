#!/usr/bin/env python
"""Compute and display the 3D gradient of a CT volume."""

import os
import sys

from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Read the CT dataset
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataByteOrderToLittleEndian()
reader.SetImageRange(1, 93)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7FFF)

# Compute the 3D gradient
gradient = vtkImageGradient()
gradient.SetInputConnection(reader.GetOutputPort())
gradient.SetDimensionality(3)

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(gradient.GetOutputPort())
viewer.SetSlice(22)
viewer.SetColorWindow(400)
viewer.SetColorLevel(0)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
