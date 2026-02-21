#!/usr/bin/env python3
"""Create a tree programmatically and visualize it.

Demonstrates building a vtkTree from a vtkMutableDirectedGraph, adding
vertex labels, and displaying it with a themed graph layout view.
"""

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView
from vtkmodules.vtkViewsCore import vtkViewTheme
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Build a tree using a mutable directed graph
graph = vtkMutableDirectedGraph()
a = graph.AddVertex()
b = graph.AddChild(a)
c = graph.AddChild(a)
d = graph.AddChild(b)
e = graph.AddChild(c)
f = graph.AddChild(c)

# Add labels to vertices
labels = vtkStringArray()
labels.SetName("Label")
labels.InsertValue(a, "a")
labels.InsertValue(b, "b")
labels.InsertValue(c, "c")
labels.InsertValue(d, "d")
labels.InsertValue(e, "e")
labels.InsertValue(f, "f")
graph.GetVertexData().AddArray(labels)

# Convert the graph to a tree
tree = vtkTree()
if not tree.CheckedShallowCopy(graph):
    print("Invalid tree")
    raise SystemExit(1)

# Create a themed graph layout view
view = vtkGraphLayoutView()
view.SetRepresentationFromInput(tree)

theme = vtkViewTheme.CreateMellowTheme()
view.ApplyViewTheme(theme)

view.SetVertexColorArrayName("VertexDegree")
view.SetColorVertices(True)
view.SetVertexLabelArrayName("Label")
view.SetVertexLabelVisibility(True)

view.GetRenderWindow().SetSize(800, 800)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()
