#!/usr/bin/env python3
#
# This example demonstrates the use of vtkXYPlotActor to display three
# probe lines using three different techniques. We are loading data
# using vtkMultiBlockPLOT3DReader and using vtkProbeFilter to extract
# the underlying point data along three probe lines.
#

import os

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkProbeFilter, vtkStructuredGridOutlineFilter, vtkTubeFilter, vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingAnnotation import vtkXYPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Ensure an OpenGL rendering backend is loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401

# Create a PLOT3D reader and load the data.
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

# vtkMultiBlockPLOT3DReader returns a vtkMultiBlockDataSet.
# Get the first block.
output = pl3d.GetOutput().GetBlock(0)

# Create a line source to use for the probe lines.
line = vtkLineSource()
line.SetResolution(30)

# Move the line into place and create the probe filter. For
# vtkProbeFilter, the probe line is the input, and the underlying data
# set is the source.
trans_l1 = vtkTransform()
trans_l1.Translate(3.7, 0.0, 28.37)
trans_l1.Scale(5, 5, 5)
trans_l1.RotateY(90)
tf = vtkTransformPolyDataFilter()
tf.SetInputConnection(line.GetOutputPort())
tf.SetTransform(trans_l1)
probe = vtkProbeFilter()
probe.SetInputConnection(tf.GetOutputPort())
probe.SetSourceData(output)

# Move the line again and create another probe filter.
trans_l2 = vtkTransform()
trans_l2.Translate(9.2, 0.0, 31.20)
trans_l2.Scale(5, 5, 5)
trans_l2.RotateY(90)
tf2 = vtkTransformPolyDataFilter()
tf2.SetInputConnection(line.GetOutputPort())
tf2.SetTransform(trans_l2)
probe2 = vtkProbeFilter()
probe2.SetInputConnection(tf2.GetOutputPort())
probe2.SetSourceData(output)

# Move the line again and create a third probe filter.
trans_l3 = vtkTransform()
trans_l3.Translate(13.27, 0.0, 33.40)
trans_l3.Scale(4.5, 4.5, 4.5)
trans_l3.RotateY(90)
tf3 = vtkTransformPolyDataFilter()
tf3.SetInputConnection(line.GetOutputPort())
tf3.SetTransform(trans_l3)
probe3 = vtkProbeFilter()
probe3.SetInputConnection(tf3.GetOutputPort())
probe3.SetSourceData(output)

# Create a vtkAppendPolyData to merge the output of the three probe
# filters into one data set.
append_f = vtkAppendPolyData()
append_f.AddInputConnection(probe.GetOutputPort())
append_f.AddInputConnection(probe2.GetOutputPort())
append_f.AddInputConnection(probe3.GetOutputPort())

# Create a tube filter to represent the lines as tubes. Set up the
# associated mapper and actor.
tuber = vtkTubeFilter()
tuber.SetInputConnection(append_f.GetOutputPort())
tuber.SetRadius(0.1)
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(tuber.GetOutputPort())
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)

# Create an xy-plot using the output of the 3 probe filters as input.
# The x-values we are plotting are arc length.
xyplot = vtkXYPlotActor()
xyplot.AddDataSetInputConnection(probe.GetOutputPort())
xyplot.AddDataSetInputConnection(probe2.GetOutputPort())
xyplot.AddDataSetInputConnection(probe3.GetOutputPort())
xyplot.GetPositionCoordinate().SetValue(0.0, 0.67, 0)
xyplot.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot.SetXValuesToArcLength()
xyplot.SetNumberOfXLabels(6)
xyplot.SetTitle("Pressure vs. Arc Length (Zoomed View)")
xyplot.SetXTitle("")
xyplot.SetYTitle("P")
xyplot.SetXRange(0.1, 0.35)
xyplot.SetYRange(0.2, 0.4)
xyplot.GetProperty().SetColor(0, 0, 0)
xyplot.GetProperty().SetLineWidth(2)
# Set text prop color
tprop = xyplot.GetTitleTextProperty()
tprop.SetColor(xyplot.GetProperty().GetColor())
xyplot.SetAxisTitleTextProperty(tprop)
xyplot.SetAxisLabelTextProperty(tprop)

# Create an xy-plot using normalized arc length.
xyplot2 = vtkXYPlotActor()
xyplot2.AddDataSetInputConnection(probe.GetOutputPort())
xyplot2.AddDataSetInputConnection(probe2.GetOutputPort())
xyplot2.AddDataSetInputConnection(probe3.GetOutputPort())
xyplot2.GetPositionCoordinate().SetValue(0.00, 0.33, 0)
xyplot2.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot2.SetXValuesToNormalizedArcLength()
xyplot2.SetNumberOfXLabels(6)
xyplot2.SetTitle("Pressure vs. Normalized Arc Length")
xyplot2.SetXTitle("")
xyplot2.SetYTitle("P")
xyplot2.PlotPointsOn()
xyplot2.PlotLinesOff()
xyplot2.GetProperty().SetColor(1, 0, 0)
xyplot2.GetProperty().SetPointSize(2)
tprop = xyplot2.GetTitleTextProperty()
tprop.SetColor(xyplot2.GetProperty().GetColor())
xyplot2.SetAxisTitleTextProperty(tprop)
xyplot2.SetAxisLabelTextProperty(tprop)

# Create an xy-plot using point index for x values.
xyplot3 = vtkXYPlotActor()
xyplot3.AddDataSetInputConnection(probe.GetOutputPort())
xyplot3.AddDataSetInputConnection(probe2.GetOutputPort())
xyplot3.AddDataSetInputConnection(probe3.GetOutputPort())
xyplot3.GetPositionCoordinate().SetValue(0.0, 0.0, 0)
xyplot3.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot3.SetXValuesToIndex()
xyplot3.SetNumberOfXLabels(6)
xyplot3.SetTitle("Pressure vs. Point Id")
xyplot3.SetXTitle("Probe Length")
xyplot3.SetYTitle("P")
xyplot3.PlotPointsOn()
xyplot3.GetProperty().SetColor(0, 0, 1)
xyplot3.GetProperty().SetPointSize(3)
tprop = xyplot3.GetTitleTextProperty()
tprop.SetColor(xyplot3.GetProperty().GetColor())
xyplot3.SetAxisTitleTextProperty(tprop)
xyplot3.SetAxisLabelTextProperty(tprop)

# Draw an outline of the PLOT3D data set.
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Create the Renderers, RenderWindow, and RenderWindowInteractor.
renderer = vtkRenderer()
renderer2 = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.AddRenderer(renderer2)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Set the background and viewport of the first renderer (3D view).
renderer.SetBackground(0.6784, 0.8471, 0.9020)
renderer.SetViewport(0, 0, 0.5, 1)
renderer.AddActor(outline_actor)
renderer.AddActor(line_actor)

# Set the background and viewport of the second renderer (plots).
renderer2.SetBackground(1, 1, 1)
renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer2.AddViewProp(xyplot)
renderer2.AddViewProp(xyplot2)
renderer2.AddViewProp(xyplot3)
render_window.SetSize(1200, 800)

# Set up the camera parameters.
cam1 = renderer.GetActiveCamera()
cam1.SetClippingRange(3.95297, 100)
cam1.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam1.SetPosition(-12.3332, 31.7479, 41.2387)
cam1.SetViewUp(0.060772, -0.319905, 0.945498)

interactor.Initialize()
render_window.Render()
interactor.Start()
