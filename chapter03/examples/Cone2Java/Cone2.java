//
// This example shows how to add an observer to a Java program.
//
// VTK uses a command/observer design pattern. That is, observers watch for
// particular events that any vtkObject (or subclass) may invoke on
// itself. For example, the vtkRenderer invokes a "StartEvent" as it begins
// to render. Here we add an observer that invokes a command when this event
// is observed.
//

import vtk.vtkActor;
import vtk.vtkConeSource;
import vtk.vtkNativeLibrary;
import vtk.vtkPolyDataMapper;
import vtk.vtkRenderer;
import vtk.vtkRenderWindow;

public class Cone2 {
  // Load VTK native libraries
  static {
    if (!vtkNativeLibrary.LoadAllNativeLibraries()) {
      for (vtkNativeLibrary lib : vtkNativeLibrary.values()) {
        if (!lib.IsLoaded()) {
          System.out.println(lib.GetLibraryName() + " not loaded");
        }
      }
    }
  }

  // Define the callback
  public void myCallback() {
    System.out.println("Starting a render");
  }

  public static void main(String[] args) {
    // Create the pipeline
    vtkConeSource cone = new vtkConeSource();
    cone.SetHeight(3.0);
    cone.SetRadius(1.0);
    cone.SetResolution(10);

    vtkPolyDataMapper coneMapper = new vtkPolyDataMapper();
    coneMapper.SetInputConnection(cone.GetOutputPort());

    vtkActor coneActor = new vtkActor();
    coneActor.SetMapper(coneMapper);

    vtkRenderer ren1 = new vtkRenderer();
    ren1.AddActor(coneActor);
    ren1.SetBackground(0.1, 0.2, 0.4);

    // Add the observer here, the first argument is the event name
    // the second argument is the instance to invoke the method on
    // the third argument is which method to invoke
    Cone2 me = new Cone2();
    ren1.AddObserver("StartEvent", me, "myCallback");

    vtkRenderWindow renWin = new vtkRenderWindow();
    renWin.AddRenderer(ren1);
    renWin.SetSize(300, 300);

    // Loop over 360 degrees and render the cone each time
    for (int i = 0; i < 360; ++i) {
      renWin.Render();
      ren1.GetActiveCamera().Azimuth(1);
    }
  }
}
