"""Custom VTK filter implemented in Python using VTKPythonAlgorithmBase."""
import sys
import math

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
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


class DistanceToPointFilter(VTKPythonAlgorithmBase):
    """Computes the Euclidean distance from each point to a reference point."""

    def __init__(self):
        super().__init__(
            nInputPorts=1, inputType="vtkPolyData",
            nOutputPorts=1, outputType="vtkPolyData",
        )
        self._reference_point = (0.0, 0.0, 0.0)

    def SetReferencePoint(self, x, y, z):
        self._reference_point = (x, y, z)
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        inp = vtkPolyData.GetData(inInfo[0])
        output = vtkPolyData.GetData(outInfo)

        # Copy input geometry to output.
        output.ShallowCopy(inp)

        # Compute distance from each point to the reference point.
        rx, ry, rz = self._reference_point
        distances = vtkFloatArray()
        distances.SetName("Distance")
        distances.SetNumberOfTuples(output.GetNumberOfPoints())

        for i in range(output.GetNumberOfPoints()):
            pt = output.GetPoint(i)
            d = math.sqrt((pt[0] - rx)**2 + (pt[1] - ry)**2 + (pt[2] - rz)**2)
            distances.SetValue(i, d)

        output.GetPointData().SetScalars(distances)
        return 1


# Use the custom filter in a pipeline.
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)

dist_filter = DistanceToPointFilter()
dist_filter.SetInputConnection(sphere.GetOutputPort())
dist_filter.SetReferencePoint(1.0, 0.0, 0.0)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(dist_filter.GetOutputPort())
mapper.SetScalarRange(0, 2)

actor = vtkActor()
actor.SetMapper(mapper)

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
