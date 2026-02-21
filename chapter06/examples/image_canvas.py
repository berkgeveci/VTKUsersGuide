#!/usr/bin/env python
"""Draw various primitives on a blank canvas using vtkImageCanvasSource2D."""

import os
import sys

from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a 512x512 canvas
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetExtent(0, 511, 0, 511, 0, 0)

# Draw various primitives
canvas.SetDrawColor(86)
canvas.FillBox(0, 511, 0, 511)
canvas.SetDrawColor(0)
canvas.FillTube(500, 20, 30, 400, 5)
canvas.SetDrawColor(255)
canvas.DrawSegment(10, 20, 500, 510)
canvas.SetDrawColor(0)
canvas.DrawCircle(400, 350, 80.0)
canvas.SetDrawColor(255)
canvas.FillPixel(450, 350)
canvas.SetDrawColor(170)
canvas.FillTriangle(100, 100, 300, 150, 150, 300)

# Display the result
viewer = vtkImageViewer2()
viewer.SetInputConnection(canvas.GetOutputPort())
viewer.SetColorWindow(256)
viewer.SetColorLevel(127.5)

interactor = vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

viewer.Render()
interactor.Initialize()
interactor.Start()
