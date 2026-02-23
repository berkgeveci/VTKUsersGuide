"""Compute and display the FFT magnitude spectrum of an image."""
import sys

from vtkmodules.vtkImagingFourier import vtkImageFFT, vtkImageFourierCenter
from vtkmodules.vtkImagingCore import vtkImageExtractComponents, vtkImageCast
from vtkmodules.vtkImagingMath import vtkImageMagnitude, vtkImageLogarithmicScale
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
canvas.FillBox(80, 180, 80, 180)

# Forward FFT (output is complex: 2 components).
fft = vtkImageFFT()
fft.SetInputConnection(canvas.GetOutputPort())
fft.SetDimensionality(2)

# Center the zero-frequency component.
center = vtkImageFourierCenter()
center.SetInputConnection(fft.GetOutputPort())
center.SetDimensionality(2)

# Compute magnitude of complex values.
mag = vtkImageMagnitude()
mag.SetInputConnection(center.GetOutputPort())

# Log scale for better visualization.
log_scale = vtkImageLogarithmicScale()
log_scale.SetInputConnection(mag.GetOutputPort())
log_scale.SetConstant(15)

# Cast to unsigned char for display.
cast = vtkImageCast()
cast.SetInputConnection(log_scale.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Display the spectrum.
viewer = vtkImageViewer2()
viewer.SetInputConnection(cast.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
