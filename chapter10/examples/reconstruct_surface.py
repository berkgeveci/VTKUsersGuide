#!/usr/bin/env python3
"""Surface reconstruction from an unorganized point cloud.

Reads cactus.3337.pts and uses vtkSurfaceReconstructionFilter
to build a surface, then contours and corrects normals for display.
"""

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkImagingHybrid import vtkSurfaceReconstructionFilter
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkReverseSense
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Read points from file
points = vtkPoints()
with open(os.path.join(data_dir, "cactus.3337.pts")) as f:
    for line in f:
        tokens = line.split()
        if tokens and tokens[0] == "p":
            x, y, z = float(tokens[1]), float(tokens[2]), float(tokens[3])
            points.InsertNextPoint(x, y, z)

point_cloud = vtkPolyData()
point_cloud.SetPoints(points)

# Construct the surface and create isosurface
surf = vtkSurfaceReconstructionFilter()
surf.SetInputData(point_cloud)

cf = vtkContourFilter()
cf.SetInputConnection(surf.GetOutputPort())
cf.SetValue(0, 0.0)

# Reverse normals (they may point inward)
reverse = vtkReverseSense()
reverse.SetInputConnection(cf.GetOutputPort())
reverse.ReverseCellsOn()
reverse.ReverseNormalsOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reverse.GetOutputPort())
mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(mapper)
surface_actor.GetProperty().SetDiffuseColor(1.0, 0.39, 0.28)
surface_actor.GetProperty().SetSpecularColor(1, 1, 1)
surface_actor.GetProperty().SetSpecular(0.4)
surface_actor.GetProperty().SetSpecularPower(50)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(surface_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)
renderer.ResetCamera()

render_window.Render()
interactor.Start()
