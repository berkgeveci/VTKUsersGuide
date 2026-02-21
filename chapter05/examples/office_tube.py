#!/usr/bin/env python
"""Single streamtube in office airflow data (Figure 5-4)."""
import os
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import (
    vtkStructuredGridGeometryFilter,
)
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read structured grid CFD data.
reader = vtkStructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "office.binary.vtk"))
reader.Update()

# Create a single streamtube using vtkStreamTracer.
streamer = vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(0.1, 2.1, 0.5)
streamer.SetMaximumPropagation(500)
streamer.SetInitialIntegrationStep(0.05)
streamer.SetIntegrationStepUnit(streamer.CELL_LENGTH_UNIT)
streamer.SetIntegrationDirectionToBoth()
streamer.SetIntegratorTypeToRungeKutta4()

# Wrap the streamline with a tube.
stream_tube = vtkTubeFilter()
stream_tube.SetInputConnection(streamer.GetOutputPort())
stream_tube.SetInputArrayToProcess(
    1, 0, 0, 0, "vectors"  # FIELD_ASSOCIATION_POINTS = 0
)
stream_tube.SetRadius(0.02)
stream_tube.SetNumberOfSides(12)
stream_tube.SetVaryRadiusToVaryRadiusByVector()

map_stream_tube = vtkPolyDataMapper()
map_stream_tube.SetInputConnection(stream_tube.GetOutputPort())
map_stream_tube.SetScalarRange(
    reader.GetOutput().GetPointData().GetScalars().GetRange()
)

stream_tube_actor = vtkActor()
stream_tube_actor.SetMapper(map_stream_tube)
stream_tube_actor.GetProperty().BackfaceCullingOn()

# Office geometry — tables, shelves, etc.
def make_geometry(rdr, extent, color):
    filt = vtkStructuredGridGeometryFilter()
    filt.SetInputConnection(rdr.GetOutputPort())
    filt.SetExtent(*extent)
    m = vtkPolyDataMapper()
    m.SetInputConnection(filt.GetOutputPort())
    m.ScalarVisibilityOff()
    a = vtkActor()
    a.SetMapper(m)
    a.GetProperty().SetColor(*color)
    return a

furniture_color = (0.59, 0.427, 0.392)
shelf_color = (0.8, 0.8, 0.6)

actors = [
    make_geometry(reader, (11, 15, 7, 9, 8, 8), furniture_color),
    make_geometry(reader, (11, 15, 10, 12, 8, 8), furniture_color),
    make_geometry(reader, (15, 15, 7, 9, 0, 8), shelf_color),
    make_geometry(reader, (15, 15, 10, 12, 0, 8), shelf_color),
    make_geometry(reader, (13, 13, 0, 4, 0, 11), shelf_color),
    make_geometry(reader, (20, 20, 0, 4, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 0, 0, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 4, 4, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 0, 4, 0, 0), shelf_color),
    make_geometry(reader, (13, 20, 0, 4, 11, 11), shelf_color),
    make_geometry(reader, (13, 13, 15, 19, 0, 11), shelf_color),
    make_geometry(reader, (20, 20, 15, 19, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 15, 15, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 19, 19, 0, 11), shelf_color),
    make_geometry(reader, (13, 20, 15, 19, 0, 0), shelf_color),
    make_geometry(reader, (13, 20, 15, 19, 11, 11), shelf_color),
    make_geometry(reader, (20, 20, 6, 13, 10, 13), (0.3, 0.3, 0.5)),
    make_geometry(reader, (0, 0, 9, 10, 14, 16), (0, 0, 0)),
    make_geometry(reader, (0, 0, 9, 10, 0, 6), (0, 0, 0)),
]

# Outline.
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter

outline = vtkStructuredGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
map_outline = vtkPolyDataMapper()
map_outline.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(map_outline)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

for a in actors:
    ren.AddActor(a)
ren.AddActor(outline_actor)
ren.AddActor(stream_tube_actor)
ren.SetBackground(0.4, 0.4, 0.5)

camera = vtkCamera()
camera.SetClippingRange(0.726079, 36.3039)
camera.SetFocalPoint(2.43584, 2.15046, 1.11104)
camera.SetPosition(-4.76183, -10.4426, 3.17203)
camera.SetViewUp(0.0511273, 0.132773, 0.989827)
camera.SetViewAngle(18.604)
camera.Zoom(1.2)
ren.SetActiveCamera(camera)

ren_win.SetSize(500, 300)

iren.Initialize()
ren_win.Render()
iren.Start()
