"""Warp a sphere by a vector field to visualize displacement."""
import sys
import math

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a sphere.
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)
sphere.Update()

output = sphere.GetOutput()

# Create a displacement vector field: radial expansion that varies with
# the azimuthal angle, creating a star-like deformation.
vectors = vtkDoubleArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(output.GetNumberOfPoints())
vectors.SetName("Displacement")

for i in range(output.GetNumberOfPoints()):
    pt = output.GetPoint(i)
    r = math.sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)
    if r > 0:
        theta = math.atan2(pt[1], pt[0])
        scale = 0.2 * (1.0 + 0.5 * math.sin(5 * theta))
        vectors.SetTuple3(i, pt[0] / r * scale, pt[1] / r * scale, pt[2] / r * scale)
    else:
        vectors.SetTuple3(i, 0, 0, 0)

output.GetPointData().SetVectors(vectors)

# Warp the sphere by the displacement vectors.
warp = vtkWarpVector()
warp.SetInputData(output)
warp.SetScaleFactor(1.0)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.3, 0.6, 0.9)

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
