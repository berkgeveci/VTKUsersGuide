#!/usr/bin/env python
"""Warp an image slice by its scalar values to create a 3D surface."""

import os
import sys

from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkWindowLevelLookupTable,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Read a single slice from the CT dataset
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataByteOrderToLittleEndian()
reader.SetImageRange(40, 40)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7FFF)

# Convert the image to polydata so we can warp it
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(reader.GetOutputPort())

# Warp the geometry by scalar values
warp = vtkWarpScalar()
warp.SetInputConnection(geometry.GetOutputPort())
warp.SetScaleFactor(0.005)

# Use a grayscale lookup table
wl_lut = vtkWindowLevelLookupTable()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(0, 2000)
mapper.SetLookupTable(wl_lut)

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.ResetCamera()

interactor.Initialize()
render_window.Render()
interactor.Start()
