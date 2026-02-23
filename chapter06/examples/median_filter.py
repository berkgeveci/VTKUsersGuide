"""Median filtering to remove salt-and-pepper noise."""
import sys

from vtkmodules.vtkImagingGeneral import vtkImageMedian3D
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D, vtkImageNoiseSource
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

# Add noise.
noise = vtkImageNoiseSource()
noise.SetWholeExtent(0, 255, 0, 255, 0, 0)
noise.SetMinimum(0)
noise.SetMaximum(50)

add = vtkImageMathematics()
add.SetOperationToAdd()
add.SetInputConnection(0, canvas.GetOutputPort())
add.SetInputConnection(1, noise.GetOutputPort())

# Apply median filter with 3x3x1 kernel.
median = vtkImageMedian3D()
median.SetInputConnection(add.GetOutputPort())
median.SetKernelSize(3, 3, 1)

# Display filtered result.
viewer = vtkImageViewer2()
viewer.SetInputConnection(median.GetOutputPort())
viewer.GetRenderWindow().SetSize(400, 400)
viewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)
viewer.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
