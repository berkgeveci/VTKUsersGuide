#!/usr/bin/env python3
"""Breadth-first search on a random graph using Boost algorithms.

Creates a random graph, performs BFS from vertex 0, and displays the
result with vertices colored and labeled by BFS distance.

Requires VTK built with Boost Graph Library support.
"""

from vtkmodules.vtkInfovisBoostGraphAlgorithms import (
    vtkBoostBreadthFirstSearch,
)
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView
from vtkmodules.vtkViewsCore import vtkViewTheme
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a random graph with edge weights
source = vtkRandomGraphSource()
source.SetIncludeEdgeWeights(True)

# Perform breadth-first search from vertex 0
bfs = vtkBoostBreadthFirstSearch()
bfs.AddInputConnection(source.GetOutputPort())
bfs.SetOriginVertex(0)

# Create a graph layout view
view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(bfs.GetOutputPort())
view.SetVertexLabelArrayName("BFS")
view.SetVertexLabelVisibility(True)
view.SetVertexColorArrayName("BFS")
view.SetColorVertices(True)
view.SetEdgeLabelArrayName("edge weight")
view.SetEdgeLabelVisibility(True)
view.SetEdgeColorArrayName("edge weight")
view.SetColorEdges(True)
view.SetLayoutStrategyToSimple2D()

# Apply a theme
theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(5)
theme.SetPointSize(10)
view.ApplyViewTheme(theme)
view.SetVertexLabelFontSize(20)
view.SetEdgeLabelFontSize(12)

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
