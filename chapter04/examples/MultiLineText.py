#!/usr/bin/env python3
#
# This example demonstrates the use of multiline 2D text using
# vtkTextMappers. It shows several justifications as well as
# single-line and multiple-line text inputs.
#

from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkCoordinate,
    vtkPolyDataMapper2D,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkTextMapper,
    vtkTextProperty,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkCommonCore import vtkPoints

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401

font_size = 14

# Create common text properties for single-line and multi-line text.
single_line_text_prop = vtkTextProperty()
single_line_text_prop.SetFontSize(font_size)
single_line_text_prop.SetFontFamilyToArial()
single_line_text_prop.BoldOff()
single_line_text_prop.ItalicOff()
single_line_text_prop.ShadowOff()

multi_line_text_prop = vtkTextProperty()
multi_line_text_prop.ShallowCopy(single_line_text_prop)
multi_line_text_prop.BoldOn()
multi_line_text_prop.ItalicOn()
multi_line_text_prop.ShadowOn()
multi_line_text_prop.SetLineSpacing(0.8)

# The text is on a single line and bottom-justified.
single_line_text_b = vtkTextMapper()
single_line_text_b.SetInput("Single line (bottom)")
tprop = single_line_text_b.GetTextProperty()
tprop.ShallowCopy(single_line_text_prop)
tprop.SetVerticalJustificationToBottom()
tprop.SetColor(1, 0, 0)
single_line_text_actor_b = vtkActor2D()
single_line_text_actor_b.SetMapper(single_line_text_b)
single_line_text_actor_b.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_b.GetPositionCoordinate().SetValue(0.05, 0.85)

# The text is on a single line and center-justified (vertical).
single_line_text_c = vtkTextMapper()
single_line_text_c.SetInput("Single line (centered)")
tprop = single_line_text_c.GetTextProperty()
tprop.ShallowCopy(single_line_text_prop)
tprop.SetVerticalJustificationToCentered()
tprop.SetColor(0, 1, 0)
single_line_text_actor_c = vtkActor2D()
single_line_text_actor_c.SetMapper(single_line_text_c)
single_line_text_actor_c.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_c.GetPositionCoordinate().SetValue(0.05, 0.75)

# The text is on a single line and top-justified.
single_line_text_t = vtkTextMapper()
single_line_text_t.SetInput("Single line (top)")
tprop = single_line_text_t.GetTextProperty()
tprop.ShallowCopy(single_line_text_prop)
tprop.SetVerticalJustificationToTop()
tprop.SetColor(0, 0, 1)
single_line_text_actor_t = vtkActor2D()
single_line_text_actor_t.SetMapper(single_line_text_t)
single_line_text_actor_t.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
single_line_text_actor_t.GetPositionCoordinate().SetValue(0.05, 0.65)

# The text is on multiple lines and left- and top-justified.
text_mapper_l = vtkTextMapper()
text_mapper_l.SetInput("This is\nmulti-line\ntext output\n(left-top)")
tprop = text_mapper_l.GetTextProperty()
tprop.ShallowCopy(multi_line_text_prop)
tprop.SetJustificationToLeft()
tprop.SetVerticalJustificationToTop()
tprop.SetColor(1, 0, 0)
text_actor_l = vtkActor2D()
text_actor_l.SetMapper(text_mapper_l)
text_actor_l.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_l.GetPositionCoordinate().SetValue(0.05, 0.5)

# The text is on multiple lines and center-justified (both horizontal
# and vertical).
text_mapper_c = vtkTextMapper()
text_mapper_c.SetInput("This is\nmulti-line\ntext output\n(centered)")
tprop = text_mapper_c.GetTextProperty()
tprop.ShallowCopy(multi_line_text_prop)
tprop.SetJustificationToCentered()
tprop.SetVerticalJustificationToCentered()
tprop.SetColor(0, 1, 0)
text_actor_c = vtkActor2D()
text_actor_c.SetMapper(text_mapper_c)
text_actor_c.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_c.GetPositionCoordinate().SetValue(0.5, 0.5)

# The text is on multiple lines and right- and bottom-justified.
text_mapper_r = vtkTextMapper()
text_mapper_r.SetInput("This is\nmulti-line\ntext output\n(right-bottom)")
tprop = text_mapper_r.GetTextProperty()
tprop.ShallowCopy(multi_line_text_prop)
tprop.SetJustificationToRight()
tprop.SetVerticalJustificationToBottom()
tprop.SetColor(0, 0, 1)
text_actor_r = vtkActor2D()
text_actor_r.SetMapper(text_mapper_r)
text_actor_r.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text_actor_r.GetPositionCoordinate().SetValue(0.95, 0.5)

# Draw the grid to demonstrate the placement of the text.
pts = vtkPoints()
pts.InsertNextPoint(0.05, 0.0, 0.0)
pts.InsertNextPoint(0.05, 1.0, 0.0)
pts.InsertNextPoint(0.5, 0.0, 0.0)
pts.InsertNextPoint(0.5, 1.0, 0.0)
pts.InsertNextPoint(0.95, 0.0, 0.0)
pts.InsertNextPoint(0.95, 1.0, 0.0)
pts.InsertNextPoint(0.0, 0.5, 0.0)
pts.InsertNextPoint(1.0, 0.5, 0.0)
pts.InsertNextPoint(0.00, 0.85, 0.0)
pts.InsertNextPoint(0.50, 0.85, 0.0)
pts.InsertNextPoint(0.00, 0.75, 0.0)
pts.InsertNextPoint(0.50, 0.75, 0.0)
pts.InsertNextPoint(0.00, 0.65, 0.0)
pts.InsertNextPoint(0.50, 0.65, 0.0)

lines = vtkCellArray()
for i in range(0, 14, 2):
    lines.InsertNextCell(2)
    lines.InsertCellPoint(i)
    lines.InsertCellPoint(i + 1)

grid = vtkPolyData()
grid.SetPoints(pts)
grid.SetLines(lines)

norm_coords = vtkCoordinate()
norm_coords.SetCoordinateSystemToNormalizedViewport()

grid_mapper = vtkPolyDataMapper2D()
grid_mapper.SetInputData(grid)
grid_mapper.SetTransformCoordinate(norm_coords)
grid_actor = vtkActor2D()
grid_actor.SetMapper(grid_mapper)
grid_actor.GetProperty().SetColor(0.1, 0.1, 0.1)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer
renderer.AddViewProp(text_actor_l)
renderer.AddViewProp(text_actor_c)
renderer.AddViewProp(text_actor_r)
renderer.AddViewProp(single_line_text_actor_b)
renderer.AddViewProp(single_line_text_actor_c)
renderer.AddViewProp(single_line_text_actor_t)
renderer.AddViewProp(grid_actor)

renderer.SetBackground(1, 1, 1)
render_window.SetSize(500, 300)
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
render_window.Render()
interactor.Start()
