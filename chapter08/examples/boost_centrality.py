#!/usr/bin/env python3
"""Compute and visualize betweenness centrality on a random graph.

Uses Brandes' algorithm via vtkBoostBrandesCentrality to compute
betweenness centrality for vertices and edges, then visualizes the
result with color indicating centrality values.

Requires VTK built with Boost Graph Library support.
"""

from vtkmodules.vtkInfovisBoostGraphAlgorithms import (
    vtkBoostBrandesCentrality,
)
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView
from vtkmodules.vtkViewsCore import vtkViewTheme
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create a random undirected graph
source = vtkRandomGraphSource()
source.DirectedOff()
source.SetNumberOfVertices(50)
source.SetEdgeProbability(0.01)
source.SetUseEdgeProbability(True)
source.AllowParallelEdgesOn()
source.AllowSelfLoopsOn()
source.SetStartWithTree(True)

# Compute betweenness centrality using Brandes' algorithm
centrality = vtkBoostBrandesCentrality()
centrality.SetInputConnection(source.GetOutputPort())

# Create a graph layout view
view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(centrality.GetOutputPort())
view.SetVertexLabelArrayName("centrality")
view.SetVertexLabelVisibility(True)
view.SetVertexColorArrayName("centrality")
view.SetColorVertices(True)
view.SetEdgeColorArrayName("centrality")
view.SetColorEdges(True)
view.SetLayoutStrategyToSimple2D()

# Apply a theme
theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(5)
theme.SetPointSize(10)
theme.SetCellOpacity(1)
view.ApplyViewTheme(theme)

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
