/*=========================================================================

  Program:   Visualization Toolkit
  Module:    Cone2.cxx

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
//
// This example shows how to add an observer to a C++ program.
//
// VTK uses a command/observer design pattern. That is, observers watch for
// particular events that any vtkObject (or subclass) may invoke on
// itself. For example, the vtkRenderer invokes a "StartEvent" as it begins
// to render. Here we add an observer that invokes a command when this event
// is observed.
//

#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkCommand.h>
#include <vtkConeSource.h>
#include <vtkNew.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>

#include <iostream>

// Callback for the interaction
class vtkMyCallback : public vtkCommand
{
public:
  static vtkMyCallback* New() { return new vtkMyCallback; }
  vtkTypeMacro(vtkMyCallback, vtkCommand);

  void Execute(vtkObject* caller, unsigned long, void*) override
  {
    vtkRenderer* renderer = reinterpret_cast<vtkRenderer*>(caller);
    std::cout << renderer->GetActiveCamera()->GetPosition()[0] << " "
              << renderer->GetActiveCamera()->GetPosition()[1] << " "
              << renderer->GetActiveCamera()->GetPosition()[2] << "\n";
  }
};

int main()
{
  vtkNew<vtkConeSource> cone;
  cone->SetHeight(3.0);
  cone->SetRadius(1.0);
  cone->SetResolution(10);

  vtkNew<vtkPolyDataMapper> coneMapper;
  coneMapper->SetInputConnection(cone->GetOutputPort());

  vtkNew<vtkActor> coneActor;
  coneActor->SetMapper(coneMapper);

  vtkNew<vtkRenderer> renderer;
  renderer->AddActor(coneActor);
  renderer->SetBackground(0.1, 0.2, 0.4);
  renderer->ResetCamera();

  vtkNew<vtkRenderWindow> renderWindow;
  renderWindow->AddRenderer(renderer);
  renderWindow->SetSize(300, 300);

  // Here is where we setup the observer
  vtkNew<vtkMyCallback> callback;
  renderer->AddObserver(vtkCommand::StartEvent, callback);

  // Loop over 360 degrees and render the cone each time
  for (int i = 0; i < 360; ++i)
  {
    renderWindow->Render();
    renderer->GetActiveCamera()->Azimuth(1);
  }

  return 0;
}
