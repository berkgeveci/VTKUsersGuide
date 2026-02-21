#!/usr/bin/env python
"""Generate texture coordinates on a Delaunay triangulation (Section 5.2)."""
import os
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersTexture import (
    vtkTextureMapToCylinder,
    vtkTransformTextureCoords,
)
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Generate 25 random points and triangulate.
sphere = vtkPointSource()
sphere.SetNumberOfPoints(25)

delny = vtkDelaunay3D()
delny.SetInputConnection(sphere.GetOutputPort())
delny.SetTolerance(0.01)

# Generate texture coordinates.
tmapper = vtkTextureMapToCylinder()
tmapper.SetInputConnection(delny.GetOutputPort())
tmapper.PreventSeamOn()

# Scale texture coords for repeats.
xform = vtkTransformTextureCoords()
xform.SetInputConnection(tmapper.GetOutputPort())
xform.SetScale(4, 4, 1)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(xform.GetOutputPort())

# Load a texture map.
bmp_reader = vtkBMPReader()
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

atext = vtkTexture()
atext.SetInputConnection(bmp_reader.GetOutputPort())
atext.InterpolateOn()

triangulation = vtkActor()
triangulation.SetMapper(mapper)
triangulation.SetTexture(atext)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(300, 300)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(triangulation)
ren.SetBackground(1, 1, 1)

iren.Initialize()
ren_win.Render()
iren.Start()
