#!/usr/bin/env python
"""Extract cells using implicit function (Figure 5-9)."""
from vtkmodules.vtkCommonDataModel import vtkQuadric, vtkSphere
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create an implicit quadric and sample it.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(50, 50, 50)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

# Two ellipsoids combined as a boolean union.
trans = vtkTransform()
trans.Scale(1, 0.5, 0.333)
sphere = vtkSphere()
sphere.SetRadius(0.25)
sphere.SetTransform(trans)

trans2 = vtkTransform()
trans2.Scale(0.25, 0.5, 1.0)
sphere2 = vtkSphere()
sphere2.SetRadius(0.25)
sphere2.SetTransform(trans2)

from vtkmodules.vtkCommonDataModel import vtkImplicitBoolean

union = vtkImplicitBoolean()
union.AddFunction(sphere)
union.AddFunction(sphere2)
union.SetOperationTypeToUnion()

# Extract cells inside the implicit function and shrink them.
extract = vtkExtractGeometry()
extract.SetInputConnection(sample.GetOutputPort())
extract.SetImplicitFunction(union)

shrink = vtkShrinkFilter()
shrink.SetInputConnection(extract.GetOutputPort())
shrink.SetShrinkFactor(0.5)

data_mapper = vtkDataSetMapper()
data_mapper.SetInputConnection(shrink.GetOutputPort())

data_actor = vtkActor()
data_actor.SetMapper(data_mapper)

# Outline for context.
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(500, 500)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(outline_actor)
ren.AddActor(data_actor)
ren.SetBackground(1, 1, 1)
ren.ResetCamera()
ren.GetActiveCamera().Zoom(1.5)

iren.Initialize()
ren_win.Render()
iren.Start()
