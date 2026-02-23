"""Image convolution with a custom sharpening kernel."""
import sys

from vtkmodules.vtkImagingGeneral import vtkImageConvolve
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a test image with geometric shapes.
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToFloat()
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

# Apply a 3x3 sharpening kernel.
convolve = vtkImageConvolve()
convolve.SetInputConnection(canvas.GetOutputPort())

# Sharpening kernel: center-surround
kernel = [
     0, -1,  0,
    -1,  5, -1,
     0, -1,  0,
]
convolve.SetKernel3x3(kernel)

# Display convolved result.
viewer = vtkImageViewer2()
viewer.SetInputConnection(convolve.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
