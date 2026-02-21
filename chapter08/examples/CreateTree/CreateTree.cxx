// Create a tree programmatically and visualize it.
//
// Demonstrates building a vtkTree from a vtkMutableDirectedGraph,
// adding vertex labels, and displaying with a themed graph layout view.

#include <vtkDataSetAttributes.h>
#include <vtkGraphLayoutView.h>
#include <vtkMutableDirectedGraph.h>
#include <vtkNew.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkStringArray.h>
#include <vtkTree.h>
#include <vtkViewTheme.h>

#include <iostream>

int main(int, char*[])
{
    // Build a tree using a mutable directed graph
    vtkNew<vtkMutableDirectedGraph> graph;
    vtkIdType a = graph->AddVertex();
    vtkIdType b = graph->AddChild(a);
    vtkIdType c = graph->AddChild(a);
    vtkIdType d = graph->AddChild(b);
    vtkIdType e = graph->AddChild(c);
    vtkIdType f = graph->AddChild(c);

    // Add labels to vertices
    vtkNew<vtkStringArray> labels;
    labels->SetName("Label");
    labels->InsertValue(a, "a");
    labels->InsertValue(b, "b");
    labels->InsertValue(c, "c");
    labels->InsertValue(d, "d");
    labels->InsertValue(e, "e");
    labels->InsertValue(f, "f");
    graph->GetVertexData()->AddArray(labels);

    // Convert the graph to a tree
    vtkNew<vtkTree> tree;
    if (!tree->CheckedShallowCopy(graph))
    {
        std::cout << "Invalid tree" << std::endl;
        return EXIT_FAILURE;
    }

    // Create a themed graph layout view
    vtkNew<vtkGraphLayoutView> view;
    view->SetRepresentationFromInput(tree);

    vtkViewTheme* theme = vtkViewTheme::CreateMellowTheme();
    view->ApplyViewTheme(theme);
    theme->Delete();

    view->SetVertexColorArrayName("VertexDegree");
    view->SetColorVertices(true);
    view->SetVertexLabelArrayName("Label");
    view->SetVertexLabelVisibility(true);

    view->GetRenderWindow()->SetSize(800, 800);
    view->ResetCamera();
    view->Render();
    view->GetInteractor()->Start();

    return EXIT_SUCCESS;
}
