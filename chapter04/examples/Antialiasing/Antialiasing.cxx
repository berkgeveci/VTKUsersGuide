//
// This example demonstrates point antialiasing by displaying the vertices
// of a mesh representing a sphere with point smoothing enabled.
//

#include <vtkNew.h>
#include <vtkActor.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSphereSource.h>

int main()
{
  vtkNew<vtkRenderWindowInteractor> interactor;
  vtkNew<vtkRenderWindow> renderWindow;
  interactor->SetRenderWindow(renderWindow);
  renderWindow->SetMultiSamples(0);     // no multisampling
  renderWindow->SetPointSmoothing(1);   // point antialiasing

  vtkNew<vtkRenderer> renderer;
  renderWindow->AddRenderer(renderer);

  vtkNew<vtkSphereSource> sphere;
  vtkNew<vtkPolyDataMapper> mapper;
  mapper->SetInputConnection(sphere->GetOutputPort());

  vtkNew<vtkActor> actor;
  actor->SetMapper(mapper);

  vtkProperty* prop = actor->GetProperty();
  prop->SetRepresentationToPoints();   // we want to see points
  prop->SetPointSize(2.0);            // big enough to notice antialiasing
  prop->SetLighting(false);           // don't be disturbed by shading

  renderer->AddActor(actor);
  interactor->Start();
  return 0;
}
