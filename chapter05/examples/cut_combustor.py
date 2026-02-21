#!/usr/bin/env python
"""Cutting a combustor with a plane (Figure 5-6)."""
import os
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
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

# Cut with a plane.
plane = vtkPlane()
plane.SetOrigin(block.GetCenter())
plane.SetNormal(-0.287, 0, 0.9579)

plane_cut = vtkCutter()
plane_cut.SetInputData(block)
plane_cut.SetCutFunction(plane)

cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(plane_cut.GetOutputPort())
cut_mapper.SetScalarRange(
    block.GetPointData().GetScalars().GetRange()
)

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Extract a computational plane as wireframe for comparison.
comp_plane = vtkStructuredGridGeometryFilter()
comp_plane.SetInputData(block)
comp_plane.SetExtent(0, 100, 0, 100, 9, 9)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(comp_plane.GetOutputPort())
plane_mapper.ScalarVisibilityOff()

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetRepresentationToWireframe()
plane_actor.GetProperty().SetColor(0, 0, 0)

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
ren_win.SetSize(1000, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(plane_actor)
ren.AddActor(cut_actor)
ren.SetBackground(1, 1, 1)

cam1 = ren.GetActiveCamera()
cam1.SetClippingRange(11.1034, 59.5328)
cam1.SetFocalPoint(9.71821, 0.458166, 29.3999)
cam1.SetPosition(-2.95748, -26.7271, 44.5309)
cam1.SetViewUp(0.0184785, 0.479657, 0.877262)

iren.Initialize()
ren_win.Render()
iren.Start()
