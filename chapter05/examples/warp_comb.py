#!/usr/bin/env python
"""Extract and warp computational planes (Section 5.3)."""
import os
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read PLOT3D combustor data.
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

block = pl3d.GetOutput().GetBlock(0)

# Extract three computational planes.
plane = vtkStructuredGridGeometryFilter()
plane.SetInputData(block)
plane.SetExtent(10, 10, 1, 100, 1, 100)

plane2 = vtkStructuredGridGeometryFilter()
plane2.SetInputData(block)
plane2.SetExtent(30, 30, 1, 100, 1, 100)

plane3 = vtkStructuredGridGeometryFilter()
plane3.SetInputData(block)
plane3.SetExtent(45, 45, 1, 100, 1, 100)

# Append and warp.
append_f = vtkAppendPolyData()
append_f.AddInputConnection(plane.GetOutputPort())
append_f.AddInputConnection(plane2.GetOutputPort())
append_f.AddInputConnection(plane3.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(append_f.GetOutputPort())
warp.UseNormalOn()
warp.SetNormal(1.0, 0.0, 0.0)
warp.SetScaleFactor(2.5)

normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())
normals.SetFeatureAngle(60)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(normals.GetOutputPort())
plane_mapper.SetScalarRange(block.GetScalarRange())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Outline.
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(block)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(500, 500)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(plane_actor)
ren.SetBackground(1, 1, 1)

cam1 = ren.GetActiveCamera()
cam1.SetClippingRange(3.95297, 50)
cam1.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam1.SetPosition(-12.3332, 31.7479, 41.2387)
cam1.SetViewUp(0.060772, -0.319905, 0.945498)

iren.Initialize()
ren_win.Render()
iren.Start()
