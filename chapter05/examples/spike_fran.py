#!/usr/bin/env python
"""Glyphing surface normals with cones (Figure 5-3)."""
import os
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkMaskPoints
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read the Cyberware data and generate normals.
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals

fran = vtkPolyDataReader()
fran.SetFileName(os.path.join(data_dir, "fran_cut.vtk"))

normals = vtkPolyDataNormals()
normals.SetInputConnection(fran.GetOutputPort())
normals.FlipNormalsOn()

fran_mapper = vtkPolyDataMapper()
fran_mapper.SetInputConnection(normals.GetOutputPort())

fran_actor = vtkActor()
fran_actor.SetMapper(fran_mapper)
fran_actor.GetProperty().SetColor(1.0, 0.49, 0.25)

# Subsample points for glyphing.
pt_mask = vtkMaskPoints()
pt_mask.SetInputConnection(normals.GetOutputPort())
pt_mask.SetOnRatio(10)
pt_mask.RandomModeOn()

# Cone glyph, translated so its base is at the origin.
cone = vtkConeSource()
cone.SetResolution(6)

transform = vtkTransform()
transform.Translate(0.5, 0.0, 0.0)

transform_f = vtkTransformPolyDataFilter()
transform_f.SetInputConnection(cone.GetOutputPort())
transform_f.SetTransform(transform)

# Create glyphs oriented by surface normals.
glyph = vtkGlyph3D()
glyph.SetInputConnection(pt_mask.GetOutputPort())
glyph.SetSourceConnection(transform_f.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.004)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

spike_actor = vtkActor()
spike_actor.SetMapper(spike_mapper)
spike_actor.GetProperty().SetColor(0.0, 0.79, 0.34)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(500, 500)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(fran_actor)
ren.AddActor(spike_actor)
ren.SetBackground(0.1, 0.2, 0.4)

ren.ResetCamera()
ren.GetActiveCamera().Zoom(1.4)
ren.GetActiveCamera().Azimuth(110)

iren.Initialize()
ren_win.Render()
iren.Start()
