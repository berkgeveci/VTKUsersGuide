# Chapter 3: System Overview

The purpose of this chapter is to provide you with an overview of the Visualization Toolkit system, and to show you the basic information you’ll need to create applications in C++, Java, Tcl, and Python. We begin by introducing basic system concepts and object model abstractions. We close the chapter by demonstrating these concepts and describing what you’ll need to know to build applications.

## 3.1 System Architecture

The Visualization Toolkit consists of two basic subsystems: a compiled C++ class library and an “interpreted” wrapper layer that lets you manipulate the compiled classes using the languages Java, Tcl, and Python. See Figure 3–1 below:

![Figure 3-1: The Visualization Toolkit architecture](images/Figure_3-1.png)

*Figure 3–1: The Visualization Toolkit consists of a compiled (C++) core wrapped with various interpreted languages (Java, Tcl, Python).*

The advantage of this architecture is that you can build efficient (in both CPU and memory usage) algorithms in the compiled C++ language, and retain the rapid code development features of interpreted languages (avoidance of compile/link cycle, simple but powerful tools, and access to GUI tools). Of course, for those proficient in C++ and who have the tools to do so, applications can be built entirely in C++.

The Visualization Toolkit is an object-oriented system. The key to using VTK effectively is to develop a good understanding of the underlying object models. Doing so will remove much of the mystery surrounding the use of the hundreds of objects in the system. With this understanding in place it’s much easier to combine objects to build applications. You’ll also need to know something about the capabilities of the many objects in the system; this only comes with reviewing code examples and online documentation. In this User’s Guide, we’ve tried to provide you with useful combinations of VTK objects that you can adapt to your own applications.

In the remainder of this section, we will introduce two major components of the Visualization Toolkit: the visualization pipeline and the rendering engine. The visualization pipeline is used to acquire or create data, process that data, and either write the results to a file or pass the results to the rendering engine for display. The rendering engine is responsible for creating a visual representation of the data. Note that these are not truly rigid architectural components of VTK but are instead conceptual components. The discussion in this chapter will be fairly high-level, but when you combine that with the specific examples in both this chapter and the next, as well as the hundreds of available examples in the VTK source distribution you will gain a good understanding of these components.

### Low-Level Object Model

The VTK object model can be thought of as being rooted in the superclass vtkObject. Nearly all VTK classes are derived from this class, or in some special cases from its superclass vtkObjectBase. All VTK must be created using the object's `New()` method, and must be destroyed using the object's `Delete()` method. VTK objects cannot be allocated on the stack because the constructor is a protected method. Using a common superclass and a unified method of creating and destroying object, VTK is able to provide several basic object-oriented operations.

**Reference Counting**. Objects explicitly store a count of the number of pointers referencing them.

When an object is created through the static `New()` method of a class its initial reference count is 1 because a raw pointer must be used to refer to the new object:

```cpp
vtkObjectBase* obj = vtkExampleClass::New();
```

When other references to the object are created or destroyed the reference count is incremented and decremented using the Register() and UnRegister() methods. Usually this is handled automatically by the various “set” methods provided in the object’s API:

```cpp
otherObject->SetExample(obj);
```

The reference count is now 2 because both the original pointer and a pointer stored inside the other object both refer to it. When the raw pointer originally storing the object is no longer needed the reference is removed using the Delete() method:

```cpp
obj->Delete();
```

From this point forward it is no longer safe to use the original pointer to access the object because the pointer does not own a reference to it. In order to ensure proper management of object references every call to `New()` must be paired with a later call to `Delete()` to be sure no references are leaked.

A "smart pointer" implementation is provided by the class template `vtkSmartPointer<>` which simplifies object management. The above example may be re-written:

```cpp
vtkSmartPointer<vtkObjectBase> obj =
vtkSmartPointer<vtkExampleClass>::New();
otherObject->SetExample(obj);
```

In this case the smart pointer automatically manages the reference it owns. When the smart pointer variable goes out-of-scope and is no longer used, such as when a function in which it is a local variable returns, it automatically informs the object by decrementing the reference count. By using the static `New()` method provided by the smart pointer no raw pointer ever needs to hold a reference to the object, so no call to `Delete()` is needed.

**Run-Time Type Information.** In C++ the real type of an object may be different from the type of pointer used to reference it. All classes in the public interface of VTK have simple identifiers for class names (no templates), so a string is sufficient to identify them. The type of a VTK object may be obtained at run-time with the `GetClassName()` method:

```cpp
const char* type = obj->GetClassName();
```

An object may be tested for whether it is an instance of a particular class or one of its subclasses using the IsA() method:

```cpp
if(obj->IsA("vtkExampleClass")) { ... }
```

A pointer of a superclass type may be safely converted to a more derived type using the static SafeDownCast() method provided by the class of the derived type:

```cpp
vtkExampleClass* example = vtkExampleClass::SafeDownCast(obj)
```

This will succeed at run-time only if the object is truly an instance of the more-derived type and otherwise will return a null pointer.

**Object State Display.** When debugging it is often useful to display a human-readable description of the current state of an object. This can be obtained for VTK objects using the `Print()` method:

```cpp
obj->Print(cout);
```

### The Rendering Engine

The VTK rendering engine consists of the classes in VTK that are responsible for taking the results of the visualization pipeline and displaying them into a window. This involves the following components. Note that this is not an exhaustive list, but rather a sense of the most commonly used objects in the rendering engine. The subheadings used here are the highest level superclass in VTK that represents this type of object, and in many cases where there are multiple choices these are abstract classes defining the basic API across the various concrete subclasses that implement the functionality.

**vtkProp**. Visible depictions of data that exist in the scene are represented by a subclass of vtkProp.

The most commonly used subclasses of vtkProp for displaying objects in 3D are vtkActor (used to represent geometric data in the scene) and vtkVolume (used to represent volumetric data in the scene).

There are also props that represent data in 2D such as vtkActor2D. The vtkProp subclass is generally responsible for knowing its position, size, and orientation in the scene. The parameters used to control the placement of the prop generally depend on whether the prop is for example a 3D object in the scene, or a 2D annotation. 

![Figure 3-2: Dataset types found in VTK](images/Figure_3-2.png)

*Figure 3–2: Dataset types found in VTK. Note that unstructured points can be represented by either polygonal data or unstructured grids.*

For 3D props such as vtkActor and vtkVolume (both subclasses of vtkProp3D which is itself a subclass of vtkProp), you can either directly control parameters such as the object's 3D position, orientation and scale, or you can use a 4x4 transformation matrix. For 2D props that provide annotation such as the vtkScalarBarActor, the size and position of the annotation can be defined in a variety of ways including specifying a position, width, and height relative to the size of the entire viewport. In addition to providing placement control, props generally have a mapper object that holds the data and knows how to render it, and a property object that controls parameters such as color and opacity.

There are a large number (over 50) of specialized props such as vtkImageActor (used to display an image) and vtkPieChartActor (used to create a pie chart visual representation of an array of data values). Some of these specialized props directly contain the parameters that control appearance, and directly have a reference to the input data to be rendered, and therefore do not require the use of a property or a mapper. The vtkFollower prop is a specialized subclass of vtkActor that will automatically update its orientation in order to continually face a specified camera. This is useful for displaying billboards or text in the 3D scene and having them remain visible as the user rotates. The vtkLODActor is also a subclass of vtkActor that automatically changes its geometric representation in order to maintain interactive frame rates, and vtkLODProp3D is a subclass of vtkProp3D that selects between a number of different mappers (perhaps even a mixture of volumetric and geometric mappers) in order to provide interactivity. vtkAssembly allows hierarchies of actors, properly managing the transformations when the hierarchy is translated, rotated or scaled.

**vtkAbstractMapper.** Some props such as vtkActor and vtkVolume use a subclass of vtkAbstractMapper to hold a reference to the input data and to provide the actual rendering functionality. The vtkPolyDataMapper is the primary mapper for rendering polygonal geometry. For volumetric objects, VTK provides several rendering techniques including the vtkFixedPointVolumeRayCastMapper that can be used to rendering vtkImageData, and the vtkProjectedTetrahedra mapper that can be used to render vtkUnstructuredGrid data.

**vtkProperty and vtkVolumeProperty.** Some props use a separate property object to hold the various parameters that control the appearance of the data. This allows you to more easily share appearance settings between different objects in your scene. The vtkActor object uses a vtkProperty to store parameters such as color, opacity, and the ambient, diffuse, and specular coefficient of the material. The vtkVolume object instead uses a vtkVolumeProperty to capture the parameters that are applicable to a volumetric object, such as the transfer functions that map the scalar value to color and opacity. Many mappers also provide functionality to set clipping planes that can be used to reveal interior structure.

**vtkCamera.** The vtkCamera contains the parameters that control how you view the scene. The vtkCamera has a position, a focal point, and a vector defining the direction of "up" in the scene. Other parameters control the specific viewing transformation (parallel or perspective), the scale or view angle of the image, and the near and far clipping planes of the view frustum.

**vtkLight.** When lighting is computed for a scene, one or more vtkLight objects are required. The vtkLight objects store the position and orientation of the light, as well as the color and intensity. Lights also have a type that describes how the light will move with respect to the camera. For example, a Headlight is always located at the camera's position and shines on the camera's focal point, whereas a SceneLight is located at a stationary position in the scene.

**vtkRenderer**. The objects that make up a scene including the props, the camera and the lights are collected together in a vtkRenderer. The vtkRenderer is responsible for managing the rendering process for the scene. Multiple vtkRenderer objects can be used together in a single vtkRenderWindow. These renderers may render into different rectangular regions (known as viewports) of the render window, or may be overlapping.

**vtkRenderWindow**. The vtkRenderWindow provides a connection between the operating system and the VTK rendering engine. Platform specific subclasses of vtkRenderWindow are responsible for opening a window in the native windowing system on your computer and managing the display process. When you develop with VTK, you simply use the platform-independent vtkRenderWindow which is automatically replaced with the correct platform-specific subclass at runtime. The vtkRenderWindow contains a collection of vtkRenderers, and parameters that control rendering features such as stereo, anti-aliasing, motion blur and focal depth.

**vtkRenderWindowInteractor**. The vtkRenderWindowInteractor is responsible for processing mouse, key, and timer events and routing these through VTK's implementation of the command / observer design pattern. A vtkInteractorStyle listens for these events and processes them in order to provide motion controls such as rotating, panning and zooming. The vtkRenderWindowInteractor automatically creates a default interactor style that works well for 3D scenes, but you can instead select one for 2D image viewing for example, or create your own custom interactor style.

**vtkTransform**. Many of the objects in the scene that require placement such as props, lights, and cameras have a vtkTransform parameter that can be used to easily manipulate the position and orientation of the object. The vtkTransform can be used to describe the full range of linear (also known as affine) coordinate transformation in three dimensions, which are internally represented as a 4x4 homogeneous transformation matrix. The vtkTransform object will start with a default identity matrix or you can chain transformation together in a pipeline fashion to create complex behavior. The pipeline mechanism assures that if you modify any transform in the pipeline, all subsequent transforms are updated accordingly.

**vtkLookupTable, vtkColorTransferFunction, and vtkPiecewiseFunction.** Visualizing scalar data often involves defining a mapping from a scalar value to a color and opacity. This is true both in geometric surface rendering where the opacity will define the translucency of the surface, and in volume rendering where the opacity will represent the opacity accumulated along some length of ray passing through the volume. For geometric rendering, this mapping is typically created using a vtkLookupTable, and in volume rendering both the vtkColorTransferFunction and the vtkPiecewiseFunction will be utilized.

**A minimal example.** The following example (adapted from ./VTK/Examples/Rendering/Cxx/Cylinder.cxx) shows how some of these objects can be used to specify and render a scene.

```cpp
vtkCylinderSource *cylinder = vtkCylinderSource::New();

vtkPolyDataMapper *cylinderMapper = vtkPolyDataMapper::New();
cylinderMapper->SetInputConnection(cylinder->GetOutputPort());

vtkActor *cylinderActor = vtkActor::New();
cylinderActor->SetMapper(cylinderMapper);

vtkRenderer *ren1 = vtkRenderer::New();
ren1->AddActor(cylinderActor);

vtkRenderWindow *renWin = vtkRenderWindow::New();
renWin->AddRenderer(ren1);

vtkRenderWindowInteractor *iren = vtkRenderWindowInteractor::New();
iren->SetRenderWindow(renWin);

renWin->Render();
iren->Start();
```

In this example we have directly created a vtkActor, vtkPolyDataMapper, vtkRenderer, vtkRenderWindow and vtkRenderWindowInteractor. Note that a vtkProperty was automatically created by the actor, and a vtkLight and a vtkCamera were automatically created by the vtkRenderer.

### The Visualization Pipeline

The visualization pipeline in VTK can be used to read or create data, analyze and create derivative version of this data, and write the data to disk or pass it along to the rendering engine for display. For example, you may read a 3D volume of data from disk, process it to create a set of triangles representing an isovalued surface through the volume, then write this geometric object back out to disk. Or, you may create a set of spheres and cylinders to represent atoms and bonds, then pass these off to the rendering engine for display.

The Visualization Toolkit uses a data flow approach to transform information into graphical data. There are two basic types of objects involved in this approach.
* vtkDataObject 
* vtkAlgorithm

Data objects represent data of various types. The class vtkDataObject can be viewed as a generic “blob” of data. Data that has a formal structure is referred to as a dataset (class vtkDataSet). Figure 3–2 shows the dataset objects supported in VTK. Datasets consist of a geometric and topological structure (points and cells) as illustrated by the figure; they also have associated attribute data such as scalars or vectors. The attribute data can be associated with the points or cells of the dataset. Cells are topological organizations of points; cells form the atoms of the dataset and are used to interpolate information between points. Figure 19–20 and Figure 19–21 show twenty-three of the most common cell types supported by VTK. Figure 3–3 shows the attribute data supported by VTK.

![Figure 3-3: Data attributes](images/Figure_3-3.png)

*Figure 3–3: Data attributes associated with the points and cells of a dataset.*

Algorithms, also referred to generally as filters, operate on data objects to produce new data objects. Algorithms and data objects are connected together to form visualization pipelines (i.e., dataflow networks). Figure 3–4 is a depiction of a visualization pipeline.

![Figure 3-4: Visualization pipeline](images/Figure_3-4.png)

*Figure 3–4: Data objects are connected with algorithms (filters) to create the visualization pipeline.*

![Figure 3-5: Algorithm types](images/Figure_3-5.png)

*Figure 3–5: Different types of algorithms. Filters ingest one or more inputs and produce one or more outputs.*

This figure together with Figure 3–5 illustrate some important visualization concepts. Source algorithms produce data by reading (reader objects) or constructing one or more data objects (procedural source objects). Filters ingest one or more data objects and generate one or more data objects on output. Mappers (or in some cases, specialized actors) take the data and convert it into a visual representation that is displayed by the rendering engine. A writer can be thought of as a type of mapper that writes data to a file or stream.

There are several important issues regarding the construction of the visualization pipeline that we will briefly introduce here. First, pipeline topology is constructed using variations of the methods

```cpp
aFilter->SetInputConnection( anotherFilter->GetOutputPort() );
```

which sets the input to the filter aFilter to the output of the filter anotherFilter. (Filters with multiple inputs and outputs have similar methods.) Second, we must have a mechanism for controlling the execution of the pipeline. We only want to execute those portions of the pipeline necessary to bring the output up to date. The Visualization Toolkit uses a lazy evaluation scheme (executes only the data is requested) based on an internal modification time of each object. Third, the assembly of the pipeline requires that only those objects compatible with one another can fit together with the `SetInputConnection()` and `GetOutputPort()` methods. VTK produces errors at run-time if the data object types are incompatible. Finally, we must decide whether to cache, or retain, the data objects once the pipeline has executed. Since visualization datasets are typically quite large, this is important to the successful application of visualization tools. VTK offers methods to turn data caching on and off, use of reference counting to avoid copying data, and methods to stream data in pieces if an entire dataset cannot be held in memory. (We recommend that you review the chapter on the Visualization Pipeline in The Visualization Toolkit An Object-Oriented Approach to 3D Graphics text for more information.) Please note that there are many varieties of both algorithm and data objects. Figure 16–2 shows six of the most common data object types supported by the current version of VTK. Algorithm objects vary in their type(s) of input data and output data and of course in the particular algorithm implemented.

**Pipeline Execution.** In the previous section we discussed the need to control the execution of the visualization pipeline. In this section we will expand our understanding of some key concepts regarding pipeline execution.

As indicated in the previous section, the VTK visualization pipeline only executes when data is required for computation (lazy evaluation). Consider this example where we instantiate a reader object and ask for the number of points as shown below. (The language shown here is Tcl.) 

```tcl
vtkPLOT3DReader reader 
reader SetXYZFileName $VTK_DATA_ROOT/Data/combxyz.bin 
[reader GetOutput] GetNumberOfPoints
```

the reader object will return “0” from the GetNumberOfPoints() method call, despite the fact that the data file contains thousands of points. However, if you add the Update() method reader Update [reader GetOutput] GetNumberOfPoints the reader object will return the correct number. In the first example, the GetNumberOfPoints() methods does not require computation, and the object simply returns the current number of points, which is “0”. In the second example, the Update() method forces execution of the pipeline, thereby forcing the reader to execute and read the data from the file indicated. Once the reader has executed, the number of points in its output is set correctly.

Normally, you do not need to manually invoke Update() because the filters are connected into a visualization pipeline. In this case, when the actor receives a request to render itself, it forwards the method to its mapper, and the Update() method is automatically sent through the visualization pipeline. A high-level view of pipeline execution appears in Figure 3–6.

![Figure 3-6: Pipeline execution](images/Figure_3-6.png)

*Figure 3–6: Conceptual overview of pipeline execution.*

As this figure illustrates, the `Render()` method often initiates the request for data; this request is then passed up through the pipeline. Depending on which portions of the pipeline are out-of-date, the filters in the pipeline may reexecute, thereby bringing the data at the end of the pipeline up-to-date; the up-to-date data is then rendered by the actor. (For more information about the execution process, see Chapter 15 "Managing Pipeline Execution".) 

**Image Processing.** VTK supports an extensive set of image processing and volume rendering functionality. In VTK, both 2D (image) and 3D (volume) data are referred to as vtkImageData. An image dataset in VTK is one in which the data is arranged in a regular, axis-aligned array. Images, pixmaps, and bitmaps are examples of 2D image datasets; volumes (a stack of 2D images) is a 3D image dataset.

Algorithms in the imaging pipeline always input and output image data objects. Because of the regular and simple nature of the data, the imaging pipeline has other important features. Volume rendering is used to visualize 3D vtkImageData (see Chapter 7 "Volume Rendering"), and special image viewers are used to view 2D vtkImageData. Almost all algorithms in the imaging pipeline are multithreaded and are capable of streaming data in pieces to satisfy a user-specified memory limit. Filters automatically sense the number of cores and processors available on the system and create that number of threads during execution as well as automatically separating data into pieces that are streamed through the pipeline.

This concludes our brief overview of the Visualization Toolkit system architecture. We recommend the The Visualization Toolkit An Object-Oriented Approach to 3D Graphics text for more details on many of the algorithms found in VTK. Learning by example is another helpful approach. Chapters 4 through 13 contain many annotated examples demonstrating various capabilities of VTK. Also, since source code is available, you may wish to study the examples found in the VTK/Examples directory of the VTK source tree.

With this abbreviated introduction behind us, let’s look at ways to create applications in C++, Tcl, Java, and Python.

## 3.2 Create An Application

This section covers the basic information you need to develop VTK applications in the four programming languages Tcl, C++, Java, and Python. After reading this introduction, you should jump to the subsection(s) that discuss the language(s) you are interested in using. In addition to providing you with instructions on how to create and run a simple application, each section will show you how to take advantage of callbacks in that language.

### User Methods, Observers, and Commands

Callbacks (or user methods) are implemented in VTK using the Subject/Observer and Command design pattern. This means that nearly every class in VTK (every subclass of vtkObject) has an AddObserver() method that can be used to setup callbacks from VTK. The observer looks at every event invoked on an object, and if it matches one of the events that the observer is watching for, then an associated command is invoked (i.e., the callback). For example, all VTK filters invoke a StartEvent right before they start to execute. If you add an observer that watches for a StartEvent then it will get called every time that filter starts to execute. Consider the following Tcl script that creates an instance of vtkElevationFilter, and adds an observer for the StartEvent to call the procedure `PrintStatus`.

```tcl
proc PrintStatus {} {
    puts "Starting to execute the elevation filter" 
    }
    vtkElevationFilter foo
    foo AddObserver StartEvent PrintStatus
```
This type of functionality (i.e., callback) is available in all the languages VTK supports. Each section that follows will show a brief example of how to use it. Further discussion on user methods is provided in the chapter "Integrating With The Windowing System". (This chapter also discusses user interface integration issues.) To create your own application, we suggest starting with one of the examples that come with VTK. They can be found in VTK/Examples in the source distribution. In the source distribution the examples are organized first by topic and then by language. Under VTK/Examples you will find directories for different topics, and under the directories there will be subdirectories for different languages such as Tcl.

### Tcl
Tcl is one of the easiest languages with which to start creating VTK applications. Once you have installed VTK, you should be able to run the Tcl examples that come with the distribution. Under UNIX you have to compile VTK with Tcl support. Under Windows you can install VTK using the provided installers.

**Windows.** Under Windows, you can run a Tcl script just by double clicking on the file (Cone.tcl in this example). If nothing happens you might have an error in your script or a problem with associating Tcl files with the vtk.exe executable. To detect this you need to run vtk.exe first. vtk.exe can be found in your start menu under VTK. Once execution begins, a console window should appear with a prompt in it. At this prompt type in a cd command to change to the directory where Cone.tcl is located. Two examples are given below:

```tcl
% cd "c:/VTK/Examples/Tutorial/Step1/Tcl"
```

Then you will need to source the example script using the following command:

```tcl
% source Cone.tcl
```

Tcl will try to execute Cone.tcl, and you will be able to see errors or warning messages that would otherwise not appear.

**Unix.** Under UNIX, Tcl development can be done by running the VTK executable (after you have compiled the source code) that can be found in your binary directory (e.g., VTK-bin/bin/vtk, VTKSolaris/bin/vtk, etc.) and then providing the Tcl script as the first argument as shown below:

```bash
unix machine> cd VTK/Examples/Tutorial/Step1/Tcl
unix machine> /home/VTK-Solaris/bin/vtk Cone.tcl
```

**User Methods in Tcl.** User methods can be set up as shown in the introduction of this section. An example can be found in Examples/Tutorial/Step2/Tcl/Cone2.tcl. The key changes are shown below:

```tcl
proc myCallback {} {
    puts "Starting to render"
}
vtkRenderer ren1
ren1 AddObserver StartEvent myCallback
```

You may instead simply provide the body of the proc directly to AddObserver():

```tcl
vtkRenderer ren1
ren1 AddObserver StartEvent {puts "Starting to render"}
```

### C++

Using C++ as your development language will typically result in smaller, faster, and more easily deployed applications than most any other language. C++ development also has the advantage that you do not need to compile any additional support for Tcl, Java, or Python. This section will show you how to create a simple VTK C++ application for the PC with Microsoft Visual C++ and also for UNIX using an appropriate compiler. We will start with a simple example called Cone.cxx which can be found in Examples/Tutorial/Step1/Cxx. For both Windows and UNIX you can use a source code installation of VTK or installed binaries. These examples will work with both.

The first step in building your C++ program is to use CMake to generate a makefile or workspace file, depending on your compiler. The CMakeList.txt file that comes with Cone.cxx (shown below) makes use of the FindVTK and UseVTK CMake modules. These modules attempt to locate VTK and then setup your include paths and link lines for building C++ programs. If they do not successfully find VTK, you will have to manually specify the appropriate CMake parameters and rerun CMake as necessary.

```cmake
PROJECT (Step1)

FIND_PACKAGE(VTK REQUIRED)

IF(NOT VTK_USE_RENDERING)
  MESSAGE(FATAL_ERROR "Example ${PROJECT_NAME} requires VTK_USE_RENDERING.")
ENDIF(NOT VTK_USE_RENDERING)

INCLUDE(${VTK_USE_FILE})

ADD_EXECUTABLE(Cone Cone.cxx)

TARGET_LINK_LIBRARIES(Cone vtkRendering)
```

**Microsoft Visual C++.** Once you have run CMake for the Cone example you are ready to start Microsoft Visual C++ and load the generated solution file. For current .NET versions of the compiler this will be named Cone.sln. You can now select a build type (such as Release or Debug) and build your application. If you want to integrate VTK into an existing project that does not use CMake, you can copy the settings from this simple example into your existing workspaces.

Now consider an example of a true Windows application. The process is very similar to what we did above, except that we create a windows application instead of a console application, as shown in the following. Much of the code is standard Windows code and will be familiar to any Windows developer. This example can be found in VTK/Examples/GUI/Win32/SimpleCxx/ Win32Cone.cxx. Note that the only significant change to the CMakeLists.txt file is the addition of the WIN32 parameter in the ADD_EXECUTABLE command. #include "windows.h" #include "vtkConeSource.h" #include "vtkPolyDataMapper.h" #include "vtkRenderWindow.h" #include "vtkRenderWindowInteractor.h" #include "vtkRenderer.h" static HANDLE hinst;

```cpp
long FAR PASCAL WndProc(HWND, UINT, UINT, LONG);

// define the vtk part as a simple c++ class
class myVTKApp {
public:
    myVTKApp(HWND parent);
    ~myVTKApp();
private:
    vtkRenderWindow *renWin;
    vtkRenderer *renderer;
    vtkRenderWindowInteractor *iren;
    vtkConeSource *cone;
    vtkPolyDataMapper *coneMapper;
    vtkActor *coneActor;
};
```

We start by including the required VTK include files. Next we have two standard windows prototypes followed by a small class definition called myVTKApp. When developing in C++, you should try to use object-oriented approaches instead of the scripting programming style found in many of the Tcl examples. Here we are encapsulating the VTK components of the application into a small class.

This is the constructor for myVTKApp. As you can see it allocates the required VTK objects, sets their instance variables, and then connects them to form a visualization pipeline. Most of this is straightforward VTK code except for the vtkRenderWindow. This constructor takes a HWND handle to the parent window that should contain the VTK rendering window. We then use this in the SetParentId() method of vtkRenderWindow so that it will create its window as a child of the window passed to the constructor.

```cpp
myVTKApp::myVTKApp(HWND hwnd)
```

{ // Similar to Examples/Tutorial/Step1/Cxx/Cone.cxx // We create the basic parts of a pipeline and connect them

```cpp
this->renderer = vtkRenderer::New();
this->renWin = vtkRenderWindow::New();
this->renWin->AddRenderer(this->renderer);
```

// setup the parent window

```cpp
this->renWin->SetParentId(hwnd);
this->iren = vtkRenderWindowInteractor::New();
this->iren->SetRenderWindow(this->renWin);
this->cone = vtkConeSource::New();
this->cone->SetHeight( 3.0 );
this->cone->SetRadius( 1.0 );
this->cone->SetResolution( 10 );
this->coneMapper = vtkPolyDataMapper::New();
this->coneMapper->SetInputConnection(this->cone->GetOutputPort());
this->coneActor = vtkActor::New();
this->coneActor->SetMapper(this->coneMapper);
this->renderer->AddActor(this->coneActor);
this->renderer->SetBackground(0.2,0.4,0.3);
this->renWin->SetSize(400,400);

// Finally we start the interactor so that events will be handled
this->renWin->Render();
```

The destructor simply frees all of the VTK objects that were allocated in the constructor.

```cpp
myVTKApp::~myVTKApp()
```

{

```cpp
renWin->Delete();
renderer->Delete();
iren->Delete();
cone->Delete();
coneMapper->Delete();
coneActor->Delete();
```

} The WinMain code here is all standard windows code and has no VTK references in it. As you can see the application has control of the event loop. Events are handled by the WndProc described later in this section. int PASCAL WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpszCmdParam, int nCmdShow) {

```cpp
static char szAppName[] = "Win32Cone";
```

HWND hwnd ; MSG msg ; WNDCLASS wndclass ; if (!hPrevInstance) {

```cpp
wndclass.style = CS_HREDRAW | CS_VREDRAW | CS_OWNDC;
wndclass.lpfnWndProc = WndProc ;
wndclass.cbClsExtra = 0 ;
wndclass.cbWndExtra = 0 ;
wndclass.hInstance = hInstance;
wndclass.hIcon = LoadIcon(NULL,IDI_APPLICATION);
wndclass.hCursor = LoadCursor (NULL, IDC_ARROW);
wndclass.lpszMenuName = NULL;
wndclass.hbrBackground = (HBRUSH)GetStockObject(BLACK_BRUSH);
wndclass.lpszClassName = szAppName;
RegisterClass (&wndclass);
```

}

```cpp
hinst = hInstance;
```

hwnd = CreateWindow ( szAppName, "Draw Window", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 400, 480, NULL, NULL, hInstance, NULL);

```cpp
ShowWindow (hwnd, nCmdShow);
UpdateWindow (hwnd);
```

while (GetMessage (&msg, NULL, 0, 0)) {

```cpp
TranslateMessage (&msg);
DispatchMessage (&msg);
```

} return msg.wParam; } This WndProc is a very simple event handler. For a full application it would be significantly more complicated, but the key integration issues are the same. At the top of this function we declare a static reference to a myVTKApp instance. When handling the WM_CREATE method we create an Exit button and then construct an instance of myVTKApp passing in the handle to the current window. The vtkRenderWindowInteractor will handle all of the events for the vtkRenderWindow, so you do not need to handle them here. You probably will want to add code to handle resizing events so that the render window resizes appropriately with respect to your overall user interface. If you do not set the ParentId of the vtkRenderWindow, it will show up as a top-level independent window. Everything else should behave the same as before. long FAR PASCAL WndProc (HWND hwnd, UINT message, UINT wParam, LONG lParam) { static HWND ewin; static myVTKApp *theVTKApp; switch (message) { case WM_CREATE: { ewin = CreateWindow("button","Exit", WS_CHILD | WS_VISIBLE | SS_CENTER, 0,400,400,60, hwnd,(HMENU)2, (HINSTANCE)GetWindowLong(hwnd,GWL_HINSTANCE), NULL);

```cpp
theVTKApp = new myVTKApp(hwnd);
```

return 0; } case WM_COMMAND: switch (wParam) { case 2:

```cpp
PostQuitMessage (0);
```

if (theVTKApp) { delete theVTKApp;

```cpp
theVTKApp = NULL;
}
break;
```

} return 0; case WM_DESTROY:

```cpp
PostQuitMessage (0);
```

if (theVTKApp) { delete theVTKApp;

```cpp
theVTKApp = NULL;
```

} return 0; }

```cpp
return DefWindowProc (hwnd, message, wParam, lParam);
}
```

**UNIX.** Creating a C++ application on UNIX is done by running CMake and then make. CMake creates a makefile that specifies the include paths, link lines, and dependencies. The make program then uses this makefile to compile the application. This should result in a Cone executable that you can run. If Cone.cxx does not compile then check the make errors and correct them. Make sure that the values in the top of CMakeCache.txt are valid. If it does compile, but you receive errors when you try running it, you might need to set your LD_LIBRARY_PATH as described in Chapter 2.

**User Methods in C++.** You can add user methods (using the observer/command design pattern) in C++ by creating a subclass of vtkCommand that overrides the Execute() method. Consider the following example taken from VTK/Examples/Tutorial/Step2/Cxx/Cone2.cxx:

```cpp
class vtkMyCallback : public vtkCommand {
    static myCallback *New() {return new vtkMyCallback;}
    virtual void Execute(vtkObject *caller, unsigned long, void *) {
        vtkRenderer *renderer = reinterpret_cast<vtkRenderer*>(caller);
        cout << renderer->GetActiveCamera()->GetPosition()[0] << " "
             << renderer->GetActiveCamera()->GetPosition()[1] << " "
             << renderer->GetActiveCamera()->GetPosition()[2] << "\n";
    }
};
```

While the Execute() method is always passed the calling object (caller) you are not required to use it.

If you do use the caller you will typically want to perform a SafeDownCast() to the actual type. For example:

```cpp
virtual void Execute(vtkObject *caller, unsigned long, void *callData) {
    vtkRenderer *ren = vtkRenderer::SafeDownCast(caller);
    if (ren) { ren->SetBackground(0.2,0.3,0.4); }
}
```

Once you have created your subclass of vtkCommand you are ready to add an observer that will call your command on certain events. This can be done as follows:

```cpp
vtkMyCallback *mo1 = vtkMyCallback::New();
ren1->AddObserver(vtkCommand::StartEvent,mo1);
mo1->Delete();
```

The above code creates an instance of myCallback and then adds an observer on ren1 for the StartEvent. Whenever ren1 starts to render, the Execute() method of vtkMyCallback will be called. When ren1 is deleted, the callback will be deleted as well.

### Java

To create Java applications you must first have a working Java development environment. This section provides instructions for using Sun's JDK 1.3 or later on either Windows or UNIX. Once your JDK has been installed and you have installed VTK, you need to set your CLASSPATH environment variable to include the VTK classes. Under Microsoft Windows this can be set by right clicking on the My Computer icon, selecting the properties option, then selecting the Advanced tab, and then clicking the Environment Variables button. Then add a CLASSPATH environment variable and set it to include the path to your vtk.jar file, your Wrapping/Java directory, and the current directory.

For a Windows build it will be something like "C:\vtk-bin\bin\vtk.jar;C:\vtkbin\Wrapping\Java;.". Under UNIX you should set your CLASSPATH environment variable to something similar to "/yourdisk/vtk-bin/bin/vtk.jar;/yourdisk/vtk-bin/Wrapping/ Java;.".

The next step is to byte compile your Java program. For starters try byte compiling (with javac) the Cone.java example that comes with VTK under VTK/Examples/Tutorial/Step1/Java.

Then you should be able to run the resulting application using the java command. It should display a cone which rotates 360 degrees and then exits. The next step is to create your own applications using the examples provided as a starting point.

**User Methods in Java.** You set up a callback by passing three arguments. The first is the name of the event you are interested in, the second is an instance of a class, the third is the name of the method you want to invoke. In this example we set up the StartEvent to invoke the myCallback method on me (which is an instance of Cone2). The myCallback method must of course be a valid method of Cone2 to avoid an error. (This code fragment is from VTK/Examples/Tutorial/Step2/Java/cone2.java.)

```java
public void myCallback() {
    System.out.println("Starting a render");
}
```

```java
Cone2 me = new Cone2();
ren1.AddObserver("StartEvent",me,"myCallback");
```

### Python

If you have built VTK with Python support, a vtkpython executable will be created. Using this executable, you should be able to run Examples/Tutorial/Step1/Python/Cone.py as follows:

```bash
vtkpython Cone.py
```

Creating your own Python scripts is a simple matter of using some of our example scripts as a starting point.

**User Methods in Python.** User methods can be set up by defining a function and then passing it as the argument to the AddObserver as shown below:

```python
def myCallback(obj, event):
    print "Starting to render"

ren1.AddObserver("StartEvent", myCallback)
```

The complete source code for the example shown above is in VTK/Examples/Tutorial/Step2/Python/Cone2.py.

## 3.3 Conversion Between Languages

As we have seen, VTK’s core is implemented in C++ and then wrapped with the Tcl, Java, and Python programming languages. This means that you have a language choice when developing applications. Your choice will depend on which language you are most comfortable with, the nature of the application, and whether you need access to internal data structures and/or have special performance requirements. C++ offers several advantages over the other languages when you need to access internal data structure or require the highest-performing application possible. However, using C++ means the extra burden of the compile/link cycle, which often slows the software development process.

You may find yourself developing prototypes in an interpreted language such as Tcl and then converting them to C++. Or, you may discover example code (in the VTK distribution or from other users) that you wish to convert to your implementation language.

Converting VTK code from one language to another is fairly straightforward. Class names and method names remain the same across languages; what changes are the implementation details and GUI interface, if any. For example, the C++ statement

```cpp
anActor->GetProperty()->SetColor(red,green,blue);
```

in Tcl becomes [anActor GetProperty] SetColor $red $green $blue in Java becomes

```cpp
anActor.GetProperty().SetColor(red,green,blue);
```

and in Python becomes anActor.GetProperty().SetColor(red,green,blue) One major limitation you’ll find is that some C++ applications cannot be converted to the other three languages because of pointer manipulation.While it is always possible to get and set individual values from the wrapped languages, it is not always possible to obtain a raw pointer to quickly traverse and inspect or modify a large structure. If your application requires this level of data inspection or manipulation, you can either develop directly in C++ or extend VTK at the C++ level with your required high-performance classes, then use these new classes from your preferred interpreted language.

### Part II

### Learn VTK By Example
