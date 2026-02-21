#!/usr/bin/env python3
"""Compute and visualize a minimum spanning tree on a random graph.

Computes betweenness centrality, then finds the minimum (or maximum)
spanning tree using Kruskal's algorithm. The MST edges are highlighted
in the graph view.

Requires VTK built with Boost Graph Library support.
"""

from vtkmodules.vtkInfovisBoostGraphAlgorithms import (
    vtkBoostBrandesCentrality,
    vtkBoostKruskalMinimumSpanningTree,
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

# Compute betweenness centrality
centrality = vtkBoostBrandesCentrality()
centrality.SetInputConnection(source.GetOutputPort())

# Find the maximal spanning tree (negate weights to get maximum)
mst_selection = vtkBoostKruskalMinimumSpanningTree()
mst_selection.SetInputConnection(centrality.GetOutputPort())
mst_selection.SetEdgeWeightArrayName("centrality")
mst_selection.NegateEdgeWeightsOn()
mst_selection.Update()

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

# Use pedigree id selection and set MST as the selection
view.SetSelectionType(2)
view.GetRepresentation(0).GetAnnotationLink().SetCurrentSelection(
    mst_selection.GetOutput()
)

# Apply a theme with highlighted selection
theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(5)
theme.SetCellOpacity(0.99)
theme.SetPointSize(10)
theme.SetSelectedCellColor(1, 0, 1)
theme.SetSelectedPointColor(1, 0, 1)
view.ApplyViewTheme(theme)
view.SetVertexLabelFontSize(14)

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
