#!/usr/bin/env python
"""Decimation followed by smoothing (Figure 5-12)."""
import os
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkPolyDataNormals,
    vtkSmoothPolyDataFilter,
)
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read the Cyberware data.
fran = vtkPolyDataReader()
fran.SetFileName(os.path.join(data_dir, "fran_cut.vtk"))

# Decimate then smooth.
deci = vtkDecimatePro()
deci.SetInputConnection(fran.GetOutputPort())
deci.SetTargetReduction(0.9)
deci.PreserveTopologyOn()

smoother = vtkSmoothPolyDataFilter()
smoother.SetInputConnection(deci.GetOutputPort())
smoother.SetNumberOfIterations(50)

normals = vtkPolyDataNormals()
normals.SetInputConnection(smoother.GetOutputPort())
normals.FlipNormalsOn()

fran_mapper = vtkPolyDataMapper()
fran_mapper.SetInputConnection(normals.GetOutputPort())

fran_actor = vtkActor()
fran_actor.SetMapper(fran_mapper)
fran_actor.GetProperty().SetColor(1.0, 0.49, 0.25)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(250, 250)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(fran_actor)
ren.SetBackground(1, 1, 1)

cam1 = vtkCamera()
cam1.SetClippingRange(0.0475572, 2.37786)
cam1.SetFocalPoint(0.052665, -0.129454, -0.0573973)
cam1.SetPosition(0.327637, -0.116299, -0.256418)
cam1.SetViewUp(-0.0225386, 0.999137, 0.034901)
ren.SetActiveCamera(cam1)

iren.Initialize()
ren_win.Render()
iren.Start()
