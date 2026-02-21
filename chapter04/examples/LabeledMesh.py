#!/usr/bin/env python3
#
# This example demonstrates the use of vtkLabeledDataMapper. This
# class is used for displaying numerical data from an underlying data
# set. In the case of this example, the underlying data are the point
# and cell ids.
#

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkCellCenters, vtkGenerateIds
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkPolyDataMapper2D,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkSelectVisiblePoints,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401

# Create a selection window. We will display the point and cell ids
# that lie within this window.
xmin = 200
x_length = 100
xmax = xmin + x_length
ymin = 200
y_length = 100
ymax = ymin + y_length

pts = vtkPoints()
pts.InsertPoint(0, xmin, ymin, 0)
pts.InsertPoint(1, xmax, ymin, 0)
pts.InsertPoint(2, xmax, ymax, 0)
pts.InsertPoint(3, xmin, ymax, 0)
rect = vtkCellArray()
rect.InsertNextCell(5)
rect.InsertCellPoint(0)
rect.InsertCellPoint(1)
rect.InsertCellPoint(2)
rect.InsertCellPoint(3)
rect.InsertCellPoint(0)
select_rect = vtkPolyData()
select_rect.SetPoints(pts)
select_rect.SetLines(rect)
rect_mapper = vtkPolyDataMapper2D()
rect_mapper.SetInputData(select_rect)
rect_actor = vtkActor2D()
rect_actor.SetMapper(rect_mapper)

# Create a sphere and its associated mapper and actor.
sphere = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Generate data arrays containing point and cell ids
ids = vtkGenerateIds()
ids.SetInputConnection(sphere.GetOutputPort())
ids.PointIdsOn()
ids.CellIdsOn()
ids.FieldDataOn()

# Create the renderer here because vtkSelectVisiblePoints needs it.
renderer = vtkRenderer()

# Create labels for points
vis_pts = vtkSelectVisiblePoints()
vis_pts.SetInputConnection(ids.GetOutputPort())
vis_pts.SetRenderer(renderer)
vis_pts.SelectionWindowOn()
vis_pts.SetSelection(xmin, xmin + x_length, ymin, ymin + y_length)

# Create the mapper to display the point ids. Specify the format to
# use for the labels. Also create the associated actor.
ldm = vtkLabeledDataMapper()
ldm.SetInputConnection(vis_pts.GetOutputPort())
ldm.SetLabelFormat("{}")
ldm.SetLabelModeToLabelFieldData()
point_labels = vtkActor2D()
point_labels.SetMapper(ldm)

# Create labels for cells
cc = vtkCellCenters()
cc.SetInputConnection(ids.GetOutputPort())
vis_cells = vtkSelectVisiblePoints()
vis_cells.SetInputConnection(cc.GetOutputPort())
vis_cells.SetRenderer(renderer)
vis_cells.SelectionWindowOn()
vis_cells.SetSelection(xmin, xmin + x_length, ymin, ymin + y_length)

# Create the mapper to display the cell ids. Specify the format to
# use for the labels. Also create the associated actor.
cell_mapper = vtkLabeledDataMapper()
cell_mapper.SetInputConnection(vis_cells.GetOutputPort())
cell_mapper.SetLabelFormat("{}")
cell_mapper.SetLabelModeToLabelFieldData()
cell_mapper.GetLabelTextProperty().SetColor(0, 1, 0)
cell_labels = vtkActor2D()
cell_labels.SetMapper(cell_mapper)

# Create the RenderWindow and RenderWindowInteractor
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actors to the renderer; set the background and size
renderer.AddActor(sphere_actor)
renderer.AddViewProp(rect_actor)
renderer.AddViewProp(point_labels)
renderer.AddViewProp(cell_labels)

renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)


# Create a function to draw the selection window at each location it
# is moved to.
def place_window(new_xmin, new_ymin):
    new_xmax = new_xmin + x_length
    new_ymax = new_ymin + y_length

    vis_pts.SetSelection(new_xmin, new_xmax, new_ymin, new_ymax)
    vis_cells.SetSelection(new_xmin, new_xmax, new_ymin, new_ymax)

    pts.InsertPoint(0, new_xmin, new_ymin, 0)
    pts.InsertPoint(1, new_xmax, new_ymin, 0)
    pts.InsertPoint(2, new_xmax, new_ymax, 0)
    pts.InsertPoint(3, new_xmin, new_ymax, 0)
    # Call Modified because InsertPoint does not modify vtkPoints
    # (for performance reasons)
    pts.Modified()
    render_window.Render()


# Initialize the interactor.
interactor.Initialize()
render_window.Render()

# Move the selection window across the data set.
for y in range(100, 300, 25):
    for x in range(100, 300, 25):
        place_window(x, y)

# Put the selection window in the center of the render window.
place_window(xmin, ymin)

# Now start normal interaction.
interactor.Start()
