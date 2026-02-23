"""Custom VTK source implemented in Python using VTKPythonAlgorithmBase."""
import sys
import math

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonCore import vtkPoints, vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401


class SpiralSource(VTKPythonAlgorithmBase):
    """A source that generates a 3D spiral polyline with scalar data."""

    def __init__(self):
        super().__init__(nInputPorts=0, nOutputPorts=1, outputType="vtkPolyData")
        self._num_points = 200
        self._num_turns = 5

    def SetNumberOfPoints(self, n):
        self._num_points = n
        self.Modified()

    def SetNumberOfTurns(self, n):
        self._num_turns = n
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        output = vtkPolyData.GetData(outInfo)

        points = vtkPoints()
        scalars = vtkFloatArray()
        scalars.SetName("ArcLength")

        for i in range(self._num_points):
            t = i / (self._num_points - 1)
            angle = 2.0 * math.pi * self._num_turns * t
            r = 0.5 * t
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            z = t
            points.InsertNextPoint(x, y, z)
            scalars.InsertNextValue(t)

        line = vtkCellArray()
        line.InsertNextCell(self._num_points)
        for i in range(self._num_points):
            line.InsertCellPoint(i)

        output.SetPoints(points)
        output.SetLines(line)
        output.GetPointData().SetScalars(scalars)
        return 1


# Use the custom source in a pipeline.
source = SpiralSource()
source.SetNumberOfPoints(500)
source.SetNumberOfTurns(8)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())
mapper.SetScalarRange(0, 1)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(3)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
if "--non-interactive" not in sys.argv:
    interactor.Start()
