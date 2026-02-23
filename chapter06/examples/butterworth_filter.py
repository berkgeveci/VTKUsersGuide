"""Butterworth low-pass filtering in the frequency domain."""
import sys

from vtkmodules.vtkImagingFourier import (
    vtkImageButterworthLowPass,
    vtkImageFFT,
    vtkImageRFFT,
)
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageExtractComponents
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a test image with sharp geometric shapes.
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToFloat()
canvas.SetNumberOfScalarComponents(1)
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(255)
canvas.FillBox(80, 180, 80, 180)
canvas.SetDrawColor(128)
canvas.DrawCircle(128, 128, 80)

# Forward FFT.
fft = vtkImageFFT()
fft.SetInputConnection(canvas.GetOutputPort())
fft.SetDimensionality(2)

# Apply Butterworth low-pass filter in frequency domain.
# This attenuates high frequencies, producing a smooth (blurred) result.
butterworth = vtkImageButterworthLowPass()
butterworth.SetInputConnection(fft.GetOutputPort())
butterworth.SetCutOff(0.1)
butterworth.SetOrder(2)

# Inverse FFT to get back to spatial domain.
rfft = vtkImageRFFT()
rfft.SetInputConnection(butterworth.GetOutputPort())
rfft.SetDimensionality(2)

# Extract real component and cast for display.
extract = vtkImageExtractComponents()
extract.SetInputConnection(rfft.GetOutputPort())
extract.SetComponents(0)

cast = vtkImageCast()
cast.SetInputConnection(extract.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Display the filtered result.
viewer = vtkImageViewer2()
viewer.SetInputConnection(cast.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
