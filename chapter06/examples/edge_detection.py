"""Edge detection using Sobel, Laplacian, and gradient magnitude filters."""
import sys

from vtkmodules.vtkImagingGeneral import (
    vtkImageGradientMagnitude,
    vtkImageLaplacian,
    vtkImageSobel2D,
)
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a test image with geometric shapes.
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(1)
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(255)
canvas.FillBox(40, 120, 40, 120)
canvas.SetDrawColor(180)
canvas.FillBox(140, 220, 60, 200)
canvas.SetDrawColor(128)
canvas.DrawCircle(128, 128, 60)

# --- Sobel edge detection ---
sobel = vtkImageSobel2D()
sobel.SetInputConnection(canvas.GetOutputPort())

# --- Gradient magnitude ---
grad_mag = vtkImageGradientMagnitude()
grad_mag.SetInputConnection(canvas.GetOutputPort())
grad_mag.SetDimensionality(2)
grad_mag.HandleBoundariesOn()

# --- Laplacian ---
laplacian = vtkImageLaplacian()
laplacian.SetInputConnection(canvas.GetOutputPort())
laplacian.SetDimensionality(2)

# Display gradient magnitude result.
viewer = vtkImageViewer2()
viewer.SetInputConnection(grad_mag.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
