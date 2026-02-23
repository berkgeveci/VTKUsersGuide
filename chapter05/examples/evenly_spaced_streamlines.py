"""Demonstrate vtkEvenlySpacedStreamlines2D for automatic seed placement."""
import sys

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersFlowPaths import vtkEvenlySpacedStreamlines2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a 2D vector field: a simple vortex.
dims = [64, 64, 1]
image = vtkImageData()
image.SetDimensions(dims)
image.SetOrigin(0, 0, 0)
image.SetSpacing(1.0 / (dims[0] - 1), 1.0 / (dims[1] - 1), 1.0)

vectors = vtkDoubleArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(dims[0] * dims[1])
vectors.SetName("Velocity")

cx, cy = 0.5, 0.5
for j in range(dims[1]):
    for i in range(dims[0]):
        x = i * image.GetSpacing()[0]
        y = j * image.GetSpacing()[1]
        dx = -(y - cy)
        dy = x - cx
        idx = j * dims[0] + i
        vectors.SetTuple3(idx, dx, dy, 0.0)

image.GetPointData().SetVectors(vectors)

# Use evenly-spaced streamlines for automatic seed placement.
streamer = vtkEvenlySpacedStreamlines2D()
streamer.SetInputData(image)
streamer.SetStartPosition(0.5, 0.1, 0.0)
streamer.SetSeparatingDistance(0.1)
streamer.SetInitialIntegrationStep(0.5)
streamer.SetIntegrationStepUnit(1)  # 1 = CELL_LENGTH_UNIT
streamer.SetMaximumNumberOfSteps(500)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(streamer.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.4, 0.8)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.ResetCamera()
render_window.Render()

if "--non-interactive" not in sys.argv:
    interactor.Start()
