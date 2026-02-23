# Chapter 3: System Overview

The purpose of this chapter is to provide you with an overview of the Visualization Toolkit system, and to show you the basic information you'll need to create applications in C++, Java, and Python. We begin by introducing basic system concepts and object model abstractions. We close the chapter by demonstrating these concepts and describing what you’ll need to know to build applications.

## 3.1 System Architecture

The Visualization Toolkit consists of two basic subsystems: a compiled C++ class library and an "interpreted" wrapper layer that lets you manipulate the compiled classes using the languages Java and Python. See Figure 3–1 below:

![Figure 3-1: The Visualization Toolkit architecture](images/Figure_3-1.png)

*Figure 3–1: The Visualization Toolkit consists of a compiled (C++) core wrapped with various interpreted languages (Java, Python).*

The advantage of this architecture is that you can build efficient (in both CPU and memory usage) algorithms in the compiled C++ language, and retain the rapid code development features of interpreted languages (avoidance of compile/link cycle, simple but powerful tools, and access to GUI tools). Of course, for those proficient in C++ and who have the tools to do so, applications can be built entirely in C++.

The Visualization Toolkit is an object-oriented system. The key to using VTK effectively is to develop a good understanding of the underlying object models. Doing so will remove much of the mystery surrounding the use of the hundreds of objects in the system. With this understanding in place it’s much easier to combine objects to build applications. You’ll also need to know something about the capabilities of the many objects in the system; this only comes with reviewing code examples and online documentation. In this User’s Guide, we’ve tried to provide you with useful combinations of VTK objects that you can adapt to your own applications.

In the remainder of this section, we will introduce two major components of the Visualization Toolkit: the visualization pipeline and the rendering engine. The visualization pipeline is used to acquire or create data, process that data, and either write the results to a file or pass the results to the rendering engine for display. The rendering engine is responsible for creating a visual representation of the data. Note that these are not truly rigid architectural components of VTK but are instead conceptual components. The discussion in this chapter will be fairly high-level, but when you combine that with the specific examples in both this chapter and the next, as well as the hundreds of available examples in the VTK source distribution you will gain a good understanding of these components.

### Low-Level Object Model

The VTK object model can be thought of as being rooted in the superclass vtkObject. Nearly all VTK classes are derived from this class, or in some special cases from its superclass vtkObjectBase. All VTK objects must be created using the object's `New()` method, and must be destroyed using the object's `Delete()` method. VTK objects cannot be allocated on the stack because the constructor is a protected method. Using a common superclass and a unified method of creating and destroying object, VTK is able to provide several basic object-oriented operations.

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

The preferred modern approach is to use `vtkNew<>`, which automatically manages object lifetime. When a `vtkNew` variable goes out-of-scope, it automatically decrements the reference count. No call to `Delete()` is needed:

```cpp
vtkNew<vtkExampleClass> obj;
otherObject->SetExample(obj);
```

For cases requiring shared ownership, `vtkSmartPointer<>` can be used instead:

```cpp
vtkSmartPointer<vtkExampleClass> obj =
    vtkSmartPointer<vtkExampleClass>::New();
otherObject->SetExample(obj);
```

In both cases the smart pointer automatically manages the reference it owns. When the variable goes out-of-scope, it automatically informs the object by decrementing the reference count.

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
vtkExampleClass* example = vtkExampleClass::SafeDownCast(obj);
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

For 3D props such as vtkActor and vtkVolume (both subclasses of vtkProp3D which is itself a subclass of vtkProp), you can either directly control parameters such as the object's 3D position, orientation and scale, or you can use a 4x4 transformation matrix. For 2D props that provide annotation such as the vtkScalarBarActor, the size and position of the annotation can be defined in a variety of ways including specifying a position, width, and height relative to the size of the entire viewport. In addition to providing placement control, props generally have a mapper object that holds the data and knows how to render it, and a property object that controls parameters such as color and opacity.

There are a large number (over 50) of specialized props such as vtkImageSlice (used to display an image) and vtkPieChartActor (used to create a pie chart visual representation of an array of data values). Some of these specialized props directly contain the parameters that control appearance, and directly have a reference to the input data to be rendered, and therefore do not require the use of a property or a mapper. The vtkFollower prop is a specialized subclass of vtkActor that will automatically update its orientation in order to continually face a specified camera. This is useful for displaying billboards or text in the 3D scene and having them remain visible as the user rotates. The vtkLODActor is also a subclass of vtkActor that automatically changes its geometric representation in order to maintain interactive frame rates, and vtkLODProp3D is a subclass of vtkProp3D that selects between a number of different mappers (perhaps even a mixture of volumetric and geometric mappers) in order to provide interactivity. vtkAssembly allows hierarchies of actors, properly managing the transformations when the hierarchy is translated, rotated or scaled.

**vtkAbstractMapper.** Some props such as vtkActor and vtkVolume use a subclass of vtkAbstractMapper to hold a reference to the input data and to provide the actual rendering functionality. The vtkPolyDataMapper is the primary mapper for rendering polygonal geometry. For volumetric objects, the recommended mapper is vtkSmartVolumeMapper, which automatically selects the best available rendering technique at runtime (typically GPU-accelerated ray casting via vtkGPUVolumeRayCastMapper). vtkSmartVolumeMapper can render vtkImageData, while vtkProjectedTetrahedraMapper can be used to render vtkUnstructuredGrid data.

**vtkProperty and vtkVolumeProperty.** Some props use a separate property object to hold the various parameters that control the appearance of the data. This allows you to more easily share appearance settings between different objects in your scene. The vtkActor object uses a vtkProperty to store parameters such as color, opacity, and the ambient, diffuse, and specular coefficient of the material. The vtkVolume object instead uses a vtkVolumeProperty to capture the parameters that are applicable to a volumetric object, such as the transfer functions that map the scalar value to color and opacity. Many mappers also provide functionality to set clipping planes that can be used to reveal interior structure.

**vtkCamera.** The vtkCamera contains the parameters that control how you view the scene. The vtkCamera has a position, a focal point, and a vector defining the direction of "up" in the scene. Other parameters control the specific viewing transformation (parallel or perspective), the scale or view angle of the image, and the near and far clipping planes of the view frustum.

**vtkLight.** When lighting is computed for a scene, one or more vtkLight objects are required. The vtkLight objects store the position and orientation of the light, as well as the color and intensity. Lights also have a type that describes how the light will move with respect to the camera. For example, a Headlight is always located at the camera's position and shines on the camera's focal point, whereas a SceneLight is located at a stationary position in the scene.

**vtkRenderer**. The objects that make up a scene including the props, the camera and the lights are collected together in a vtkRenderer. The vtkRenderer is responsible for managing the rendering process for the scene. Multiple vtkRenderer objects can be used together in a single vtkRenderWindow. These renderers may render into different rectangular regions (known as viewports) of the render window, or may be overlapping.

**vtkRenderWindow**. The vtkRenderWindow provides a connection between the operating system and the VTK rendering engine. Platform specific subclasses of vtkRenderWindow are responsible for opening a window in the native windowing system on your computer and managing the display process. When you develop with VTK, you simply use the platform-independent vtkRenderWindow which is automatically replaced with the correct platform-specific subclass at runtime. The vtkRenderWindow contains a collection of vtkRenderers, and parameters that control rendering features such as stereo, anti-aliasing, motion blur and focal depth.

**vtkRenderWindowInteractor**. The vtkRenderWindowInteractor is responsible for processing mouse, key, and timer events and routing these through VTK's implementation of the command / observer design pattern. A vtkInteractorStyle listens for these events and processes them in order to provide motion controls such as rotating, panning and zooming. The vtkRenderWindowInteractor automatically creates a default interactor style that works well for 3D scenes, but you can instead select one for 2D image viewing for example, or create your own custom interactor style.

**vtkTransform**. Many of the objects in the scene that require placement such as props, lights, and cameras have a vtkTransform parameter that can be used to easily manipulate the position and orientation of the object. The vtkTransform can be used to describe the full range of linear (also known as affine) coordinate transformation in three dimensions, which are internally represented as a 4x4 homogeneous transformation matrix. The vtkTransform object will start with a default identity matrix or you can chain transformation together in a pipeline fashion to create complex behavior. The pipeline mechanism assures that if you modify any transform in the pipeline, all subsequent transforms are updated accordingly.

**vtkLookupTable, vtkColorTransferFunction, and vtkPiecewiseFunction.** Visualizing scalar data often involves defining a mapping from a scalar value to a color and opacity. This is true both in geometric surface rendering where the opacity will define the translucency of the surface, and in volume rendering where the opacity will represent the opacity accumulated along some length of ray passing through the volume. For geometric rendering, this mapping is typically created using a vtkLookupTable, and in volume rendering both the vtkColorTransferFunction and the vtkPiecewiseFunction will be utilized.

**A minimal example.** The following example shows how some of these objects can be used to specify and render a scene.

```cpp
vtkNew<vtkCylinderSource> cylinder;

vtkNew<vtkPolyDataMapper> cylinderMapper;
cylinderMapper->SetInputConnection(cylinder->GetOutputPort());

vtkNew<vtkActor> cylinderActor;
cylinderActor->SetMapper(cylinderMapper);

vtkNew<vtkRenderer> renderer;
renderer->AddActor(cylinderActor);

vtkNew<vtkRenderWindow> renderWindow;
renderWindow->AddRenderer(renderer);

vtkNew<vtkRenderWindowInteractor> interactor;
interactor->SetRenderWindow(renderWindow);

renderWindow->Render();
interactor->Start();
```

In this example we have directly created a vtkActor, vtkPolyDataMapper, vtkRenderer, vtkRenderWindow and vtkRenderWindowInteractor using `vtkNew<>` for automatic memory management. Note that a vtkProperty was automatically created by the actor, and a vtkLight and a vtkCamera were automatically created by the vtkRenderer.

### The Visualization Pipeline

The visualization pipeline in VTK can be used to read or create data, analyze and create derivative version of this data, and write the data to disk or pass it along to the rendering engine for display. For example, you may read a 3D volume of data from disk, process it to create a set of triangles representing an isovalued surface through the volume, then write this geometric object back out to disk. Or, you may create a set of spheres and cylinders to represent atoms and bonds, then pass these off to the rendering engine for display.

The Visualization Toolkit uses a data flow approach to transform information into graphical data. There are two basic types of objects involved in this approach.
* vtkDataObject 
* vtkAlgorithm

Data objects represent data of various types. The class vtkDataObject can be viewed as a generic "blob" of data. Data that has a formal structure is referred to as a dataset (class vtkDataSet). Figure 3–2 shows the dataset objects supported in VTK.

![Figure 3-2: Dataset types found in VTK](images/Figure_3-2.png)

*Figure 3–2: Dataset types found in VTK. Note that unstructured points can be represented by either polygonal data or unstructured grids.*

Datasets consist of a geometric and topological structure (points and cells) as illustrated by the figure; they also have associated attribute data such as scalars or vectors. The attribute data can be associated with the points or cells of the dataset. Cells are topological organizations of points; cells form the atoms of the dataset and are used to interpolate information between points. VTK supports over twenty cell types including vertices, lines, triangles, quadrilaterals, tetrahedra, hexahedra, and higher-order variants. Figure 3–3 shows the attribute data supported by VTK.

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

which sets the input to the filter aFilter to the output of the filter anotherFilter. (Filters with multiple inputs and outputs have similar methods.) Second, we must have a mechanism for controlling the execution of the pipeline. We only want to execute those portions of the pipeline necessary to bring the output up to date. The Visualization Toolkit uses a lazy evaluation scheme (executes only the data is requested) based on an internal modification time of each object. Third, the assembly of the pipeline requires that only those objects compatible with one another can fit together with the `SetInputConnection()` and `GetOutputPort()` methods. VTK produces errors at run-time if the data object types are incompatible. Finally, we must decide whether to cache, or retain, the data objects once the pipeline has executed. Since visualization datasets are typically quite large, this is important to the successful application of visualization tools. VTK offers methods to turn data caching on and off, use of reference counting to avoid copying data, and methods to stream data in pieces if an entire dataset cannot be held in memory. (We recommend that you review the chapter on the Visualization Pipeline in *The Visualization Toolkit An Object-Oriented Approach to 3D Graphics* text for more information.) Please note that there are many varieties of both algorithm and data objects. Figure 3–2 shows the most common data object types supported by VTK. Algorithm objects vary in their type(s) of input data and output data and of course in the particular algorithm implemented.

**Pipeline Execution.** In the previous section we discussed the need to control the execution of the visualization pipeline. In this section we will expand our understanding of some key concepts regarding pipeline execution.

As indicated in the previous section, the VTK visualization pipeline only executes when data is required for computation (lazy evaluation). Consider this example where we instantiate a reader object and ask for the number of points as shown below.

```python
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader

reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName("Data/combxyz.bin")
reader.GetOutput().GetBlock(0)  # returns None
```

the reader object will return `None` because the pipeline has not yet executed and the output contains no data, despite the fact that the data file contains thousands of points. However, if you call the `Update()` method first:

```python
reader.Update()
reader.GetOutput().GetBlock(0).GetNumberOfPoints()  # returns 7194
```

the reader object will return the correct number. In the first example, no computation has been requested, so the output is empty. In the second example, the `Update()` method forces execution of the pipeline, thereby forcing the reader to read the data from the file. Once the reader has executed, its output is populated with the data from the file.

Normally, you do not need to manually invoke Update() because the filters are connected into a visualization pipeline. In this case, when the actor receives a request to render itself, it forwards the method to its mapper, and the Update() method is automatically sent through the visualization pipeline. A high-level view of pipeline execution appears in Figure 3–6.

![Figure 3-6: Pipeline execution](images/Figure_3-6.png)

*Figure 3–6: Conceptual overview of pipeline execution.*

As this figure illustrates, the `Render()` method often initiates the request for data; this request is then passed up through the pipeline. Depending on which portions of the pipeline are out-of-date, the filters in the pipeline may reexecute, thereby bringing the data at the end of the pipeline up-to-date; the up-to-date data is then rendered by the actor.

**Image Processing.** VTK supports an extensive set of image processing and volume rendering functionality. In VTK, both 2D (image) and 3D (volume) data are referred to as vtkImageData. An image dataset in VTK is one in which the data is arranged in a regular, axis-aligned array. Images, pixmaps, and bitmaps are examples of 2D image datasets; volumes (a stack of 2D images) are 3D image datasets.

Algorithms in the imaging pipeline always input and output image data objects. Because of the regular and simple nature of the data, the imaging pipeline has other important features. Volume rendering is used to visualize 3D vtkImageData (see Chapter 7 "Volume Rendering"), and special image viewers are used to view 2D vtkImageData. Almost all algorithms in the imaging pipeline are multithreaded and are capable of streaming data in pieces to satisfy a user-specified memory limit. Filters automatically sense the number of cores and processors available on the system and create that number of threads during execution as well as automatically separating data into pieces that are streamed through the pipeline.

This concludes our brief overview of the Visualization Toolkit system architecture. We recommend *The Visualization Toolkit An Object-Oriented Approach to 3D Graphics* text for more details on many of the algorithms found in VTK. Learning by example is another helpful approach. Chapters 4 through 13 contain many annotated examples demonstrating various capabilities of VTK. Also, since source code is available, you may wish to study the examples found in the VTK/Examples directory of the VTK source tree.

With this abbreviated introduction behind us, let's look at ways to create applications in C++, Java, and Python.

## 3.2 Create An Application

This section covers the basic information you need to develop VTK applications in C++, Java, and Python. After reading this introduction, you should jump to the subsection(s) that discuss the language(s) you are interested in using. In addition to providing you with instructions on how to create and run a simple application, each section will show you how to take advantage of callbacks in that language.

### User Methods, Observers, and Commands

Callbacks (or user methods) are implemented in VTK using the Subject/Observer and Command design pattern. This means that nearly every class in VTK (every subclass of vtkObject) has an AddObserver() method that can be used to setup callbacks from VTK. The observer looks at every event invoked on an object, and if it matches one of the events that the observer is watching for, then an associated command is invoked (i.e., the callback). For example, all VTK filters invoke a StartEvent right before they start to execute. If you add an observer that watches for a StartEvent then it will get called every time that filter starts to execute. Consider the following Python script that creates an instance of vtkElevationFilter, and adds an observer for the StartEvent to call the function `print_status`.

```python
from vtkmodules.vtkFiltersCore import vtkElevationFilter

def print_status(obj, event):
    print("Starting to execute the elevation filter")

foo = vtkElevationFilter()
foo.AddObserver("StartEvent", print_status)
```

This type of functionality (i.e., callback) is available in all the languages VTK supports. Each section that follows will show a brief example of how to use it. To create your own application, we suggest starting with one of the examples that come with VTK or the many examples available at https://examples.vtk.org.

### C++

Using C++ as your development language will typically result in smaller, faster, and more easily deployed applications than most any other language. C++ development also has the advantage that you do not need to compile any additional support for Java or Python.

The first step in building your C++ program is to use CMake to generate a makefile or project file, depending on your compiler. A typical CMakeLists.txt for a VTK C++ application uses `find_package` to locate VTK and specify the required components:

```cmake
cmake_minimum_required(VERSION 3.12...3.28)
project(MyConeExample)

find_package(VTK
  COMPONENTS
    CommonCore
    FiltersSources
    InteractionStyle
    RenderingCore
    RenderingOpenGL2)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "MyConeExample: Unable to find the VTK build folder.")
endif()

add_executable(Cone Cone.cxx)
target_link_libraries(Cone PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS Cone
  MODULES ${VTK_LIBRARIES})
```

**Building.** Once you have run CMake, build the application using your platform's build tool. On UNIX, run `make` (or `ninja` if using the Ninja generator). CMake creates a makefile that specifies the include paths, link lines, and dependencies. If the application does not compile, check the build errors and make sure the VTK_DIR CMake variable points to a valid VTK build or install directory.

**User Methods in C++.** VTK provides several ways to set up callbacks using the observer/command design pattern.

**Using vtkCallbackCommand.** The simplest approach for standalone callbacks is to use `vtkCallbackCommand` with a free function:

```cpp
void PrintCameraPosition(
  vtkObject* caller, unsigned long, void*, void*)
{
  vtkRenderer* renderer = static_cast<vtkRenderer*>(caller);
  double* pos = renderer->GetActiveCamera()->GetPosition();
  std::cout << pos[0] << " " << pos[1] << " " << pos[2] << "\n";
}

vtkNew<vtkCallbackCommand> callback;
callback->SetCallback(PrintCameraPosition);
renderer->AddObserver(vtkCommand::StartEvent, callback);
```

**Using member function callbacks.** If you are working within a class, you can pass a member function pointer directly to `AddObserver()` without creating a separate command object:

```cpp
renderer->AddObserver(
  vtkCommand::StartEvent, this, &MyClass::OnStartRender);
```

**Using a vtkCommand subclass.** For more complex callbacks that need to carry state, you can create a subclass of vtkCommand that overrides the `Execute()` method:

```cpp
class vtkMyCallback : public vtkCommand
{
public:
  static vtkMyCallback* New() { return new vtkMyCallback; }
  vtkTypeMacro(vtkMyCallback, vtkCommand);

  void Execute(vtkObject* caller, unsigned long, void*) override
  {
    vtkRenderer* renderer = vtkRenderer::SafeDownCast(caller);
    if (renderer)
    {
      double* pos = renderer->GetActiveCamera()->GetPosition();
      std::cout << pos[0] << " " << pos[1] << " " << pos[2] << "\n";
    }
  }
};

vtkNew<vtkMyCallback> callback;
renderer->AddObserver(vtkCommand::StartEvent, callback);
```

Note that `SafeDownCast()` is the preferred way to convert the caller to the expected type, as it returns a null pointer if the cast is not valid.

### Java

To create Java applications you must first have a working Java development environment. Once your JDK has been installed and you have built VTK with Java wrapping enabled, you need to set your CLASSPATH environment variable to include the path to your vtk.jar file and the current directory.

**User Methods in Java.** You set up a callback by passing three arguments. The first is the name of the event you are interested in, the second is an instance of a class, the third is the name of the method you want to invoke. In this example we set up the StartEvent to invoke the myCallback method on me (which is an instance of Cone2). The myCallback method must of course be a valid method of Cone2 to avoid an error.

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

VTK can be installed as a Python package using `pip install vtk`, or you can build VTK from source with Python wrapping enabled. Once installed, VTK classes are available through the `vtkmodules` package:

```python
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import vtkRenderer
```

Creating your own Python scripts is a simple matter of using some of the example scripts as a starting point.

**User Methods in Python.** User methods can be set up by defining a function and then passing it as the argument to the AddObserver as shown below:

```python
def myCallback(obj, event):
    print("Starting to render")

ren1.AddObserver("StartEvent", myCallback)
```

## 3.3 Conversion Between Languages

As we have seen, VTK's core is implemented in C++ and then wrapped with the Java and Python programming languages. This means that you have a language choice when developing applications. Your choice will depend on which language you are most comfortable with, the nature of the application, and whether you need access to internal data structures and/or have special performance requirements. C++ offers several advantages over the other languages when you need to access internal data structure or require the highest-performing application possible. However, using C++ means the extra burden of the compile/link cycle, which often slows the software development process.

You may find yourself developing prototypes in an interpreted language such as Python and then converting them to C++. Or, you may discover example code (in the VTK distribution or from other users) that you wish to convert to your implementation language.

Converting VTK code from one language to another is fairly straightforward. Class names and method names remain the same across languages; what changes are the implementation details and GUI interface, if any. For example, the C++ statement

```cpp
anActor->GetProperty()->SetColor(red, green, blue);
```

in Java becomes

```java
anActor.GetProperty().SetColor(red, green, blue);
```

and in Python becomes

```python
anActor.GetProperty().SetColor(red, green, blue)
```

One major limitation you'll find is that some C++ applications cannot be converted to the other languages because of pointer manipulation. While it is always possible to get and set individual values from the wrapped languages, it is not always possible to obtain a raw pointer to quickly traverse and inspect or modify a large structure. If your application requires this level of data inspection or manipulation, you can either develop directly in C++ or extend VTK at the C++ level with your required high-performance classes, then use these new classes from your preferred interpreted language.

## 3.4 Building Desktop Applications with Qt

Qt is the standard toolkit for building polished desktop VTK applications with menus, toolbars, dockable panels, and multiple views. VTK provides dedicated Qt widgets that embed a VTK render window inside any Qt layout. Both C++ and Python (via PySide6) workflows are supported.

### C++ Qt + VTK

#### CMake Configuration

A Qt+VTK application requires the `GUISupportQt` VTK component and Qt's `Core` and `Widgets` modules. The `CMAKE_AUTOMOC` flag tells CMake to run Qt's meta-object compiler automatically, and `vtk_module_autoinit` ensures the correct VTK rendering backend is loaded:

```cmake
cmake_minimum_required(VERSION 3.12)
project(MyQtVTKApp)

find_package(VTK COMPONENTS CommonCore GUISupportQt)
find_package("Qt${VTK_QT_VERSION}" COMPONENTS Core Widgets)

set(CMAKE_AUTOMOC ON)

add_executable(MyQtVTKApp MyQtVTKApp.cxx)
target_link_libraries(MyQtVTKApp
  PRIVATE
    ${VTK_LIBRARIES}
    "Qt${VTK_QT_VERSION}::Core"
    "Qt${VTK_QT_VERSION}::Widgets")
vtk_module_autoinit(
  TARGETS MyQtVTKApp
  MODULES ${VTK_LIBRARIES})
```

The variable `VTK_QT_VERSION` is set by VTK's CMake configuration to match the Qt major version (5 or 6) that VTK was built against, so the same CMakeLists.txt works with either Qt version.

#### Minimal C++ Example

The following example creates a Qt main window with a VTK render widget as its central widget and renders a cone (see `examples/QtConeCxx/`):

```cpp
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
```

> **Important:** The call to `QSurfaceFormat::setDefaultFormat()` must come *before* the `QApplication` constructor. Setting it later can cause OpenGL context creation failures.
>
> **macOS note:** On macOS, the trackpad can generate spurious button-press events through touch input. Call `setAttribute(Qt::WA_AcceptTouchEvents, false)` on the VTK widget to prevent this.

#### Key Classes

- **`QVTKOpenGLNativeWidget`** -- A `QOpenGLWidget` subclass that hosts a VTK render window inside any Qt layout. This is the primary widget for embedding VTK views in Qt applications.
- **`vtkGenericOpenGLRenderWindow`** -- A render window designed to work with an externally managed OpenGL context. Qt creates and owns the OpenGL context, and this class lets VTK render into it. Must be used with `QVTKOpenGLNativeWidget`.
- **`vtkEventQtSlotConnect`** -- Bridges VTK's observer/command event system to Qt's signal/slot mechanism. Allows a Qt slot to be called in response to any VTK event (e.g., `ProgressEvent`, `PickEvent`).

### Python (PySide6) + VTK

VTK's Python package includes a Qt widget module that works with PySide6 out of the box -- no source build required.

#### Installation

```bash
pip install vtk PySide6
```

VTK detects PySide6 automatically at runtime.

#### Minimal Python Example

The following example embeds a VTK cone in a Qt window (see `examples/QtCone.py`):

```python
import sys

# Use QOpenGLWidget as the base class -- must be set before importing
# QVTKRenderWindowInteractor.
import vtkmodules.qt
vtkmodules.qt.QVTKRWIBase = "QOpenGLWidget"

from PySide6.QtWidgets import QApplication, QMainWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401 (load OpenGL2 backend)
import vtkmodules.vtkInteractionStyle  # noqa: F401 (load interactor styles)

app = QApplication(sys.argv)
window = QMainWindow()

# Create the VTK widget and place it in the main window.
vtk_widget = QVTKRenderWindowInteractor(window)
window.setCentralWidget(vtk_widget)

# Build a VTK pipeline.
cone = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
vtk_widget.GetRenderWindow().AddRenderer(renderer)

window.show()
vtk_widget.Initialize()
vtk_widget.Start()

sys.exit(app.exec())
```

The `QVTKRenderWindowInteractor` widget manages its own `vtkRenderWindow` and `vtkRenderWindowInteractor` internally. Setting `QVTKRWIBase` to `"QOpenGLWidget"` *before* importing the widget selects the `QOpenGLWidget`-backed implementation, which provides reliable rendering on all platforms. After calling `Initialize()` and `Start()` on the widget, hand control to Qt's event loop with `app.exec()`.
