#!/usr/bin/env python
"""Warp an image by scalar luminance and merge data (Section 5.1)."""
import os
from vtkmodules.vtkFiltersCore import vtkMergeFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read a BMP image and compute luminance.
reader = vtkBMPReader()
reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

luminance = vtkImageLuminance()
luminance.SetInputConnection(reader.GetOutputPort())

geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(luminance.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(geometry.GetOutputPort())
warp.SetScaleFactor(-0.1)

# Merge warped geometry with original image scalars.
merge = vtkMergeFilter()
merge.SetGeometryConnection(warp.GetOutputPort())
merge.SetScalarsConnection(reader.GetOutputPort())

mapper = vtkDataSetMapper()
mapper.SetInputConnection(merge.GetOutputPort())
mapper.SetScalarRange(0, 255)

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(800, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(actor)
ren.ResetCamera()
ren.GetActiveCamera().Azimuth(20)
ren.GetActiveCamera().Elevation(30)
ren.SetBackground(0.1, 0.2, 0.4)
ren.ResetCameraClippingRange()
ren.GetActiveCamera().Zoom(1.4)

iren.Initialize()
ren_win.Render()
iren.Start()
