#!/usr/bin/env python
"""Blend a grid pattern with a slice from a CT dataset."""

import os
import sys

from vtkmodules.vtkImagingCore import vtkImageBlend
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Read a single slice from the CT dataset
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataByteOrderToLittleEndian()
reader.SetImageRange(22, 22)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7FFF)

# Create a grid pattern
image_grid = vtkImageGridSource()
image_grid.SetGridSpacing(16, 16, 0)
image_grid.SetGridOrigin(0, 0, 0)
image_grid.SetDataExtent(0, 63, 0, 63, 0, 0)
image_grid.SetLineValue(4095)
image_grid.SetFillValue(0)
image_grid.SetDataScalarTypeToUnsignedShort()

# Blend the grid pattern with the CT slice
blend = vtkImageBlend()
blend.SetOpacity(0, 0.5)
blend.SetOpacity(1, 0.5)
blend.AddInputConnection(reader.GetOutputPort())
blend.AddInputConnection(image_grid.GetOutputPort())

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(blend.GetOutputPort())
viewer.SetColorWindow(1000)
viewer.SetColorLevel(500)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
