#!/usr/bin/env python
"""Apply Gaussian smoothing to a CT volume and display a slice."""

import os
import sys

from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
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

# Apply 2D Gaussian smoothing
smooth = vtkImageGaussianSmooth()
smooth.SetInputConnection(reader.GetOutputPort())
smooth.SetDimensionality(2)
smooth.SetStandardDeviations(2, 10)

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(smooth.GetOutputPort())
viewer.SetSlice(22)
viewer.SetColorWindow(2000)
viewer.SetColorLevel(1000)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
