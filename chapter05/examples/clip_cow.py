#!/usr/bin/env python
"""Clip a polygonal model of a cow (Figure 5-13)."""
import os
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkCutter,
    vtkPolyDataNormals,
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

peacock = (0.26, 0.44, 0.56)
tomato = (1.0, 0.388, 0.278)

# Read cow model and generate normals.
cow = vtkBYUReader()
cow.SetGeometryFileName(os.path.join(data_dir, "cow.g"))

cow_normals = vtkPolyDataNormals()
cow_normals.SetInputConnection(cow.GetOutputPort())

# Clip with a plane.
plane = vtkPlane()
plane.SetOrigin(0.25, 0, 0)
plane.SetNormal(-1, -1, 0)

clipper = vtkClipPolyData()
clipper.SetInputConnection(cow_normals.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()
clipper.SetValue(0.5)

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

back_prop = vtkProperty()
back_prop.SetDiffuseColor(*tomato)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(*peacock)
clip_actor.SetBackfaceProperty(back_prop)

# Cut edges to close the clipped boundary.
cut_edges = vtkCutter()
cut_edges.SetInputConnection(cow_normals.GetOutputPort())
cut_edges.SetCutFunction(plane)
cut_edges.GenerateCutScalarsOn()
cut_edges.SetValue(0, 0.5)

cut_strips = vtkStripper()
cut_strips.SetInputConnection(cut_edges.GetOutputPort())
cut_strips.Update()

cut_poly = vtkPolyData()
cut_poly.SetPoints(cut_strips.GetOutput().GetPoints())
cut_poly.SetPolys(cut_strips.GetOutput().GetLines())

cut_triangles = vtkTriangleFilter()
cut_triangles.SetInputData(cut_poly)

cut_mapper2 = vtkPolyDataMapper()
cut_mapper2.SetInputConnection(cut_triangles.GetOutputPort())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper2)
cut_actor.GetProperty().SetColor(*peacock)

# Render the clipped-away portion as wireframe.
rest_mapper = vtkPolyDataMapper()
rest_mapper.SetInputConnection(clipper.GetClippedOutputPort())
rest_mapper.ScalarVisibilityOff()

rest_actor = vtkActor()
rest_actor.SetMapper(rest_mapper)
rest_actor.GetProperty().SetRepresentationToWireframe()

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(300, 300)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(clip_actor)
ren.AddActor(cut_actor)
ren.AddActor(rest_actor)
ren.SetBackground(1, 1, 1)

ren.ResetCamera()
ren.GetActiveCamera().Azimuth(30)
ren.GetActiveCamera().Elevation(30)
ren.GetActiveCamera().Dolly(1.5)
ren.ResetCameraClippingRange()

iren.Initialize()
ren_win.Render()
iren.Start()
