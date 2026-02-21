// Simple graph visualization with vtkGraphLayoutView in Java.
//
// Creates a random graph and displays it using the default layout.

import vtk.vtkGraphLayoutView;
import vtk.vtkNativeLibrary;
import vtk.vtkRandomGraphSource;

public class HelloWorld {

    static {
        if (!vtkNativeLibrary.LoadAllNativeLibraries()) {
            for (vtkNativeLibrary lib : vtkNativeLibrary.values()) {
                if (!lib.IsLoaded()) {
                    System.out.println(lib.GetLibraryName() + " not loaded");
                }
            }
        }
    }

    public static void main(String[] args) {
        vtkRandomGraphSource source = new vtkRandomGraphSource();

        vtkGraphLayoutView view = new vtkGraphLayoutView();
        view.AddRepresentationFromInputConnection(source.GetOutputPort());

        view.ResetCamera();
        view.Render();
        view.GetInteractor().Start();
    }
}
