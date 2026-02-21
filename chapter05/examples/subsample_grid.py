#!/usr/bin/env python
"""Subsample a structured grid (Section 5.3)."""
import os
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
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

# Subsample the grid.
extract = vtkExtractGrid()
extract.SetInputData(block)
extract.SetVOI(30, 30, -1000, 1000, -1000, 1000)
extract.SetSampleRate(1, 2, 3)
extract.IncludeBoundaryOn()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(extract.GetOutputPort())
mapper.SetScalarRange(0.18, 0.7)

actor = vtkActor()
actor.SetMapper(mapper)

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
ren_win.SetSize(1200, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(actor)
ren.SetBackground(1, 1, 1)

cam1 = ren.GetActiveCamera()
cam1.SetClippingRange(2.64586, 47.905)
cam1.SetFocalPoint(8.931, 0.358127, 31.3526)
cam1.SetPosition(29.7111, -0.688615, 37.1495)
cam1.SetViewUp(-0.268328, 0.00801595, 0.963294)

iren.Initialize()
ren_win.Render()
iren.Start()
