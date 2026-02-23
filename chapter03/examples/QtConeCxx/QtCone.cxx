/*=========================================================================

  Program:   Visualization Toolkit
  Module:    QtCone.cxx

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
//
// This example demonstrates how to embed a VTK render window inside a
// Qt application. A cone is rendered in a QVTKOpenGLNativeWidget placed
// as the central widget of a QMainWindow.
//

#include <QApplication>
#include <QMainWindow>
#include <QSurfaceFormat>
#include <QVTKOpenGLNativeWidget.h>

#include <vtkActor.h>
#include <vtkConeSource.h>
#include <vtkGenericOpenGLRenderWindow.h>
#include <vtkNew.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderer.h>

int main(int argc, char* argv[])
{
  // Set the default surface format BEFORE constructing QApplication.
  QSurfaceFormat::setDefaultFormat(QVTKOpenGLNativeWidget::defaultFormat());
  QApplication app(argc, argv);

  // Create a QMainWindow with a VTK render widget.
  QMainWindow window;
  window.setWindowTitle("VTK Qt Cone Example");
  window.resize(800, 600);

  QVTKOpenGLNativeWidget* vtkWidget = new QVTKOpenGLNativeWidget();
  window.setCentralWidget(vtkWidget);

  // Prevent the macOS trackpad from generating spurious button-press
  // events via touch input.  Normal mouse/trackpad clicks still work.
  vtkWidget->setAttribute(Qt::WA_AcceptTouchEvents, false);

  // Create a vtkGenericOpenGLRenderWindow and assign it to the widget.
  vtkNew<vtkGenericOpenGLRenderWindow> renderWindow;
  vtkWidget->setRenderWindow(renderWindow);

  // Build a VTK pipeline.
  vtkNew<vtkConeSource> cone;
  cone->SetHeight(3.0);
  cone->SetRadius(1.0);
  cone->SetResolution(30);

  vtkNew<vtkPolyDataMapper> mapper;
  mapper->SetInputConnection(cone->GetOutputPort());

  vtkNew<vtkActor> actor;
  actor->SetMapper(mapper);

  vtkNew<vtkRenderer> renderer;
  renderer->AddActor(actor);
  renderer->SetBackground(0.1, 0.2, 0.4);

  renderWindow->AddRenderer(renderer);

  window.show();

  // Qt's event loop replaces vtkRenderWindowInteractor::Start().
  return app.exec();
}
