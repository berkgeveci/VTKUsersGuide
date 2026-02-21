#!/usr/bin/env python
"""Color an isosurface with another scalar (Figure 5-8)."""
import os
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkPolyDataNormals
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read PLOT3D data; add function 153 (VelocityMagnitude).
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.AddFunction(153)
pl3d.Update()

block = pl3d.GetOutput().GetBlock(0)

# Generate an isosurface colored by VelocityMagnitude.
iso = vtkContourFilter()
iso.SetInputData(block)
iso.SetValue(0, 0.24)

normals = vtkPolyDataNormals()
normals.SetInputConnection(iso.GetOutputPort())
normals.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOn()
iso_mapper.SetScalarRange(0, 1500)
iso_mapper.SetScalarModeToUsePointFieldData()
iso_mapper.ColorByArrayComponent("VelocityMagnitude", 0)

iso_actor = vtkLODActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.SetNumberOfCloudPoints(1000)

# Outline.
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(block)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(800, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(iso_actor)
ren.SetBackground(0.1, 0.2, 0.4)

cam1 = ren.GetActiveCamera()
cam1.SetClippingRange(3.95297, 50)
cam1.SetFocalPoint(9.71821, 0.458166, 29.3999)
cam1.SetPosition(2.7439, -37.3196, 38.7167)
cam1.SetViewUp(-0.16123, 0.264271, 0.950876)

iren.Initialize()
ren_win.Render()
iren.Start()
