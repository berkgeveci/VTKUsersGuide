//
// This example demonstrates depth peeling for correct rendering of
// translucent polygonal geometry. A sinusoidal image source is used
// to create translucent surfaces.
//

#include <vtkNew.h>
#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkDataSetSurfaceFilter.h>
#include <vtkImageData.h>
#include <vtkImageSinusoidSource.h>
#include <vtkLookupTable.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>

#include <iostream>

int main()
{
  vtkNew<vtkRenderWindowInteractor> interactor;
  vtkNew<vtkRenderWindow> renderWindow;
  renderWindow->SetMultiSamples(0);
  renderWindow->SetAlphaBitPlanes(1);
  interactor->SetRenderWindow(renderWindow);

  vtkNew<vtkRenderer> renderer;
  renderWindow->AddRenderer(renderer);
  renderer->SetUseDepthPeeling(1);
  renderer->SetMaximumNumberOfPeels(200);
  renderer->SetOcclusionRatio(0.1);

  vtkNew<vtkImageSinusoidSource> imageSource;
  imageSource->SetWholeExtent(0, 9, 0, 9, 0, 9);
  imageSource->SetPeriod(5);
  imageSource->Update();

  vtkImageData* image = imageSource->GetOutput();
  double range[2];
  image->GetScalarRange(range);

  vtkNew<vtkDataSetSurfaceFilter> surface;
  surface->SetInputConnection(imageSource->GetOutputPort());

  vtkNew<vtkPolyDataMapper> mapper;
  mapper->SetInputConnection(surface->GetOutputPort());

  vtkNew<vtkLookupTable> lut;
  lut->SetTableRange(range);
  lut->SetAlphaRange(0.5, 0.5);
  lut->SetHueRange(0.2, 0.7);
  lut->SetNumberOfTableValues(256);
  lut->Build();

  mapper->SetScalarVisibility(1);
  mapper->SetLookupTable(lut);

  vtkNew<vtkActor> actor;
  renderer->AddActor(actor);
  actor->SetMapper(mapper);

  renderer->SetBackground(0.1, 0.3, 0.0);
  renderWindow->SetSize(400, 400);
  renderWindow->Render();

  if (renderer->GetLastRenderingUsedDepthPeeling())
  {
    std::cout << "depth peeling was used" << std::endl;
  }
  else
  {
    std::cout << "depth peeling was not used (alpha blending instead)"
              << std::endl;
  }

  vtkCamera* camera = renderer->GetActiveCamera();
  camera->Azimuth(-40.0);
  camera->Elevation(20.0);
  renderWindow->Render();
  interactor->Start();
  return 0;
}
