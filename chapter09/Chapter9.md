# Chapter 9: Geospatial Visualization

VTK provides support for geospatial visualization through cartographic projections and coordinate transforms. The vtkGeoProjection class wraps the PROJ library, giving access to over 180 cartographic projections. The vtkGeoTransform class transforms points between any two projections, and because it inherits from vtkAbstractTransform, it integrates directly with VTK's transform filters.

## 9.1 Cartographic Projections

The vtkGeoProjection class represents a cartographic projection from a sphere to a plane. VTK includes over 180 projections from the PROJ library, a few of which are shown in Figure 9–5.

![Figure 9-5](images/Figure_9-5.png)

*Figure 9–5 Some interesting cartographic projections provided by the PROJ library.*

By default, new vtkGeoProjection instances are set to the natural cartographic transform named "latlong" (no projection at all). To use a specific projection, call `SetName()` with a PROJ projection identifier such as "robin" (Robinson), "moll" (Mollweide), "wintri" (Winkel Tripel), or "eck1" (Eckert I). You can also specify a full PROJ4 parameter string with `SetPROJ4String()`. Some projections accept additional parameters such as `SetCentralMeridian()`.

Note that many projections are not intended for use over the entire globe, but rather over a small lat-long region. If you attempt to use these projections on a domain that is too large, the results will often be confusing and incoherent.

```python
from vtkmodules.vtkGeovisCore import vtkGeoProjection

# List all available projections
num = vtkGeoProjection.GetNumberOfProjections()
for i in range(num):
    name = vtkGeoProjection.GetProjectionName(i)
    desc = vtkGeoProjection.GetProjectionDescription(i)
    print(f"  {name:12s}  {desc}")

# Create a specific projection
proj = vtkGeoProjection()
proj.SetName("robin")
print(proj.GetDescription())
```

## 9.2 Coordinate Transforms

The vtkGeoTransform class moves points from one projection to another by applying the inverse of the source projection followed by the forward projection of the destination. Because vtkGeoTransform inherits from vtkAbstractTransform, it can be used with vtkTransformFilter or vtkTransformPolyDataFilter to transform any VTK dataset between coordinate systems.

The following example creates a graticule (grid of constant-latitude and constant-longitude lines) in lat-long coordinates, then projects it through a Mollweide projection using vtkGeoTransform and vtkTransformPolyDataFilter. The result is shown in Figure 9–6.

![Figure 9-6](images/Figure_9-6.png)

*Figure 9–6 A grid of equal latitude/longitude lines sent through a 2D projection.*

```python
import math

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkGeovisCore import vtkGeoProjection, vtkGeoTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Build a graticule in lat-long coordinates (radians)
points = vtkPoints()
lines = vtkCellArray()
for lat in range(-90, 91, 15):
    lat_rad = math.radians(max(-89.9, min(89.9, lat)))
    ids = []
    for i in range(101):
        lon_rad = math.radians(-180 + i * 3.6)
        ids.append(points.InsertNextPoint(lon_rad, lat_rad, 0.0))
    lines.InsertNextCell(len(ids), ids)
for lon in range(-180, 181, 15):
    lon_rad = math.radians(lon)
    ids = []
    for i in range(101):
        lat_rad = math.radians(-89.9 + i * 1.798)
        ids.append(points.InsertNextPoint(lon_rad, lat_rad, 0.0))
    lines.InsertNextCell(len(ids), ids)

graticule = vtkPolyData()
graticule.SetPoints(points)
graticule.SetLines(lines)

# Set up projections
source_proj = vtkGeoProjection()
source_proj.SetPROJ4String("+proj=latlong")

dest_proj = vtkGeoProjection()
dest_proj.SetPROJ4String("+proj=moll +R=1")

# Transform the graticule
transform = vtkGeoTransform()
transform.SetSourceProjection(source_proj)
transform.SetDestinationProjection(dest_proj)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputData(graticule)
transform_filter.SetTransform(transform)

# Visualize
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(transform_filter.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.4, 0.8)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 600)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
renderer.ResetCamera()
render_window.Render()
interactor.Start()
```
