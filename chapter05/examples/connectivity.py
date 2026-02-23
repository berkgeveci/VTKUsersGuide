"""Extract and color connected regions of a dataset."""
import sys

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkConnectivityFilter, vtkThreshold
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

# Create a 3D scalar field and threshold to get disconnected pieces.
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(50, 50, 50)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

# Threshold to create multiple disconnected regions.
thresh = vtkThreshold()
thresh.SetInputConnection(sample.GetOutputPort())
thresh.SetThresholdFunction(thresh.THRESHOLD_BETWEEN)
thresh.SetLowerThreshold(0.8)
thresh.SetUpperThreshold(1.5)

# Extract all connected regions and color by region ID.
conn = vtkConnectivityFilter()
conn.SetInputConnection(thresh.GetOutputPort())
conn.SetExtractionModeToAllRegions()
conn.ColorRegionsOn()

surface = vtkGeometryFilter()
surface.SetInputConnection(conn.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RegionId")
mapper.SetScalarRange(0, conn.GetNumberOfExtractedRegions())
mapper.Update()
mapper.SetScalarRange(mapper.GetInput().GetPointData().GetArray("RegionId").GetRange())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
if "--non-interactive" not in sys.argv:
    interactor.Start()
