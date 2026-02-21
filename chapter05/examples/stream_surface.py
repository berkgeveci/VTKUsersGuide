#!/usr/bin/env python
"""Stream surface from combustor data (Figure 5-5)."""
import os
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read PLOT3D combustor data.
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

block = pl3d.GetOutput().GetBlock(0)

# Rake of seed points for streamlines.
rake = vtkLineSource()
rake.SetPoint1(15, -5, 32)
rake.SetPoint2(15, 5, 32)
rake.SetResolution(21)

rake_mapper = vtkPolyDataMapper()
rake_mapper.SetInputConnection(rake.GetOutputPort())
rake_actor = vtkActor()
rake_actor.SetMapper(rake_mapper)

# Generate streamlines.
sl = vtkStreamTracer()
sl.SetInputData(block)
sl.SetSourceConnection(rake.GetOutputPort())
sl.SetIntegratorTypeToRungeKutta4()
sl.SetMaximumPropagation(100)
sl.SetInitialIntegrationStep(0.1)
sl.SetIntegrationStepUnit(sl.CELL_LENGTH_UNIT)
sl.SetIntegrationDirectionToBackward()

# Create a ruled surface from the streamlines.
scalar_surface = vtkRuledSurfaceFilter()
scalar_surface.SetInputConnection(sl.GetOutputPort())
scalar_surface.SetOffset(0)
scalar_surface.SetOnRatio(2)
scalar_surface.PassLinesOn()
scalar_surface.SetRuledModeToPointWalk()
scalar_surface.SetDistanceFactor(30)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(scalar_surface.GetOutputPort())
mapper.SetScalarRange(block.GetScalarRange())

actor = vtkActor()
actor.SetMapper(mapper)

# Outline for context.
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(block)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(800, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(rake_actor)
ren.AddActor(actor)
ren.AddActor(outline_actor)
ren.SetBackground(1, 1, 1)

iren.Initialize()
ren_win.Render()
iren.Start()
