"""Morphological operations: dilation, erosion, opening, and closing."""
import sys

from vtkmodules.vtkImagingMorphological import (
    vtkImageDilateErode3D,
    vtkImageOpenClose3D,
)
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a binary test image with geometric shapes.
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(1)
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(255)
canvas.FillBox(40, 120, 40, 120)
canvas.SetDrawColor(255)
canvas.FillBox(150, 210, 80, 180)
# Add a thin line and small dots to show morphological effects.
canvas.SetDrawColor(255)
canvas.FillBox(60, 62, 150, 230)  # thin vertical line
canvas.FillBox(180, 183, 20, 23)  # small dot

# --- Dilation: expands bright regions ---
dilate = vtkImageDilateErode3D()
dilate.SetInputConnection(canvas.GetOutputPort())
dilate.SetKernelSize(5, 5, 1)
dilate.SetDilateValue(255)
dilate.SetErodeValue(0)

# --- Erosion: shrinks bright regions ---
erode = vtkImageDilateErode3D()
erode.SetInputConnection(canvas.GetOutputPort())
erode.SetKernelSize(5, 5, 1)
erode.SetDilateValue(0)
erode.SetErodeValue(255)

# --- Opening (erosion then dilation): removes small bright features ---
opening = vtkImageOpenClose3D()
opening.SetInputConnection(canvas.GetOutputPort())
opening.SetKernelSize(5, 5, 1)
opening.SetOpenValue(255)
opening.SetCloseValue(0)

# --- Closing (dilation then erosion): fills small dark gaps ---
closing = vtkImageOpenClose3D()
closing.SetInputConnection(canvas.GetOutputPort())
closing.SetKernelSize(5, 5, 1)
closing.SetOpenValue(0)
closing.SetCloseValue(255)

# Display the dilation result.
viewer = vtkImageViewer2()
viewer.SetInputConnection(dilate.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
