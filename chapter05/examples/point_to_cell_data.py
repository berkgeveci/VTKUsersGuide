#!/usr/bin/env python
"""Convert point data to cell data and threshold (Section 5.1)."""
import os
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersCore import vtkPointDataToCellData
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read unstructured grid.
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
reader.SetScalarsName("thickness9")
reader.SetVectorsName("displacement9")

# Convert point data to cell data.
p2c = vtkPointDataToCellData()
p2c.SetInputConnection(reader.GetOutputPort())
p2c.PassPointDataOn()

warp = vtkWarpVector()
warp.SetInputConnection(p2c.GetOutputPort())

# Threshold using cell data.
thresh = vtkThreshold()
thresh.SetInputConnection(warp.GetOutputPort())
thresh.SetThresholdFunction(thresh.THRESHOLD_BETWEEN)
thresh.SetLowerThreshold(0.25)
thresh.SetUpperThreshold(0.75)
thresh.SetInputArrayToProcess(0, 0, 0, 1, "thickness9")  # 1 = CELL

mapper = vtkDataSetMapper()
mapper.SetInputConnection(thresh.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(actor)
ren.SetBackground(0.1, 0.2, 0.4)

iren.Initialize()
ren_win.Render()
iren.Start()
