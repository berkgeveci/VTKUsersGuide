#!/usr/bin/env python
"""Probing combustor data with planes (Figure 5-7)."""
import os
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkContourFilter, vtkProbeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
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

# Create three probe planes.
plane = vtkPlaneSource()
plane.SetResolution(50, 50)

def make_probe_plane(translate, plane_src):
    trans = vtkTransform()
    trans.Translate(*translate)
    trans.Scale(5, 5, 5)
    trans.RotateY(90)
    tpd = vtkTransformPolyDataFilter()
    tpd.SetInputConnection(plane_src.GetOutputPort())
    tpd.SetTransform(trans)
    out = vtkOutlineFilter()
    out.SetInputConnection(tpd.GetOutputPort())
    m = vtkPolyDataMapper()
    m.SetInputConnection(out.GetOutputPort())
    a = vtkActor()
    a.SetMapper(m)
    a.GetProperty().SetColor(0, 0, 0)
    return tpd, a

tpd1, tpd1_actor = make_probe_plane((3.7, 0.0, 28.37), plane)
tpd2, tpd2_actor = make_probe_plane((9.2, 0.0, 31.20), plane)
tpd3, tpd3_actor = make_probe_plane((13.27, 0.0, 33.30), plane)

# Append all three planes.
append_f = vtkAppendPolyData()
append_f.AddInputConnection(tpd1.GetOutputPort())
append_f.AddInputConnection(tpd2.GetOutputPort())
append_f.AddInputConnection(tpd3.GetOutputPort())

# Probe the structured grid data.
probe = vtkProbeFilter()
probe.SetInputConnection(append_f.GetOutputPort())
probe.SetSourceData(block)

# Contour the probed data.
contour = vtkContourFilter()
contour.SetInputConnection(probe.GetOutputPort())
contour.GenerateValues(50, block.GetScalarRange())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(block.GetScalarRange())

plane_actor = vtkActor()
plane_actor.SetMapper(contour_mapper)

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
ren_win.SetSize(800, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(plane_actor)
ren.AddActor(tpd1_actor)
ren.AddActor(tpd2_actor)
ren.AddActor(tpd3_actor)
ren.SetBackground(1, 1, 1)

ren.ResetCamera()
cam1 = ren.GetActiveCamera()
cam1.SetClippingRange(3.95297, 50)
cam1.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam1.SetPosition(-12.3332, 31.7479, 41.2387)
cam1.SetViewUp(0.060772, -0.319905, 0.945498)

iren.Initialize()
ren_win.Render()
iren.Start()
