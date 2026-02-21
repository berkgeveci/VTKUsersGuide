#!/usr/bin/env python
"""Extract portions of an unstructured grid (Section 5.5)."""
import os
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkConnectivityFilter, vtkPolyDataNormals
from vtkmodules.vtkFiltersExtraction import vtkExtractUnstructuredGrid
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Read unstructured grid data.
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
reader.SetScalarsName("thickness9")
reader.SetVectorsName("displacement9")
reader.Update()

# Warp by displacement.
warp = vtkWarpVector()
warp.SetInputConnection(reader.GetOutputPort())

# Extract the mold (regions 0 and 1).
connect = vtkConnectivityFilter()
connect.SetInputConnection(warp.GetOutputPort())
connect.SetExtractionModeToSpecifiedRegions()
connect.AddSpecifiedRegion(0)
connect.AddSpecifiedRegion(1)

mold_mapper = vtkDataSetMapper()
mold_mapper.SetInputConnection(reader.GetOutputPort())
mold_mapper.ScalarVisibilityOff()

mold_actor = vtkActor()
mold_actor.SetMapper(mold_mapper)
mold_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
mold_actor.GetProperty().SetRepresentationToWireframe()

# Extract the parison (region 2).
connect2 = vtkConnectivityFilter()
connect2.SetInputConnection(warp.GetOutputPort())
connect2.SetExtractionModeToSpecifiedRegions()
connect2.AddSpecifiedRegion(2)

# Extract a subset of cells.
extract_grid = vtkExtractUnstructuredGrid()
extract_grid.SetInputConnection(connect2.GetOutputPort())
extract_grid.CellClippingOn()
extract_grid.SetCellMinimum(0)
extract_grid.SetCellMaximum(23)

parison = vtkGeometryFilter()
parison.SetInputConnection(extract_grid.GetOutputPort())

normals2 = vtkPolyDataNormals()
normals2.SetInputConnection(parison.GetOutputPort())
normals2.SetFeatureAngle(60)

lut = vtkLookupTable()
lut.SetHueRange(0.0, 0.66667)

parison_mapper = vtkPolyDataMapper()
parison_mapper.SetInputConnection(normals2.GetOutputPort())
parison_mapper.SetLookupTable(lut)
parison_mapper.SetScalarRange(0.12, 1.0)

parison_actor = vtkActor()
parison_actor.SetMapper(parison_mapper)

# Rendering.
ren = vtkRenderer()
ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(1000, 800)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

ren.AddActor(parison_actor)
ren.AddActor(mold_actor)
ren.SetBackground(1, 1, 1)

ren.ResetCamera()
ren.GetActiveCamera().Azimuth(60)
ren.GetActiveCamera().Roll(-90)
ren.GetActiveCamera().Dolly(2)
ren.ResetCameraClippingRange()

iren.Initialize()
ren_win.Render()
iren.Start()
