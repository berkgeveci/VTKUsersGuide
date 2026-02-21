#!/usr/bin/env python3
"""Graph visualization colored by vertex degree.

Creates a random graph, computes vertex degree using vtkVertexDegree,
and displays the result with vertices colored and labeled by degree.
"""

from vtkmodules.vtkInfovisCore import (
    vtkRandomGraphSource,
    vtkVertexDegree,
)
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView
from vtkmodules.vtkViewsCore import vtkViewTheme
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a random graph with edge weights
source = vtkRandomGraphSource()
source.SetIncludeEdgeWeights(True)

# Compute vertex degree
degree = vtkVertexDegree()
degree.AddInputConnection(source.GetOutputPort())

# Create a graph layout view
view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(degree.GetOutputPort())
view.SetVertexLabelArrayName("VertexDegree")
view.SetVertexLabelVisibility(True)
view.SetVertexColorArrayName("VertexDegree")
view.SetColorVertices(True)
view.SetEdgeLabelArrayName("edge weight")
view.SetEdgeLabelVisibility(True)
view.SetEdgeColorArrayName("edge weight")
view.SetColorEdges(True)
view.SetLayoutStrategyToSimple2D()

# Apply a theme
theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(4)
view.ApplyViewTheme(theme)

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
