// Simple graph visualization with vtkGraphLayoutView.
//
// Creates a random graph and displays it using the default layout.

#include <vtkGraphLayoutView.h>
#include <vtkNew.h>
#include <vtkRandomGraphSource.h>
#include <vtkRenderWindowInteractor.h>

int main(int, char*[])
{
    vtkNew<vtkRandomGraphSource> source;

    vtkNew<vtkGraphLayoutView> view;
    view->SetRepresentationFromInputConnection(source->GetOutputPort());

    view->ResetCamera();
    view->Render();
    view->GetInteractor()->Start();

    return 0;
}
