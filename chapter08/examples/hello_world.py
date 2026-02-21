#!/usr/bin/env python3
"""Simple graph visualization with vtkGraphLayoutView.

Creates a random graph and displays it using a force-directed layout.
This is the most basic information visualization example in VTK.
"""

from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a random graph
source = vtkRandomGraphSource()

# Create a view to display the graph
view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(source.GetOutputPort())

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
