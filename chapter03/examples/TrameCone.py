"""Minimal trame application: interactive VTK cone in the browser."""

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk as vtk_widgets, vuetify3 as vuetify

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# --- VTK pipeline ---
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

cone = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()

# --- Trame application ---
server = get_server(client_type="vue3")

with SinglePageLayout(server) as layout:
    layout.title.set_text("VTK Cone")
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            vtk_widgets.VtkLocalView(render_window)

if __name__ == "__main__":
    server.start()
