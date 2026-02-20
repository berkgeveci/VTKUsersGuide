# Chapter 4: The Basics

The purpose of this chapter is to introduce you to some of VTK’s capabilities by way of a selected set of examples. Our focus will be on commonly used methods and objects, and combinations of objects. We will also introduce important concepts and useful applications. By no means are all of VTK’s features covered; this chapter is meant to give you a broad overview of what’s possible. You’ll want to refer to online documentation or class .h files to learn about other options each class might have. 

Most of the examples included here are implemented in the Tcl programming language. They could just as easily be implemented in C++, Java, and Python—the conversion process between the languages is straightforward. (See “Conversion Between Languages” on page37.) C++ does offer some advantages, mainly access and manipulation of data structures and pointers, and some examples reflect this by being implemented in the C++ language.

Each example presented here includes sample code and often a supplemental image. We indicate the name of the source code file (when one exists in the VTK source tree), so you will not have to enter it manually. We recommend that you run and understand the example and then experiment with object methods and parameters. You may also wish to try suggested alternative methods and/or classes. Often, the Visualization Toolkit offers several approaches to achieve similar results. Note also that the scripts are often modified from what’s found in the source code distribution. This is done to simplify concepts or remove extraneous code.

Learning an object-oriented system like VTK first requires understanding the programming abstraction, and then becoming familiar with the library of objects and their methods. We recommend that you review “System Architecture” on page19 for information about the programming abstraction. The examples in this chapter will then provide you with a good overview of the many VTK objects.

![Figure 4-1](images/Figure_4-1.png)

*Figure 4–1 Using Tcl/Tk to program an interpreted application.*

## 4.1 Creating Simple Models

The use of the Visualization Toolkit typically goes as follows: read/generate some data, filter it, render it, and interact with it. In this section, we’ll start by looking at ways to read and generate data.

There are two basic ways to obtain data. The data may exist in a file (or files, streams, etc.) that is read into the system, or the data may be procedurally generated (via an algorithm or mathematical expression). Recall that objects that initiate the processing of data in the visualization pipeline are called source objects (see Figure 3–5). Objects that generate data are called procedural (source) objects, and objects that read data are called reader (source) objects. 

### Procedural Source Object
We’ll start off by rendering a simple cylinder. The example code shown below (VTK/Examples/ Rendering/Tcl/Cylinder.tcl) demonstrates many basic concepts in the visualization pipeline and rendering engine. Refer to Figure 4–1 to see the results of running the script.

We begin the script by invoking a Tcl command to load the VTK package (package require vtk) and create a GUI interpreter (package require vtkinteraction) that lets you type commands at run-time. Also, we load vtktesting which defines a set of colors, one of which (tomato) is used later in the script.

```tcl
package require vtk
package require vtkinteraction
package require vtktesting
```
We then create a procedural source object: vtkCylinderSource. This source creates a polygonal representation of a cylinder. The output of the cylinder is set as the input to the vtkPolyDataMapper via the method SetInputConnection(). We create an actor (the object that is rendered) that refers to the mapper as its defining geometry. Notice the way objects are constructed in Tcl: we use the class name followed by the desired instance name.

```tcl
vtkCylinderSource cylinder
cylinder SetResolution 8
vtkPolyDataMapper cylinderMapper
cylinderMapper SetInputConnection [cylinder GetOutputPort]
vtkActor cylinderActor
cylinderActor SetMapper cylinderMapper
eval [cylinderActor GetProperty] SetColor $tomato
cylinderActor RotateX 30.0
cylinderActor RotateY -45.0
```

As a reminder of how similar a C++ implementation is to a Tcl (or other interpreted languages) implementation, the same code implemented in C++ is shown below, and can be found in VTK/Examples/ Rendering/Cxx/Cylinder.cxx.

```cpp
vtkCylinderSource *cylinder = vtkCylinderSource::New();
cylinder->SetResolution(8);
vtkPolyDataMapper *cylinderMapper = vtkPolyDataMapper::New();
cylinderMapper->SetInputConnection(cylinder->GetOutputPort());
vtkActor *cylinderActor = vtkActor::New();
cylinderActor->SetMapper(cylinderMapper);
cylinderActor->GetProperty()->SetColor(1.0000, 0.3882, 0.2784);
cylinderActor->RotateX(30.0);
cylinderActor->RotateY(-45.0);
```
Recall that source objects initiate the visualization pipeline, and mapper objects (or prop objects that include mapping functionality) terminate the pipeline, so in this example we have a pipeline consisting of two algorithms (i.e., a source and mapper). The VTK pipeline uses a lazy evaluation scheme, so even though the pipeline is connected, no generation or processing of data has yet occurred (since we have not yet requested the data).

Next we create graphics objects which will allow us to render the actor. The vtkRenderer instance ren1 coordinates the rendering process for a viewport of the render window renWin. The render window interactor iren is a 3D widget that allows us to manipulate the camera.

```tcl
# Create the graphics structure
vtkRenderer ren1
vtkRenderWindow renWin
renWin AddRenderer ren1
vtkRenderWindowInteractor iren
iren SetRenderWindow renWin
```
Notice that we’ve associated the renderer with the render window via the AddRenderer() method. We must also associate the actor with the renderer using the AddActor() method.

```tcl
# Add the actors to the renderer, set the background and size
ren1 AddActor cylinderActor
ren1 SetBackground 0.1 0.2 0.4
renWin SetSize 200 200
```
The SetBackground() method specifies the background color of the rendering window using RGB (red, green, blue) values between (0,1), and SetSize() specifies the window size in pixels. Finally, we conclude this example by associating the GUI interactor with the render window interactor’s userdefined method. (The user-defined method is invoked by pressing the u key when the mouse focus is in the rendering window. See “Using VTK Interactors” on page45. Also see “User Methods, Observers, and Commands” on page29) The Initialize() method begins the event loop, and the Tcl/Tk command wm withdraw . makes sure that the interpreter widget .vtkInteract is not visible when the application starts. 

```tcl
# Associate the “u” keypress with a UserEvent and start the event loop
iren AddObserver UserEvent {wm deiconify .vtkInteract}
iren Initialize

# suppress the tk window
wm withdraw .
```

When the script is run, the visualization pipeline will execute because the rendering engine will request data. (The window expose event will force the render window to render itself.) Only after the pipeline executes are the filters up-to-date with respect to the input data. If you desire, you can manually cause execution of the pipeline by invoking renWin Render.

After you get this example running, you might try a couple of things. First, use the interactor by mousing in the rendering window. Next, change the resolution of the cylinder object by invoking the `cylinder SetResolution 12`. You can do this by editing the example file and re-executing it, or by pressing u in the rendering window to bring up the interpreter GUI and typing the command there. Remember, if you are using the Tcl interactor popup, the changes you make are visible only after data is requested, so follow changes with a renWin Render command, or by mousing in the rendering window.

### Reader Source Object

This example is similar to the previous example except that we read a data file rather than procedurally generating the data. A stereo-lithography file is read (suffix .stl) that represents polygonal data using the binary STL data format. (Refer to Figure 4–2 and the Tcl script VTK/Examples/Rendering/ Tcl/CADPart.tcl.)

![Figure 4-2](images/Figure_4-2.png)

*Reader Source Object*

```tcl
vtkSTLReader part
part SetFileName \
$VTK_DATA_ROOT/Data/42400-IDGH.stl
vtkPolyDataMapper partMapper
partMapper SetInputConnection \
[part GetOutputPort]
vtkLODActor partActor
partActor SetMapper partMapper
```
Notice the use of the vtkLODActor. This actor changes its representation to maintain interactive performance. Its default behavior is to create a point cloud and wireframe, bounding-box outline to represent the intermediate and low-level representations. (See “Level-Of-Detail Actors” on page55 for more information.) The model used in this example is small enough that on most computers today you will only see the high-level representation (the full geometry of the model).

Many of the readers do not sense when the input file(s) change and re-execute. For example, if the file 42400-IDGH.stl changes, the pipeline will not re-execute. You can manually modify objects by invoking the Modified() method on them. This will cause the filter to re-execute, as well as all filters downstream of it.

The Visualization Toolkit has limited, built-in modeling capabilities. If you want to use VTK to edit and manipulate complex models (e.g., those created by a solid modeler or modeling tool), you’ll typically use a reader (see “Readers” on page239) to interface to the data. (Another option is importers, which are used to ingest entire scenes. See “Importers” on page245 for more information.)

## 4.2 Using VTK Interactors

Once you’ve visualized your data, you typically want to interact with it. The Visualization Toolkit offers several approaches to do this. The first approach is to use the built in class vtkRenderWindowInteractor. The second approach is to create your own interactor by specifying event bindings. And don’t forget that if you are using an interpreted language you can type commands at run-time. You may also wish to refer to “Picking” on page59 to see how to select data from the screen. (Note: Developers can also interface to a windowing system of their choice. See “Integrating With The Windowing System” on page421.)

### vtkRenderWindowInteractor
The simplest way to interact with your data is to instantiate vtkRenderWindowInteractor. This class responds to a pre-defined set of events and actions and provides a way to override the default actions. vtkRenderWindowInteractor allows you to control the camera and actors and offers two interaction styles: position sensitive (i.e., joystick mode) and motion sensitive (i.e., trackball mode). (More about interactor styles in the next section.)

vtkRenderWindowInteractor responds to the following events in the render window. (Remember that multiple renderers can draw into a rendering window and that the renderer draws into a viewport within the render window. Interactors support multiple renderers in a render window.)

- Keypress j / Keypress t — Toggle between joystick (position sensitive) and trackball (motion sensitive) styles. In joystick style, motion occurs continuously as long as a mouse button is pressed. In trackball style, motion occurs when the mouse button is pressed and the mouse pointer moves.
- Keypress c / Keypress a — Toggle between camera and actor (object) modes. In camera mode, mouse events affect the camera position and focal point. In object mode, mouse events affect the actor that is under the mouse pointer.
- Button 1 — Rotate the camera around its focal point (if camera mode) or rotate the actor around its origin (if actor mode). The rotation is in the direction defined from the center of the renderer’s viewport towards the mouse position. In joystick mode, the magnitude of the rotation is determined by the distance between the mouse and the center of the render window.
- Button 2 — Pan the camera (if camera mode) or translate the actor (if object mode). In joystick mode, the direction of pan or translation is from the center of the viewport towards the mouse position. In trackball mode, the direction of motion is the direction the mouse moves. (Note: With a 2-button mouse, pan is defined as <Shift>-Button 1.)
- Button 3 — Zoom the camera (if camera mode), or scale the actor (if object mode). Zoom in/ increase scale if the mouse position is in the top half of the viewport; zoom out/decrease scale if the mouse position is in the bottom half. In joystick mode, the amount of zoom is controlled by the distance of the mouse pointer from the horizontal centerline of the window.
- Keypress 3 — Toggle the render window into and out of stereo mode. By default, red-blue stereo pairs are created. Some systems support Crystal Eyes LCD stereo glasses; you have to invoke SetStereoTypeToCrystalEyes() on the rendering window.
- Keypress e/q — Exit or quit the application.
- Keypress f — Fly-to the point under the cursor. This sets the focal point and allows rotations around that point.
- Keypress p — Perform a pick operation. The render window interactor has an internal instance of vtkPropPicker that it uses to pick. See “Picking” on page59 for more information about picking.
- Keypress r — Reset the camera view along the current view direction. Centers the actors and moves the camera so that all actors are visible.
- Keypress s — Modify the representation of all actors so that they are surfaces.
- Keypress u — Invoke the user-defined method. Typically, this keypress will bring up an interactor that you can type commands into.
- Keypress w — Modify the representation of all actors so that they are wireframe.

The default interaction style is position sensitive (i.e., joystick style)—that is, it manipulates the camera or actor and renders continuously as long as a mouse button is pressed. If you don’t like the default behavior, you can change it or write your own. (See “vtkRenderWindow Interaction Style” on page421 for information about writing your own style.)

vtkRenderWindowInteractor has other useful features. Invoking LightFollowCameraOn() (the default behavior) causes the light position and focal point to be synchronized with the camera position and focal point (i.e., a “headlight” is created). Of course, this can be turned off with LightFollowCameraOff(). A callback that responds to the “u” keypress can be added with “AddObserver(UserEvent) method. It is also possible to set several pick-related methods. AddObserver(StartPickEvent) defines a method to be called prior to picking, and AddObserver(EndPickEvent) defines a method after the pick has been performed. (Please see “User Methods, Observers, and Commands” on page29 for more information on defining user methods.) You can also specify an instance of a subclass of vtkAbstractPicker to use via the SetPicker() method. (See “Picking” on page59.)

If you are using a prop that adjusts rendering quality based on desired interactivity, you may wish to set the desired frame rate via SetDesiredUpdateRate() in the interactor. Normally, this is handled automatically. (When the mouse buttons are activated, the desired update rate is increased; when the mouse button is released, the desired update rate is set back down.) Refer to “Level-Of-Detail Actors” on page55, the “vtkLODProp3D” on page57, and the chapter on “Volume Rendering” on page139 for further information on how props and their associated mappers may adjust render style to achieve a desired frame rate.

We’ve seen how to use vtkRenderWindowInteractor previously, here’s a recapitulation.
```tcl
vtkRenderWindowInteractor iren
iren SetRenderWindow renWin
iren AddObserver UserEvent {wm deiconify .vtkInteract}
```

### Interactor Styles
There are two distinctly different ways to control interaction style in VTK. The first is to use a subclass of vtkInteractorStyle, either one supplied with the system or one that you write. The second method is to add observers that watch for events on the vtkRenderWindowInteractor and define your own set of callbacks (or commands) to implement the style. (Note: 3D widgets are another, more complex way to interact with data in the scene. See “3D Widgets” on page72 for more information.)

### vtkInteractorStyle.
The class vtkRenderWindowInteractor can support different interaction styles. When you type “t” or “j” in the interactor (see the previous section) you are changing between trackball and joystick interaction styles. The way this works is that vtkRenderWindowInteractor translates window-system-specific events it receives (e.g., mouse button press, mouse motion, keyboard events) to VTK events such as MouseMoveEvent, StartEvent, and so on. (See “User Methods, Observers, and Commands” on page29 for related information.) Different styles then observe particular events and perform the action(s) appropriate to the event. To set the style, use the `vtkRenderWindowInteractor::SetInteractorStyle()` method. For example:

 
```tcl
vtkInteractorStyleFlight flightStyle
vtkRenderWindowInteractor iren
iren SetInteractorStyle flightStyle
```
(Note: When vtkRenderWindowInteractor is instantiated, a window-system specific render window interactor is actually instantiated. For example, on Unix systems the class vtkXRenderWindowInteractor is actually created and returned as an instance of vtkRenderWindowInteractor. On Windows, the class vtkWin32RenderWindowInteractor is instantiated.)

### Adding vtkRenderWindowInteractor Observers.
While a variety of interactor styles are available in VTK, you may prefer to create your own custom style to meet the needs of a particular application. In C++ the natural approach is to subclass vtkInteractorStyle. (See “vtkRenderWindow Interaction Style” on page421.) However, in an interpreted language (e.g., Tcl, Python, or Java), this is difficult to do. For interpreted languages the simplest approach is to use observers to define particular interaction bindings. (See “User Methods, Observers, and Commands” on page29.) The bindings can be managed in any language that VTK supports, including C++, Tcl, Python, and Java. An example of this is found in the Tcl code VTK/Examples/GUI/Tcl/CustomInteraction.tcl, which defines bindings for a simple Tcl application. Here’s an excerpt to give you an idea of what’s going on.

```tcl
vtkRenderWindowInteractor iren
iren SetInteractorStyle ""
iren SetRenderWindow renWin
# Add the observers to watch for particular events. These invoke # Tcl procedures.

set Rotating 0
set Panning 0
set Zooming 0
iren AddObserver LeftButtonPressEvent {global Rotating; set Rotating 1}
iren AddObserver LeftButtonReleaseEvent \
 {global Rotating; set Rotating 0}
iren AddObserver MiddleButtonPressEvent {global Panning; set Panning 1}
iren AddObserver MiddleButtonReleaseEvent \
 {global Panning; set Panning 0}

iren AddObserver RightButtonPressEvent {global Zooming; set Zooming 1}
iren AddObserver RightButtonReleaseEvent {global Zooming; set Zooming 0}
iren AddObserver MouseMoveEvent MouseMove
iren AddObserver KeyPressEvent Keypress
proc MouseMove {} {
  ...
  set xypos [iren GetEventPosition]
  set x [lindex $xypos 0]
  set y [lindex $xypos 1]
  ...
}
proc Keypress {} {
  set key [iren GetKeySym]
  if { $key == "e" } {
    vtkCommand DeleteAllObjects
    exit
  }
  ...
}
```
Note that a key step in this example is disabling the default interaction style by invoking SetInteractionStyle(). Observers are then added to watch for particular events which are tied to the appropriate Tcl procedures. This example is a simple way to add bindings from a Tcl script. If you would like to create a full GUI using Tcl/Tk, then use the vtkTkRenderWidget, and refer to “Tcl/Tk” on page433 for more details.

## 4.3 Filtering Data

The previous example pipelines consisted of a source and mapper object; the pipeline had no filters. In this section we show how to add a filter into the pipeline.

Filters are connected by using the SetInputConnection() and GetOutputPort() methods. For example, we can modify the script in “Reader Source Object” on page44 to shrink the polygons that make up the model. The script is shown below. (Only the pipeline and other pertinent objects are shown.) The complete script can be found at VTK/Examples/Rendering/Tcl/FilterCADPart.tcl.

```tcl
vtkSTLReader part
part SetFileName \
 "$VTK_DATA_ROOT/Data/42400-IDGH.stl"

vtkShrinkPolyData shrink
shrink SetInputConnection [part GetOutputPort]
shrink SetShrinkFactor 0.85

vtkPolyDataMapper partMapper
partMapper SetInputConnection \
  [shrink GetOutputPort]

vtkLODActor partActor
partActor SetMapper partMapper
```
As you can see, creating a visualization pipeline is simple. You need to select the right classes for the task at hand, make sure that the input and output type of connected filters are compatible, and
set the necessary instance variables. (Input and output types are
compatible when the output dataset type of a source or filter is acceptable as input to the next filter or mapper in the pipeline. The output dataset type must either match the input dataset type exactly or be a subclass of it.

![Figure 4-3](images/Figure_4-3.png)

*Figure 4–3 Filtering data. Here we use a filter to shrink the polygons forming the model towards their center.*) Visualization pipelines can contain their centroid. loops, but the output of a filter cannot be directly connected to its input.

## 4.4 Controlling The Camera

You may have noticed that in the proceeding scripts no cameras or lights were instantiated. If you’re familiar with 3D graphics, you know that lights and cameras are necessary to render objects. In VTK, if lights and cameras are not directly created, the renderer automatically instantiates them. Instantiating The Camera The following Tcl script shows how to instantiate and associate a camera with a renderer.

```tcl
vtkCamera cam1
cam1 SetClippingRange 0.0475572 2.37786
cam1 SetFocalPoint 0.052665 -0.129454 -0.0573973
cam1 SetPosition 0.327637 -0.116299 -0.256418
cam1 ComputeViewPlaneNormal
cam1 SetViewUp -0.0225386 0.999137 0.034901
ren1 SetActiveCamera cam1
```
Alternatively, if you wish to access a camera that already exists (for example, a camera that the renderer has automatically instantiated), in Tcl you would use

```tcl
set cam1 [ren1 GetActiveCamera]
$cam1 Zoom 1.4
```

Let’s review some of the camera methods that we’ve just introduced. SetClippingPlane() takes two arguments, the distance to the near and far clipping planes along the view plane normal. Recall that all graphics primitives not between these planes are eliminated during rendering, so you need to make sure the objects you want to see lie between the clipping planes. The FocalPoint and Position (in world coordinates) instance variables control the direction and position of the camera. ComputeViewPlaneNormal() resets the normal to the view plane based on the current position and focal point. (If the view plane normal is not perpendicular to the view plane you can get some interesting shearing effects.) Setting the ViewUp controls the “up” direction for the camera. Finally, the Zoom() method magnifies objects by changing the view angle (i.e., SetViewAngle()). You can also use the Dolly() method to move the camera in and out along the view plane normal to either enlarge or shrink the visible actors. 

### Simple Manipulation Methods
The methods described above are not always the most convenient ones for controlling the camera. If the camera is “looking at” the point you want (i.e., the focal point is set), you can use the Azimuth() and Elevation() methods to move the camera about the focal point.

```tcl
cam1 Azimuth 150
cam1 Elevation 60
```

These methods move the camera in a spherical coordinate system centered at the focal point by moving in the longitude direction (azimuth) and the latitude direction (elevation) by the angle (in degrees) given. These methods do not modify the view-up vector and depend on the view-up vector remaining constant. Note that there are singularities at the north and south poles — the view-up vector becomes parallel with the view plane normal. To avoid this, you can force the view-up vector to be orthogonal to the view vector by using OrthogonalizeViewUp(). However, this changes the camera coordinate system, so if you’re flying around an object with a natural horizon or view-up vector (such as terrain), camera manipulation is no longer natural with respect to the data.

### Controlling The View Direction
A common function of the camera is to generate a view from a particular direction. You can do this by invoking SetFocalPoint(), SetPosition(), and ComputeViewPlaneNormal() followed by invoking ResetCamera() on the renderer associated with the camera.

```tcl
vtkCamera cam1
cam1 SetFocalPoint 0 0 0
cam1 SetPosition 1 1 1
cam1 ComputeViewPlaneNormal
cam1 SetViewUp 1 0 0
cam1 OrthogonalizeViewUp

ren1 SetActiveCamera cam1
ren1 ResetCamera
```
The initial direction (view vector or view plane normal) is computed from the focal point and position of the camera, which, together with ComputeViewPlaneNormal(), defines the initial view vector. Optionally, you can specify an initial view-up vector and orthogonalize it with respect to the view vector. The ResetCamera() method then moves the camera along the view vector so that the renderer’s actors are all visible to the camera.

### Perspective Versus Orthogonal Views
In the previous examples, we have assumed that the camera is a perspective camera where a view angle controls the projection of the actors onto the view plane during the rendering process. Perspective projection, while generating more natural looking images, introduces distortion that can be undesirable in some applications. Orthogonal (or parallel) projection is an alternative projection method. In orthogonal projection, view rays are parallel, and objects are rendered without distance effects.

To set the camera to use orthogonal projection, use the vtkCamera::ParallelProjectionOn()
method. In parallel projection mode, the camera view angle no longer controls zoom. Instead, use the SetParallelScale() method to control the magnification of the actors.

### Saving/Restoring Camera State

Another common requirement of applications is the capability to save and restore camera state (i.e., recover a view). To save camera state, you’ll need to save (at a minimum) the clipping range, the focal point and position, and the view-up vector. You’ll also want to compute the view plane normal (as shown in the example in "Instantiating The Camera" on page49). Then, to recover camera state, simply instantiate a camera with the saved information, and assign it to the appropriate renderer (i.e., SetActiveCamera()).

In some cases you may need to store additional information. For example, if the camera view angle (or parallel scale) is set, you’ll need to save this. Or, if you are using the camera for stereo viewing, the EyeAngle and Stereo flags are required.

## 4.5 Controlling Lights

Lights are easier to control than cameras. The most frequently used methods are SetPosition(), SetFocalPoint(), and SetColor(). The position and focal point of the light control the direction in which the light points. The color of the light is expressed as an RGB vector. Also, lights can be turned on and off via the SwitchOn() and SwitchOff() methods, and the brightness of the light can be set with the SetIntensity() method.

By default, instances of vtkLight are directional lights. That is, the position and focal point define a vector parallel to which light rays travel, and the light source is assumed to be located at the infinity point. This means that the lighting on an object does not change if the focal point and position are translated identically.

Lights are associated with renderers as follows.

```tcl
vtkLight light
light SetColor 1 0 0
light SetFocalPoint [cam1 GetFocalPoint]
light SetPosition [cam1 GetPosition]
ren1 AddLight light
```
Here we’ve created a red headlight: a light located at the camera’s (cam1’s) position and pointing towards the camera’s focal point. This is a useful trick, and is used by the interactive renderer to position the light as the camera moves. (See “Using VTK Interactors” on page45.)

### Positional Lights
It is possible to create positional (i.e., spot lights) by using the PositionalOn() method. This method is used in conjunction with the SetConeAngle() method to control the spread of the spot. A cone angle of 180 degrees indicates that no spot light effects will be applied (i.e., no truncated light cone), only the effects of position.

## 4.6 Controlling 3D Props

Objects in VTK that are to be drawn in the render window are generically known as “props.” (The word prop comes from the vocabulary of theater—a prop is something that appears on stage.) There are several different types of props including vtkProp3D and vtkActor. vtkProp3D is an abstract superclass for those types of props existing in 3D space. The class vtkActor is a type of vtkProp3D whose geometry is defined by analytic primitives such as polygons and lines. 

### Specifying the Position of a vtkProp3D
We have already seen how to use cameras to move around an object; alternatively, we can also hold the camera steady and transform the props. The following methods can be used to define the position of a vtkProp3D (and its subclasses).

- SetPosition(x,y,z) — Specify the position of the vtkProp3D in world coordinates.
- AddPosition(deltaX,deltaY,deltaZ) — Translate the prop by the specified amount along each of the x, y, and z axes.
- RotateX(theta), RotateY(theta), RotateZ(theta) — Rotate the prop by theta degrees around the x, y, z coordinate axes, respectively.
- SetOrientation(x,y,z) — Set the orientation of the prop by rotating about the z axis, then about the x axis, and then about the y axis.
- AddOrientation(a1,a2,a3) — Add to the current orientation of the prop.
- RotateWXYZ(theta,x,y,z) — Rotate the prop by theta degress around the x-y-z vector defined.
- SetScale(sx,sy,sz) — Scale the prop in the x, y, z axes coordinate directions.
- SetOrigin(x,y,z) — Specify the origin of the prop. The origin is the point around which rotations and scaling occur.

These methods work together in complex ways to control the resulting transformation matrix. The most important thing to remember is that the operations listed above are applied in a particular order, and the order of application dramatically affects the resulting actor position. The order used in VTK to apply these transformations is as follows:
1. Shift to Origin
2. Scale
3. Rotate Y
4. Rotate X
5. Rotate Z
6. Shift from Origin
7. Translate

![Figure 4-4](images/Figure_4-4.png)

*Figure 4–4 The effects of applying rotation in different order. On the left, first an x rotation followed by a y rotation; on the right, first a y rotation followed by an x rotation.*

The shift to and from the origin is a negative and positive translation of the Origin value, respectively. The net translation is given by the Position value of the vtkProp3D. The most confusing part of these transformations are the rotations. For example, performing an x rotation followed by a y rotation gives very different results than the operations applied in reverse order (see Figure 4–4). For more information about actor transformation, please refer to the Visualization Toolkit text.

In the next section we describe a variety of vtkProp3D’s—of which the most widely used class in VTK is called vtkActor. Later on (see “Controlling vtkActor2D” on page62) we will examine 2D props (i.e., vtkActor2D) which tend to be used for annotation and other 2D operations.

### Actors

An actor is the most common type of vtkProp3D. Like other concrete subclasses of vtkProp3D, vtkActor serves to group rendering attributes such as surface properties (e.g., ambient, diffuse, and specular color), representation (e.g., surface or wireframe), texture maps, and/or a geometric definition (a mapper). 

**Defining Geometry.** As we have seen in previous examples, the geometry of an actor is specified with the SetMapper() method:

```tcl
vtkPolyDataMapper mapper
mapper SetInputConnection [aFilter GetOutputPort]
vtkActor anActor
anActor SetMapper mapper
```
In this case mapper is of type vtkPolyDataMapper, which renders geometry using analytic primitives such as points, lines, polygons, and triangle strips. The mapper terminates the visualization pipeline and serves as the bridge between the visualization subsystem and the graphics subsystem.

**Actor Properties.** Actors refer to an instance of vtkProperty, which in turn controls the appearance of the actor. Probably the most used property is actor color, which we will describe in the next section. Other important features of the property are its representation (points, wireframe, or surface), its shading method (either flat or Gouraud shaded), the actor’s opacity (relative transparency), and the ambient, diffuse, and specular color and related coefficients. The following script shows how to set some of these instance variables.

```tcl
vtkActor anActor
anActor SetMapper mapper
[anActor GetProperty] SetOpacity 0.25
[anActor GetProperty] SetAmbient 0.5
[anActor GetProperty] SetDiffuse 0.6
[anActor GetProperty] SetSpecular 1.0
[anActor GetProperty] SetSpecularPower 10.0
```
Notice how we dereference the actor’s property via the GetProperty() method. Alternatively, we can create a property and assign it to the actor.

```tcl
vtkProperty prop
prop SetOpacity 0.25
prop SetAmbient 0.5
prop SetDiffuse 0.6
prop SetSpecular 1.0
prop SetSpecularPower 10.0
vtkActor anActor
anActor SetMapper mapper
anActor SetProperty prop
```
The advantage of the latter method is that we can control the properties of several actors by assigning each the same property.

**Actor Color.** Color is perhaps the most important property applied to an actor. The simplest procedure for controlling this property is the SetColor() method, used to set the red, green, and blue (RGB) values of the actor. Each value ranges from zero to one.

```tcl
[anActor GetProperty] SetColor 0.1 0.2 0.4
```
Alternatively, you can set the ambient, diffuse, and specular colors separately.

```tcl
vtkActor anActor
anActor SetMapper mapper
[anActor GetProperty] SetAmbientColor .1 .1 .1
[anActor GetProperty] SetDiffuseColor .1 .2 .4
[anActor GetProperty] SetSpecularColor 1 1 1
```
In this example we’ve set the ambient color to a dark gray, the diffuse color to a shade of blue, and the specular color to white. (Note: The SetColor() method sets the ambient, diffuse, and specular colors to the color specified.) 

**Important:** The color set in the actor’s property only takes effect if there is no scalar data available to the actor’s mapper. By default, the mapper’s input scalar data colors the actor, and the actor’s color is ignored. To ignore the scalar data, use the method ScalarVisibilityOff() as shown in the Tcl script below.

```tcl
vtkPolyDataMapper planeMapper
planeMapper SetInputConnection [CompPlane GetOutputPort]
planeMapper ScalarVisibilityOff

vtkActor planeActor
planeActor SetMapper planeMapper
[planeActor GetProperty] SetRepresentationToWireframe
[planeActor GetProperty] SetColor 0 0 0
```
**Actor Transparency.** Many times it is useful to adjust transparency (or opacity) of an actor. For example, if you wish to show internal organs surrounded by the skin of a patient, adjusting the transparency of the skin allows the user to see the organs in relation to the skin. Use the vtkProperty::SetOpacity() method as follows.
```tcl
vtkActor popActor
popActor SetMapper popMapper
[popActor GetProperty] SetOpacity 0.3
[popActor GetProperty] SetColor .9 .9 .9
```
Please note that transparency is implemented in the rendering library using an α-blending process. This process requires that polygons are rendered in the correct order. In practice, this is very difficult to achieve, especially if you have multiple transparent actors. To order polygons, you should add transparent actors to the end of renderer’s list of actors (i.e., add them last). Also, you can use the filter vtkDepthSortPolyData to sort polygons along the view vector. Please see VTK/Examples/ VisualizationAlgorithms/Tcl/DepthSort.tcl for an example using this filter. For more information on this topic see "Translucent polygonal geometry" on page 79. 

**Miscellaneous Features.** Actors have several other important features. You can control whether an actor is visible with the VisibilityOn() and VisibilityOff() methods. If you don’t want to pick an actor during a picking operation, use the PickableOff() method. (See "Picking" on page59 for more information about picking.) Actors also have a pick event that can be invoked when they are picked. Additionally you can get the axis-aligned bounding box of actor with the GetBounds() method.

### Level-Of-Detail Actors
One major problem with graphics systems is that they often become too slow for interactive use. To handle this problem, VTK uses level-of-detail actors to achieve acceptable rendering performance at the cost of lower-resolution representations.

In "Reader Source Object" on page 44 we saw how to use a vtkLODActor. Basically, the simplest way to use vtkLODActor is to replace instances of vtkActor with instances of vtkLODActor. In addition, you can control the representation of the levels of detail. The default behavior of vtkLOD-
Actor is to create two additional, lower-resolution models from the original mapper. The first is a point cloud, sampled from the points defining the mapper’s input. You can control the number of
points in the cloud as follows. (The default is 150 points.)

```tcl
vtkLODActor dotActor
dotActor SetMapper dotMapper
dotActor SetNumberOfCloudPoints 1000
```
The lowest resolution model is a bounding box of the actor. Additional levels of detail can be added using the AddLODMapper() method. They do not have to be added in order of complexity.

To control the level-of-detail selected by the actor during rendering, you can set the desired frame rate in the rendering window:

```tcl
vtkRenderWindow renWin
renWin SetDesiredUpdateRate 5.0
```
which translates into five frames per second. The vtkLODActor will automatically select the appropriate level-of-detail to yield the requested rate. (Note: The interactor widgets such as vtkRenderWindowInteractor automatically control the desired update rate. They typically set the frame rate very low when a mouse button is released, and increase the rate when a mouse button is pressed. This gives the pleasing effect of low-resolution/high frame rate models with camera motion, and high-resolution/low frame rate when the camera stops. If you would like more control over the levels-of-detail, see “vtkLODProp3D” on page57. vtkLODProp3D allow you to specifically set each level.) 

### Assemblies

Actors are often grouped in hierarchal assemblies so that the motion of one actor affects the position of other actors. For example, a robot arm might consist of an upper arm, forearm, wrist, and end effector, all connected via joints. When the upper arm rotates around the shoulder joint, we expect the rest of the arm to move with it. This behavior is implemented using assemblies, which are a type of (subclass of) vtkActor. The following script shows how it’s done (from VTK/Examples/ Rendering/Tcl/assembly.tcl). 

```tcl
# create four parts: a top level assembly and three primitives
vtkSphereSource sphere
vtkPolyDataMapper sphereMapper
sphereMapper SetInputConnection [sphere GetOutputPort]
vtkActor sphereActor
sphereActor SetMapper sphereMapper
sphereActor SetOrigin 2 1 3
sphereActor RotateY 6
sphereActor SetPosition 2.25 0 0
[sphereActor GetProperty] SetColor 1 0 1
vtkCubeSource cube
vtkPolyDataMapper cubeMapper
cubeMapper SetInputConnection [cube GetOutputPort]
vtkActor cubeActor
cubeActor SetMapper cubeMapper
cubeActor SetPosition 0.0 .25 0
[cubeActor GetProperty] SetColor 0 0 1
vtkConeSource cone
vtkPolyDataMapper coneMapper
coneMapper SetInputConnection [cone GetOutputPort]
vtkActor coneActor
coneActor SetMapper coneMapper
coneActor SetPosition 0 0 .25
[coneActor GetProperty] SetColor 0 1 0
vtkCylinderSource cylinder
vtkPolyDataMapper cylinderMapper
CylinderMapper SetInputConnection [cylinder GetOutputPort]
vtkActor cylinderActor
cylinderActor SetMapper cylinderMapper
[cylinderActor GetProperty] SetColor 1 0 0
vtkAssembly assembly
assembly AddPart cylinderActor
assembly AddPart sphereActor
assembly AddPart cubeActor
assembly AddPart coneActor
assembly SetOrigin 5 10 15
assembly AddPosition 5 0 0
assembly RotateX 15
# Add the actors to the renderer, set the background and size
ren1 AddActor assembly
ren1 AddActor coneActor
```
Notice how we use vtkAssembly’s AddPart() method to build the hierarchies. Assemblies can be nested arbitrarily deeply as long as there are not any self-referencing cycles. Note that vtkAssembly is a subclass of vtkProp3D, so it has no notion of properties or of an associated mapper. Therefore, the leaf nodes of the vtkAssembly hierarchy must carry information about material properties (color, etc.) and any associated geometry. Actors may also be used by more than one assembly (notice howconeActor is used in the assembly and as an actor). Also, the renderer’s AddActor() method is used to associate the top level of the assembly with the renderer; those actors at lower levels in the assembly hierarchy do not need to be added to the renderer since they are recursively rendered.

You may be wondering how to distinguish the use of an actor relative to its context if an actor is used in more than one assembly, or is mixed with an assembly as in the example above. (This is particularly important in activities like picking, where the user may need to know which vtkProp was picked as well as the context in which it was picked.) We address this issue along with the introduction of the class vtkAssemblyPath, which is an ordered list of vtkProps with associated transformation matrices (if any), in detail in "Picking" on page 59.

### Volumes

The class vtkVolume is used for volume rendering. It is analogous to the class vtkActor. Like vtkActor, vtkVolume inherits methods from vtkProp3D to position and orient the volume. vtkVolume has an associated property object, in this case a vtkVolumeProperty. Please see "Volume Rendering" on page 116 for a thorough description of the use of vtkVolume and a description of volume rendering.

### vtkLODProp3D
The vtkLODProp3D class is similar to vtkLODActor (see “Level-Of-Detail Actors” on page55) in that it uses different representations of itself in order to achieve interactive frame rates. Unlike vtkLODActor, vtkLODProp3D supports both volume rendering and surface rendering. This means that you can use vtkLODProp3D in volume rendering applications to achieve interactive frame rates. The following example shows how to use the class.

```tcl
vtkLODProp3D lod
set level1 [lod AddLOD volumeMapper volumeProperty2 0.0]
set level2 [lod AddLOD volumeMapper volumeProperty 0.0]
set level3 [lod AddLOD probeMapper_hres probeProperty 0.0]
set level4 [lod AddLOD probeMapper_lres probeProperty 0.0]
set level5 [lod AddLOD outlineMapper outlineProperty 0.0]
```
Basically, you create different mappers each corresponding to a different rendering complexity, and add the mappers to the vtkLODProp3D. The AddLOD() method accepts either volume or geometric mappers and optionally a texture map and/or property object. (There are different signatures for this method depending on what information you wish to provide.) The last value in the field is an estimated time to render. Typically you set it to zero to indicate that there is no initial estimate. The method returns an integer id that can be used to access the appropriate LOD (i.e., to select a level or delete it). 

vtkLODProp3D measures the time it takes to render each LOD and sorts them appropriately. Then, depending on the render window’s desired update rate, vtkLODProp3D selects the appropriate level to render. See “Using a vtkLODProp3D to Improve Performance” on page135 for more information.

## 4.7 Using Texture

Texture mapping is a powerful graphics tool for creating realistic and compelling visualizations. The basic idea behind 2D texture mapping is that images can be “pasted” onto a surface during the rendering process, thereby creating richer and more detailed images. Texture mapping requires three pieces of information: a surface to apply the texture to; a texture map, which in VTK is a vtkImageData dataset (i.e., a 2D image); and texture coordinates, which control the positioning of the texture on the surface.

The following example (Figure 4–5) demonstrates the use of texture mapping (see VTK/Examples/Rendering/Tcl/ TPlane.tcl). Notice that the texture map (of class vtkTexture) is associated with the actor, and the texture coordinates come from the plane (the texture coordinates are generated by vtkPlaneSource when the plane is created). # load in the texture map

![Figure 4-5](images/Figure_4-5.png)

*Figure 4–5 Texture map on  plane*

```tcl
vtkBMPReader bmpReader
bmpReader SetFileName \
  "$VTK_DATA_ROOT/Data/masonry.bmp"

vtkTexture atext
atext SetInputConnection [bmpReader GetOutputPort]
atext InterpolateOn
# create a plane source and actor
vtkPlaneSource plane
vtkPolyDataMapper planeMapper
planeMapper SetInputConnection [plane GetOutputPort]
vtkActor planeActor
planeActor SetMapper planeMapper
planeActor SetTexture atext
```

Often times texture coordinates are not available, usually because they are not generated in the pipeline. If you need to generate texture coordinates, refer to “Generate Texture Coordinates” on page111. Although some older graphics card have limitations on the dimensions of textures (e.g. they must be a power of two and less than 1024 on a side), VTK allows arbitrarily sized textures. At run time, VTK will query the graphics system to determine its capabilities, and will automatically resample your texture to meet the card's requirements.

## 4.8 Picking

Picking is a common visualization task. Picking is used to select data and actors or to query underlying data values. A pick is made when a display position (i.e., pixel coordinate) is selected and used to invoke vtkAbstractPicker’s Pick() method. Depending on the type of picking class, the information returned from the pick may be as simple as an x-y-z global coordinate, or it may include cell ids, point ids, cell parametric coordinates, the instance of vtkProp that was picked, and/or assembly paths. The syntax of the pick method is as follows.

```
Pick(selectionX, selectionY, selectionZ, Renderer)
```
Notice that the pick method requires a renderer. The actors associated with the renderer are the candidates for pick selection. Also, selectionZ is typically set to 0.0—it relates to depth in the z-buffer. (In typical usage, this method is not invoked directly. Rather the user interacts with the class vtkRenderWindowInteractor which manages the pick. In this case, the user would control the picking process by assigning an instance of a picking class to the vtkRenderWindowInteractor, as we will see in a later example.)

The Visualization Toolkit supports several types of pickers of varying functionality and performance. (Please see Figure 19–16 which is an illustration of the picking class hierarchy.) The class vtkAbstractPicker serves as the base class for all pickers. It defines a minimal API which allows the user to retrieve the pick position (in global coordinates) using the GetPickPosition() method.

Two direct subclasses of vtkAbstractPicker exist. The first, vtkWorldPointPicker, is a fast (usually in hardware) picking class that uses the z-buffer to return the x-y-z global pick position. However, no other information (about the vtkProp that was picked, etc.) is returned. The class vtkAbstractPropPicker is another direct subclass of vtkAbstractPicker. It defines an API for pickers that can pick an instance of vtkProp. There are several convenience methods in this class to allow querying for the
return type of a pick.
- GetProp() — Return the instance of vtkProp that was picked. If anything at all was picked, then this method will return a pointer to the instance of vtkProp, otherwise NULL is returned.
- GetProp3D() — If an instance of vtkProp3D was picked, return a pointer to the instance of vtkProp3D.
- GetActor2D() — If an instance of vtkActor2D was picked, return a pointer to the instance of vtkActor2D.
- GetActor() — If an instance of vtkActor was picked, return a pointer to the instance of vtkActor.
- GetVolume() — If an instance of vtkVolume was picked, return a pointer to the instance of vtkVolume.
- GetAssembly() — If an instance of vtkAssembly was picked, return a pointer to the instance of vtkAssembly.
- GetPropAssembly() — If an instance of vtkPropAssembly was picked, return a pointer to the instance of vtkPropAssembly.

A word of caution about these methods. The class (and its subclass) return information about the top level of the assembly path that was picked. So if you have an assembly whose top level is of type vtkAssembly, and whose leaf node is of type vtkActor, the method GetAssembly() will return a pointer to the instance of vtkAssembly, while the GetActor() method will return a NULL pointer (i.e., no vtkActor). If you have a complex scene that includes assemblies, actors, and other types of props, the safest course to take is to use the GetProp() method to determine whether anything at all was picked, and then use GetPath().

There are three direct subclasses of vtkAbstractPropPicker. These are vtkPropPicker, vtkAreaPicker, and vtkPicker. vtkPropPicker uses hardware picking to determine the instance of vtkProp that was picked, as well as the pick position (in global coordinates). vtkPropPicker is generally faster than all other decendents of vtkAbstractPropPicker but it cannot return information detailed information about what was picked.

vtkAreaPicker and its hardware picking based descendent vtkRenderedAreaPicker are similarly incapable of determining detailed information, as all three exist for the purpose of identifying entire objects that are shown on screen. The AreaPicker classes differ from all other pickers in that they can determine what lies begin an entire rectangular region of pixels on the screen instead of only what lies behind a single pixel. These classes have an AreaPick(x_min, y_min, x_max, y_max, Renderer) method that can be called in addition to the standard Pick(x,y,z, Renderer) method. If you need detailed information, for example specific cells and points or information about what lies behind an area, review the following picker explanations below.

vtkPicker is a software-based picker that selects vtkProp’s based on their bounding box. Its pick method fires a ray from the camera position through the selection point and intersects the bounding box of each prop 3D; of course, more than one prop 3D may be picked. The "closest" prop 3D in terms of its bounding box intersection point along the ray is returned. (The GetProp3Ds() method can be used to get all prop 3D’s whose bounding box was intersected.) vtkPicker is fairly fast but cannot generate a single unique pick.

vtkPicker has two subclasses that can be used to retrieve more detailed information about what was picked (e.g., point ids, cell ids, etc.) vtkPointPicker selects a point and returns the point id and coordinates. It operates by firing a ray from the camera position through the selection point, and projecting those points that lie within Tolerance onto the ray. The projected point closest to the camera position is selected, along with its associated actor. (Note: The instance variable Tolerance is expressed as a fraction of the renderer window’s diagonal length.) vtkPointPicker is slower than vtkPicker but faster than vtkCellPicker. It cannot always return a unique pick because of the tolerances involved.

vtkCellPicker selects a cell and returns information about the intersection point (cell id, global coordinates, and parametric cell coordinates). It operates by firing a ray and intersecting all cells in each actor’s underlying geometry, determining if each intersects this ray, within a certain specified tolerance. The cell closest to the camera position along the specified ray is selected, along with its associated actor. (Note: The instance variable Tolerance is used during intersection calculation, and you may need to experiment with its value to get satisfactory behavior.) vtkCellPicker is the slowest
of all the pickers, but provides the most information. It will generate a unique pick within the tolerance specified.

Several events are defined to interact with the pick operation. The picker invokes StartPickEvent prior to executing the pick operation. EndPickEvent is invoked after the pick operation is complete. The picker’s PickEvent and the actor’s PickEvent are invoked each time an actor is picked. (Note that no PickEvent is invoked when using vtkWorldPointPicker.)

### vtkAssemblyPath
An understanding of the class vtkAssemblyPath is essential if you are to perform picking in a scene with different types of vtkProp’s, especially if the scene contains instances of vtkAssembly. vtkAssemblyPath is simply an ordered list of vtkAssemblyNode’s, where each node contains a pointer to a vtkProp, as well as an optional vtkMatrix4x4. The order of the list is important: the start of the list represents the root, or top level node in an assembly hierarchy, while the end of the list represents a leaf node in an assembly hierarchy. The ordering of the nodes also affects the associated matrix. Each matrix is a concatenation of the node’s vtkProp’s matrix with the previous matrix in the list. Thus, for a given vtkAssemblyNode, the associated vtkMatrix4x4 represents the position and orientation of the vtkProp (assuming that the vtkProp is initially untransformed).

### Example
Typically, picking is automatically managed by vtkRenderWindowInteractor (see “Using VTK Interactors” on page45 for more information about interactors). For example, when pressing the p key, vtkRenderWindowInteractor invokes a pick with its internal instance of vtkPropPicker. You can then ask the vtkRenderWindowInteractor for its picker, and gather the information you need. You can also specify a particular vtkAbstractPicker instance for vtkRenderWindowInteractor to use, as the following script illustrates. The results on a sample data set are shown in Figure 4–6. The script for this example can be found in VTK/Examples/Annotation/Tcl/annotatePick.tcl.

![Figure 4-6](images/Figure_4-6.png)

*Figure 4–6 Annotating a pick operation.*

```tcl
vtkCellPicker picker
picker AddObserver EndPickEvent annotatePick
vtkTextMapper textMapper
set tprop [textMapper GetTextProperty]
$tprop SetFontFamilyToArial
$tprop SetFontSize 10
$tprop BoldOn
$tprop ShadowOn
$tprop SetColor 1 0 0
vtkActor2D textActor
textActor VisibilityOff
textActor SetMapper textMapper
vtkRenderWindowInteractor iren
iren SetRenderWindow renWin
iren SetPicker picker
proc annotatePick {} {
if { [picker GetCellId] < 0 } {
  textActor VisibilityOff
} else {
  set selPt [picker GetSelectionPoint]
  set x [lindex $selPt 0]
  set y [lindex $selPt 1]
  set pickPos [picker GetPickPosition]
  set xp [lindex $pickPos 0]
  set yp [lindex $pickPos 1]
  set zp [lindex $pickPos 2]
  textMapper SetInput "($xp, $yp, $zp)"
  textActor SetPosition $x $y
  textActor VisibilityOn

renWin Render
}
picker Pick 85 126 0 ren1
```
This example uses a vtkTextMapper to draw the world coordinate of the pick on the screen. (See "Text Annotation" on page 63 for more information.) Notice that we register the EndPickEvent to
perform setup after the pick occurs. The method is configured to invoke the annotatePick() procedure when picking is complete.

## 4.9 vtkCoordinate and Coordinate Systems

The Visualization Toolkit supports several different coordinate systems, and the class vtkCoordinate manages transformations between them. The supported coordinate systems are as follows.

- DISPLAY — x-y pixel values in the (rendering) window. (Note that vtkRenderWindow is a subclass of vtkWindow). The origin is the lower-left corner (which is true for all 2D coordinate systems described below).
- NORMALIZED DISPLAY — x-y (0,1) normalized values in the window.
- VIEWPORT — x-y pixel values in the viewport (or renderer — a subclass of vtkViewport)
- NORMALIZED VIEWPORT — x-y (0,1) normalized values in viewport
- VIEW — x-y-z (-1,1) values in camera coordinates (z is depth)
- WORLD — x-y-z global coordinate value
- USERDEFINED - x-y-z in user-defined space. The user must provide a transformation method for user defined coordinate systems. See vtkCoordinate for more information.

The class vtkCoordinate can be used to transform between coordinate systems and can be linked together to form “relative” or “offset” coordinate values. Refer to the next section for an example of using vtkCoordinate in an application.

## 4.10 Controlling vtkActor2D

vtkActor2D is analogous to vtkActor except that it draws on the overlay plane and does not have a 4x4 transformation matrix associated with it. Like vtkActor, vtkActor2D refers to a mapper (vtkMapper2D) and a property object (vtkProperty2D). The most difficult part when working with vtkActor2D is positioning it. To do that, the class vtkCoordinate is used. (See previous section, “vtkCoordinate and Coordinate Systems”.) The following script shows how to use the vtkCoordinate object.

![Figure 4-7](images/Figure_4-7.png)

*Figure 4–7 2D (left) and 3D (right) annotation.*

```tcl
vtkActor2D bannerActor
bannerActor SetMapper banner
[bannerActor GetProperty] SetColor 0 1 0
[bannerActor GetPositionCoordinate]
       SetCoordinateSystemToNormalizedDisplay
[bannerActor GetPositionCoordinate] SetValue 0.5 0.5
```
What’s done in this script is to access the coordinate object and define it’s coordinate system. Then the appropriate value is set for that coordinate system. In this script a normalized display coordinate system is used, so display coordinates range from zero to one, and the values (0.5,0.5) are set to position the vtkActor2D in the middle of the rendering window. vtkActor2D also provides a convenience method, SetDisplayPosition(), that sets the coordinate system to DISPLAY and uses the input parameters to set the vtkActor2D’s position using pixel offsets in the render window. The example in the following section shows how the method is used.

## 4.11 Text Annotation

The Visualization Toolkit offers two ways to annotate images. First, text (and graphics) can be rendered on top of the underlying 3D graphics window (often referred to as rendering in the overlay plane). Second, text can be created as 3D polygonal data and transformed and displayed as any other 3D graphics object. We refer to this as 2D and 3D annotation, respectively. See Figure 4–7 to see the difference.

### 2DText Annotation

To use 2D text annotation, we employ 2D actors (vtkActor2D and its subclasses such as vtkScaledTextActor) and mappers (vtkMapper2D and subclasses such as vtkTextMapper). 2D actors and mappers are similar to their 3D counterparts except that they render in the overlay plane on top of underlying graphics or images. Here’s an example Tcl script found in VTK/Examples/ Annotation/Tcl/TestText.tcl; the results are shown on the left side of Figure 4–7.

```tcl
vtkSphereSource sphere
vtkPolyDataMapper sphereMapper
sphereMapper SetInputConnection [sphere GetOutputPort]

sphereMapper GlobalImmediateModeRenderingOn
vtkLODActor sphereActor
sphereActor SetMapper sphereMapper
vtkTextActor textActor
textActor SetTextScaleModeToProp
textActor SetDisplayPosition 90 50
textActor SetInput "This is a sphere"
# Specify an initial size
[textActor GetPosition2Coordinate] \
  SetCoordinateSystemToNormalizedViewport
  [textActor GetPosition2Coordinate] SetValue 0.6 0.1
set tprop [textActor GetTextProperty]
$tprop SetFontSize 18
$tprop SetFontFamilyToArial
$tprop SetJustificationToCentered
$tprop BoldOn
$tprop ItalicOn
$tprop ShadowOn
$tprop SetColor 0 0 1
# Create the RenderWindow, Renderer and both Actors

vtkRenderer ren1
vtkRenderWindow renWin
renWin AddRenderer ren1
vtkRenderWindowInteractor iren
iren SetRenderWindow renWin
# Add the actors to the renderer

ren1 AddViewProp textActor
ren1 sphereActor
```
Instances of the class vtkTextProperty allow you to control font family (Arial, Courier, or Times), set
text color, turn bolding and italics on and off, and apply font shadowing. (Shadowing is used to make the font more readable when placed on top of complex background images.) The position and color of the text is controlled by the associated vtkActor2D. (In this example, the position is set using display or pixel coordinates.) vtkTextProperty also supports justification (vertical and horizontal) and multi-line text. Use the methods SetJustificationToLeft(), SetJustificationToCentered(), and SetJustificationToRight() to control the horizontal justification. Use the methods SetVerticalJustificationToBottom(), SetVerticalJustificationToCentered(), and SetVerticalJustificationToTop() to control vertical justification. By default, text is left-bottom justified. To insert multi-line text, use the \n character embedded in the text. The example in Figure 4–8 demonstrates justification and multi-line text (taken from VTK/Examples/Annotation/Tcl/multiLineText.tcl). The essence of the example is shown below.

![Figure 4-8](images/Figure_4-8.png)

*Figure 4–8 Justification and use of multi-line text. Use the \n character embedded in the text string to generate line breaks. Both vertical and horizontal justification is supported.*

```tcl
vtkTextMapper textMapperL
textMapperL SetInput "This is\nmulti-line\ntext output\n(left-top)"
set tprop [textMapperL GetTextProperty]
$tprop ShallowCopy multiLineTextProp
$tprop SetJustificationToLeft
$tprop SetVerticalJustificationToTop
$tprop SetColor 1 0 0
vtkActor2D textActorL
textActorL SetMapper textMapperL
[textActorL GetPositionCoordinate] \
  SetCoordinateSystemToNormalizedDisplay
[textActorL GetPositionCoordinate] SetValue 0.05 0.5
```
Note the use of the vtkCoordinate object (obtained by invoking the GetPositionCoordinate() method) to control the position of the actor in the normalized display coordinate system. See the section "vtkCoordinate and Coordinate Systems" on page 62 for more information about placing annotation. 

### 3D Text Annotation and vtkFollower
3D text annotation is implemented using vtkVectorText to create a polygonal representation of a text string, which is then appropriately positioned in the scene. One useful class for positioning 3D text is vtkFollower. This class is a type of actor that always faces the renderer’s active camera, thereby insuring that the text is readable. This Tcl script found in VTK/Examples/Annotation/Tcl/ textOrigin.tcl shows how to do this (Figure 4–7). The example creates an axes and labels the origin using an instance of vtkVectorText in combination with a vtkFollower.

```tcl
vtkAxes axes
axes SetOrigin 0 0 0
vtkPolyDataMapper axesMapper
axesMapper SetInputConnection [axes GetOutputPort]
vtkActor axesActor
axesActor SetMapper axesMapper
vtkVectorText atext
atext SetText "Origin"
vtkPolyDataMapper textMapper
textMapper SetInputConnection [atext GetOutputPort]
vtkFollower textActor
textActor SetMapper textMapper
textActor SetScale 0.2 0.2 0.2
textActor AddPosition 0 -0.1 0
...etc...after rendering...
textActor SetCamera [ren1 GetActiveCamera]
```
As the camera moves around the axes, the follower will orient itself to face the camera. (Try this by mousing in the rendering window to move the camera.)

## 4.12 Special Plotting Classes

The Visualization Toolkit provides several composite classes that perform supplemental plotting operations. These include the ability to plot scalar bars, perform simple x-y plotting, and place flying axes for 3D spatial context.

### Scalar Bar
The class vtkScalarBar is used to create a colorcoded key that relates color values to numerical data values as shown in Figure 4–9. There are three parts to the scalar bar: a rectangular bar with colored segments, labels, and a title.

![Figure 4-9](images/Figure_4-9.png)

*Figure 4–9 vtkScalarBarActor used to create color legends.*

To use vtkScalarBar, you must reference an instance of vtkLookupTable (defines colors and the range of data values), position and orient the scalar bar on the overlay plane, and optionally specify attributes such as color (of the labels and the title), number of labels, and text string for the title. The following example shows typical usage.

```tcl
vtkScalarBarActor scalarBar
scalarBar SetLookupTable [mapper GetLookupTable]
scalarBar SetTitle "Temperature"
[scalarBar GetPositionCoordinate] \
  SetCoordinateSystemToNormalizedViewport
calarBar GetPositionCoordinate] SetValue 0.1 0.01
scalarBar SetOrientationToHorizontal
scalarBar SetWidth 0.8
scalarBar SetHeight 0.17
```
The orientation of the scalar bar is controlled by the methods SetOrientationToVertical() and vtkSetOrientationToHorizontal(). To control the position of the scalar bar (i.e., its lower-left corner),
set the position coordinate (in whatever coordinate system you desire—see "vtkCoordinate and Coordinate Systems" on page 62), and then specify the width and height using normalized viewport values (or alternatively, specify the Position2 instance variable to set the upper-right corner).

### X-Y Plots
The class vtkXYPlotActor generates x-y plots from one or more input datasets, as shown in Figure 4–10. This class is particularly useful for showing the variation of data across a sequence of points such as a line probe or a boundary edge.

To use vtkXYPlotActor2D, you must specify one or more input datasets, axes, and the plot title, and position the composite actor on the overlay plane. The PositionCoordinate instance variable defines the location of the lower-left corner of the x-y plot (specified in normalized viewport coordinates), and the Position2Coordinate instance variable defines the upper-right corner. (Note: The Position2Coordinate is relative to PositionCoordinate, so you can move the vtkXYPlotActor around the viewport by setting just the PositionCoordinate.) The combination of the two position coordinates specifies a rectangle in which the plot will lie. The following example (from VTK/Examples/ Annotation/Tcl/xyPlot.tcl) shows how the class is used.

![Figure 4-10](images/Figure_4-10.png)

*Figure 4–10 Example of using the vtkXYPlotActor2D class to display three probe lines using three different techniques (seeVTK/Hybrid/Testing/ Tcl/xyPlot.tcl).*

```tcl
vtkXYPlotActor xyplot
xyplot AddInput [probe GetOutput]
xyplot AddInput [probe2 GetOutput]
xyplot AddInput [probe3 GetOutput]
[xyplot GetPositionCoordinate] SetValue 0.0 0.67 0
[xyplot GetPosition2Coordinate] SetValue 1.0 0.33 0
xyplot SetXValuesToArcLength
xyplot SetNumberOfXLabels 6
xyplot SetTitle "Pressure vs. Arc Length (Zoomed View)"
xyplot SetXTitle ""
xyplot SetYTitle "P"
xyplot SetXRange .1 .35
xyplot SetYRange .2 .4
[xyplot GetProperty] SetColor 0 0 0
```
Note the x axis definition. By default, the x coordinate is set as the point index in the input datasets. Alternatively, you can use arc length and normalized arc length of lines used as input to vtkXYPlotActor to generate the x values.

![Figure 4-11](images/Figure_4-11.png)

*Figure 4–11 Use of vtkCubeAxisActor2D. On the left, outer edges of the cube are used to draw the axes. On the right, the closest vertex to the camera is used.*

![Figure 4-12](images/Figure_4-12.png)

*Figure 4–12 Labelling point and cell ids on a sphere within a rectangular window.*

### Bounding Box Axes (vtkCubeAxesActor2D)

Another composite actor class is vtkCubeAxesActor2D. This class can be used to indicate the position in space that the camera is viewing, as shown in Figure 4–11. The class draws axes around the bounding box of the input dataset labeled with x-y-z coordinate values. As the camera zooms in, the
axes are scaled to fit within the cameras viewport, and the label values are updated. The user can control various font attributes as well as the relative font size (The font size is selected automatically— the method SetFontFactor() can be used to affect the size of the selected font.) The following script demonstrates how to use the class (taken from VTK/Examples/Annotation/Tcl/ cubeAxes.tcl).

```tcl
vtkTextProperty tprop
tprop SetColor 1 1 1
tprop ShadowOn
vtkCubeAxesActor2D axes
axes SetInput [normals GetOutput]
axes SetCamera [ren1 GetActiveCamera]
axes SetLabelFormat "%6.4g"
axes SetFlyModeToOuterEdges
axes SetFontFactor 0.8
axes SetAxisTitleTextProperty tprop
axis SetAxisLabelTextProperty tprop
```
Note that there are two ways that the axes can be drawn. By default, the outer edges of the bounding box are used (SetFlyModeToOuterEdges()). You can also place the axes at the vertex closest to the camera position (SetFlyModeToClosestTriad()).

### Labeling Data
In some applications, you may wish to display numerical values from an underlying data set. The class vtkLabeledDataMapper allows you to label the data associated with the points of a dataset. This includes scalars, vectors, tensors, normals, texture coordinates, and field data, as well as the point ids of the dataset. The text labels are placed on the overlay plane of the rendered image as shown in Figure 4–12. The figure was generated from the Tcl script VTK/Examples/Annotation/Tcl/ labeledMesh.tcl which is included in part below. The script uses three new classes, vtkCellCenters (to generate points at the parametric centers of cells), vtkIdFilter (to generate ids as scalar or field data from dataset ids), and vtkSelectVisiblePoints (to select those points currently visible), to label the cell and point ids of the sphere. In addition, vtkSelectVisiblePoints has the ability to define a “window” in display (pixel) coordinates in which it operates—all points outside of the window are discarded. 

```tcl
# Create a sphere
vtkSphereSource sphere
vtkPolyDataMapper sphereMapper
sphereMapper SetInputConnection [sphere GetOutputPort]
sphereMapper GlobalImmediateModeRenderingOn
vtkActor sphereActor
sphereActor SetMapper sphereMapper
# Generate ids for labeling

vtkIdFilter ids
ids SetInputConnection [sphere GetOutputPort]
ids PointIdsOn ids CellIdsOn ids FieldDataOn

vtkRenderer ren1
# Create labels for points

vtkSelectVisiblePoints visPts
visPts SetInputConnection [ids GetOutputPort]
visPts SetRenderer ren1
visPts SelectionWindowOn

visPts SetSelection $xmin [expr $xmin + $xLength] \
 $ymin [expr $ymin + $yLength]
vtkLabeledDataMapper ldm
ldm SetInput [visPts GetOutput]
ldm SetLabelFormat "%g"
ldm SetLabelModeToLabelFieldData
vtkActor2D pointLabels
pointLabels SetMapper ldm
# Create labels for cells

vtkCellCenters cc
cc SetInputConnection [ids GetOutputPort]
vtkSelectVisiblePoints visCells
visCells SetInputConnection [cc GetOutputPort]
visCells SetRenderer ren1
visCells SelectionWindowOn
visCells SetSelection $xmin [expr $xmin + $xLength] \
$ymin [expr $ymin + $yLength]
vtkLabeledDataMapper cellMapper
cellMapper SetInputConnection [visCells GetOutputPort]
cellMapper SetLabelFormat "%g"
cellMapper SetLabelModeToLabelFieldData
[cellMapper GetLabelTextProperty] SetColor 0 1 0
vtkActor2D cellLabels
cellLabels SetMapper cellMapper
# Add the actors to the renderer, set the background and size

ren1 AddActor sphereActor
ren1 AddActor2D pointLabels
ren1 AddActor2D cellLabels
```

## 4.13 Transforming Data

As we saw in the section “Notice how we use vtkAssembly’s AddPart() method to build the hierarchies. Assemblies can be nested arbitrarily deeply as long as there are not any self-referencing cycles. Note that vtkAssembly is a subclass of vtkProp3D, so it has no notion of properties or of an associated mapper. Therefore, the leaf nodes of the vtkAssembly hierarchy must carry information about material properties (color, etc.) and any associated geometry. Actors may also be used by more than one assembly (notice how coneActor is used in the assembly and as an actor). Also, the renderer’s AddActor() method is used to associate the top level of the assembly with the renderer; those actors at lower levels in the assembly hierarchy do not need to be added to the renderer since they are recursively rendered.” on page57, it is possible to position and orient vtkProp3D’s in world space. However, in many applications we wish to transform the data prior to using it in the visualization pipeline. For example, to use a plane to cut ("Cutting" on page 98) or clip ("Clip Data" on page110) an object, the plane must be positioned within the pipeline, not via the actor transformation matrix. Some objects (especially procedural source objects) can be created at a specific position and orientation in space. For example, vtkSphereSource has Center and Radius instance variables, and vtkPlaneSource has Origin, Point1, and Point2 instance variables that allow you to position the plane using three points. However, many classes do not provide this capability without moving data into a new position. In this case, you must transform the data using vtkTransformFilter or vtkTransformPolyDataFilter. 

vtkTransformFilter is a filter that takes vtkPointSet dataset objects as input. Datasets that are subclasses of the abstract class vtkPointSet represent points explicitly, that is, an instance of vtkPoints is used to store coordinate information. vtkTransformFilter applies a transformation matrix to the points and create a transformed points array; the rest of the dataset structure (i.e., cell topology) and attribute data (e.g., scalars, vectors, etc.) remains unchanged. vtkTransformPolyDataFilter does the same thing as vtkTransformFilter except that it is more convenient to use in a visualization pipeline containing polygonal data. 
![Figure 4-13](images/Figure_4-13.png)

*Figure 4–13 Transforming data within the pipeline.*

The following example (taken from VTK/Examples/ DataManipulation/Tcl/marching.tcl with results shown in Figure 4–13) uses a vtkTransformPolyDataFilter to reposition a 3D text string. (See “3D Text Annotation and vtkFollower” on page65 for more information about 3D text.)

```tcl
# define the text for the labels
vtkVectorText caseLabel
caseLabel SetText "Case 12c - 11000101"
vtkTransform aLabelTransform
aLabelTransform Identity
aLabelTransform Translate -.2 0 1.25
aLabelTransform Scale .05 .05 .05
vtkTransformPolyDataFilter labelTransform
labelTransform SetTransform aLabelTransform
labelTransform SetInputConnection [caseLabel GetOutputPort]
vtkPolyDataMapper labelMapper
labelMapper SetInputConnection [labelTransform GetOutputPort];
vtkActor labelActor
labelActor SetMapper labelMapper
```
Notice that vtkTransformPolyDataFilter requires that you supply it with an instance of vtkTransform. Recall that vtkTransform is used by actors to control their position and orientation in space. Instances of vtkTransform support many methods, some of the most commonly used are shown here.

- RotateX(angle) — apply rotation (angle in degrees) around the x axis
- RotateY(angle) — apply rotation around the y axis
- RotateZ(angle) — apply rotation around the z axis
- RotateWXYZ(angle,x,y,z) — apply rotation around a vector defined by x-y-z components
- Scale(x,y,z) — apply scale in the x, y, and z directions
- Translate(x,y,z) — apply translation
- Inverse() — invert the transformation matrix
- SetMatrix(m) — specify the 4x4 transformation matrix directly
- GetMatrix(m) — get the 4x4 transformation matrix
- PostMultiply() — control the order of multiplication of transformation matrices. If PostMultiply() is invoked, matrix operations are applied on the left hand side of the current matrix.
- PreMultiply() — matrix multiplications are applied on the right hand side of the current transformation matrix

The last two methods described above remind us that the order in which transformations are applied dramatically affects the resulting transformation matrix. (See “Notice how we use vtkAssembly’s AddPart() method to build the hierarchies. Assemblies can be nested arbitrarily deeply as long as there are not any self-referencing cycles. Note that vtkAssembly is a subclass of vtkProp3D, so it has no notion of properties or of an associated mapper. Therefore, the leaf nodes of the vtkAssembly hierarchy must carry information about material properties (color, etc.) and any associated geometry. Actors may also be used by more than one assembly (notice how coneActor is used in the assembly and as an actor). Also, the renderer’s AddActor() method is used to associate the top level of the assembly with the renderer; those actors at lower levels in the assembly hierarchy do not need to be added to the renderer since they are recursively rendered.” on page57.) We recommend that you spend some time experimenting with these methods and the order of application to fully understand vtkTransform.

### Advanced Transformation
Advanced users may wish to use VTK’s extensive transformation hierarchy. (Much of this work was done by David Gobbi.) The hierarchy, of which the class hierarchy is shown in Figure 19–17, supports a variety of linear and non-linear transformations.

A wonderful feature of the VTK transformation hierarchy is that different types of transformation can be used in a filter to give very different results. For example, the vtkTransformPolyDataFilter accepts any transform of type vtkAbstractTransform (or a subclass). This includes transformation types ranging from the linear, affine vtkTransform (represented by a 4x4 matrix) to the non-linear, warping vtkThinPlateSplineTransform, which is a complex function representing a correlation between a set of source and target landmarks.

### 3D Widgets
Interactor styles (see "Using VTK Interactors" on page 45) are generally used to control the camera and provide simple keypress and mouse-oriented interaction techniques. Interactor styles have no representation in the scene; that is, they cannot be “seen” or interacted with, the user must know what the mouse and key bindings are in order to use them. Certain operations, however, are greatly facilitated by the ability to operate directly on objects in the scene. For example, starting a rake of streamlines along a line is easily performed if the endpoints of the line can be interactively positioned.

3D widgets have been designed to provide this functionality. Like the class vtkInteractorStyle, 3D widgets are subclasses of vtkInteractorObserver. That is, they watch for events invoked by vtkRenderWindowInteractor. (Recall that vtkRenderWindowInteractor translates windowing-system specific events into VTK event invocations.) Unlike vtkInteractorStyle, however, 3D widgets represent themselves in the scene in various ways. Figure 4–14 illustrates some of the many 3D widgets found in VTK.

The following is a list of the most important widgets currently found in VTK and a brief description of their features. Note that some of the concepts mentioned here have not yet been covered in this text. Please refer to “Interaction, Widgets and Selections” on page255 to learn more about a particular concept and the various widgets available in VTK.

- vtkScalarBarWidget — Manage a vtkScalarBar including positioning, scaling, and orienting it. (See “Scalar Bar” on page66 for more information about scalar bars.)
- vtkPointWidget — Position a point x-y-z location in 3D space. The widget produces a polygonal output. Point widgets are typically used for probing. (See “Probing” on page100.)
- vtkLineWidget — Place a straight line with a specified subdivision resolution. The widget produces a polygonal output. A common use of the line widget is to probe (“Probing” on page100) and plot data (“X-Y Plots” on page66) or produce streamlines (“Streamlines” on page95) or stream surfaces (“Stream Surfaces” on page97).
- vtkPlaneWidget — Orient and position a finite plane. The plane resolution is variable, and the widget produces an implicit function and a polygonal output. The plane widget is used for probing (“Probing” on page100) and seeding streamlines (“Streamlines” on page95).
- vtkImplicitPlaneWidget — Orient and position an unbounded plane. The widget produces an implicit function and a polygonal output. The polygonal output is created by clipping the plane with a bounding box. The implicit plane widget is typically used for probing (“Probing” on page100), cutting (“Cutting” on page98), and clipping data (“Clip Data” on page110).
- vtkBoxWidget — Orient and position a bounding box. The widget produces an implicit function and a transformation matrix. The box widget is used to transform vtkProp3D’s and subclasses (“Transforming Data” on page70) or to cut (“Cutting” on page98) or clip data (“Clip Data” on page110).
- vtkImagePlaneWidget — Manipulate three orthogonal planes within a 3D volumetric data set. Probing of the planes to obtain data position, pixel value, and window-level is possible. The image plane widget is used to visualize volume data (“Image Processing and Visualization” on page103).
- vtkSphereWidget — Manipulate a sphere of variable resolution. The widget produces an implicit function and a transformation matrix and enables the control of focal point and position to support such classes as vtkCamera and vtkLight. The sphere widget can be used for controlling lights and cameras (“Controlling The Camera” on page49 and “Controlling Lights” on page51), for clipping (“Clip Data” on page110), and for cutting (“Cutting” on page98).
- vtkSplineWidget — Manipulate an interpolating 3D spline (“Creating Movie Files” on page248). The widget produces polygonal data represented by a series of line segments of specified resolution. The widget also directly manages underlying splines for each of the x-y-z coordinate values.

![Figure 4-14](images/Figure_4-14.png)

*Figure 4–14 Some of the 3D widgets found in VTK.*

While each widget provides different functionality and offers a different API, 3D widgets are similar in how they are set up and used. The general procedure is as follows.
1. Instantiate the widget.
2. Specify the vtkRenderWindowInteractor to observe. The vtkRenderWindowInteractor invokes events that the widget may process.
3. Create callbacks (i.e., commands) as necessary using the Command/Observer mechanism—see “User Methods, Observers, and Commands” on page 29. The widgets invoke the events StartInteractionEvent, InteractionEvent, and EndInteractionEvent.
4. Most widgets require "placing" – positioning in the scene. This typically entails specifying an instance of vtkProp3D, a dataset, or explicitly specifying a bounding box, and then invoking the PlaceWidget() method.
5. Finally, the widget must be enabled. By default, a keypress i will enable the widget and it will appear in the scene.

Note that more than one widget can be enabled at any given time, and the widgets function fine in combination with an instance of vtkInteractorStyle. Thus mousing in the scene not on any particular widget will engage the vtkInteractorStyle, but mousing on a particular widget will engage just that widget—typically no other widget or interactor style will see the events. (One notable exception is the class vtkInteractorEventRecorder that records events and then passes them along. It can also playback events. This is a very useful class for recording sessions and testing.)

The following example (found in VTK/Examples/ GUI/Tcl/ImplicitPlaneWidget.tcl) demonstrates how to use a 3D widget. The vtkImplicitPlaneWidget will be used to clip an object. (See “Clip Data” on page110 for more information in clipping.) In this example the vtkProp3D to be clipped is a mace formed from a sphere and cone glyphs located at the sphere points and oriented in the direction of the sphere normals. (See “Glyphing” on page94 for more information about glyphing.) The mace is clipped with a plane that separates it into two parts, one of which is colored green. The vtkImplicitPlaneWidget is used to control the position and orientation of the clip plane by mousing on the widget normal vector, moving the
point defining the origin of the plane, or translating the plane by grabbing the widget bounding box.

![Figure 4-15](images/Figure_4-15.png)

*Figure 4–15 Using the implicit plane widget (vtkImplicitPlaneWidget).*

```tcl
vtkSphereSource sphere
vtkConeSource cone
vtkGlyph3D glyph
glyph SetInputConnection [sphere GetOutputPort]
glyph SetSourceConnection [cone GetOutputPort]
glyph SetVectorModeToUseNormal
glyph SetScaleModeToScaleByVector
glyph SetScaleFactor 0.25
# The sphere and spikes are appended
# into a single polydata.
# This makes things simpler to manage.

vtkAppendPolyData apd
apd AddInputConnection [glyph GetOutputPort]
apd AddInputConnection [sphere GetOutputPort]
vtkPolyDataMapper maceMapper
maceMapper SetInputConnection [apd GetOutputPort]
vtkLODActor maceActor
maceActor SetMapper maceMapper
maceActor VisibilityOn
# This portion of the code clips the mace with the vtkPlanes
# implicit function. The clipped region is colored green.

vtkPlane plane
vtkClipPolyData clipper
clipper SetInputConnection [apd GetOutputPort]
clipper SetClipFunction plane
clipper InsideOutOn
vtkPolyDataMapper selectMapper
selectMapper SetInputConnection [clipper GetOutputPort]
vtkLODActor selectActor

selectActor SetMapper selectMapper
[selectActor GetProperty] SetColor 0 1 0
selectActor VisibilityOff
selectActor SetScale 1.01 1.01 1.01
vtkRenderer ren1
vtkRenderWindow renWin
renWin AddRenderer ren1
vtkRenderWindowInteractor iren
iren SetRenderWindow renWin
# Associate the line widget with the interactor

vtkImplicitPlaneWidget planeWidget
planeWidget SetInteractor iren
planeWidget SetPlaceFactor 1.25
planeWidget SetInput [glyph GetOutput]
planeWidget PlaceWidget
planeWidget AddObserver InteractionEvent myCallback
ren1 AddActor maceActor
ren1 AddActor selectActor
iren AddObserver UserEvent {wm deiconify .vtkInteract}
renWin Render
# Prevent the tk window from showing up then start the event loop.

wm withdraw .
proc myCallback {} {
    planeWidget GetPlane plane
    selectActor VisibilityOn
}
```
As shown above, the implicit plane widget is instantiated and placed. The placing of the widget is with respect to a dataset. (The Tcl statement “[glyph GetOutput]” returns a vtkPolyData, a subclass of vtkDataSet.) The PlaceFactor adjusts the relative size of the widget. In this example the widget is grown 25% larger than the bounding box of the input dataset. The key to the behavior of the widget is the addition of an observer that responds to the InteractionEvent. StartInteraction and EndInteractionare typically invoked by the widget on mouse down and mouse up respectively; the InteractionEvent is invoked on mouse move. The InteractionEvent is tied to the Tcl procedure myCallback that copies the plane maintained by the widget to an instance of vtkPlane—an implicit function used to do the clipping. (See “Implicit Modeling” on page213.)

The 3D widgets are a powerful feature in VTK that can quickly add complex interaction to any application. We encourage you to explore the examples included with the VTK distribution (in Examples/GUI and Hybrid/Testing/Cxx) to see the breadth and power of their capabilities.

## 4.14 Antialiasing

There are two ways to enable antialiasing with VTK: per primitive type or through multisampling. Multisampling usually gives more pleasant result.

Both antialiasing methods are controlled with the vtkRenderWindow API. When multisampling is enabled and supported by the graphics card, the per-primitive-type antialiasing flags are ignored. In both cases, the setting has to be done after the creation of a vtkRenderWindow object but before its initialization on the the screen.

Note that in general, the antialiasing result differs among actual OpenGL implementations. (an OpenGL implementation is either a software implementation, like Mesa, or the combination of a graphics card and its driver)

![Figure 4-16](images/Figure_4-16.png)

*Figure 4–16 Effect of antialiasing techniques on a wireframe sphere. 

### Per-primitive type antialiasing
Three flags, one for each type of primitive, control antialiasing:*
- PointSmoothing,
- LineSmoothing and
- PolygonSmoothing.
Initially, they are all disabled. Here are the 4 steps in required order to enable antialiasing on point primitives:
1. vtkRenderWindow *w=vtkRenderWindow::New();
2. w->SetMultiSamples(0);
3. w->SetPointSmoothing(1);
4. w->Render();

Here is a complete example to display the vertices of a mesh representing a sphere with point antialiasing:

```cpp
#include "vtkRenderWindowInteractor.h"
#include "vtkRenderWindow.h"
#include "vtkRenderer.h"
#include "vtkSphereSource.h"
#include "vtkPolyDataMapper.h"
#include "vtkProperty.h"
int main()
{

vtkRenderWindowInteractor *i=vtkRenderWindowInteractor::New();
vtkRenderWindow *w=vtkRenderWindow::New();
i->SetRenderWindow(w);
w->SetMultiSamples(0); // no multisampling
w->SetPointSmoothing(1); // point antialiasing
vtkRenderer *r=vtkRenderer::New();
w->AddRenderer(r);
vtkSphereSource *s=vtkSphereSource::New();
vtkPolyDataMapper *m=vtkPolyDataMapper::New();
m->SetInputConnection(s->GetOutputPort());
vtkActor *a=vtkActor::New();
a->SetMapper(m);
vtkProperty *p=a->GetProperty();
p->SetRepresentationToPoints(); // we want to see points
p->SetPointSize(2.0); // big enough to notice antialiasing
p->SetLighting(0); // don't be disturb by shading
r->AddActor(a);
i->Start();
s->Delete();
m->Delete();
a->Delete();
r->Delete();
w->Delete();
i->Delete();
}
```
The following lines are specific to point antialiasing:

```cpp
w->SetPointSmoothing(1);
p->SetRepresentationToPoints();
p->SetPointSize(2.0);
```
You can visualize line antialiasing by changing them to:

```cpp
w->SetLineSmoothing(1);
p->SetRepresentationToWireframe();
p->SetLineWidth(2.0);
```
You can visualize polygon antialiasing with simply:

```cpp
w->PolygonSmoothing(1);
p->SetRepresentationToSurface();
```

### Multisampling
Multisampling gives better result than the previous method. Initially, multisampling is enabled. But it is only effective if the graphics card support it. Currently, VTK supports multisampling on X window only. To disable multisampling, set the MultiSamples value (initially set to 8) to 0:

1. vtkRenderWindow *w=vtkRenderWindow::New();
2. w->SetMultiSamples(0); // disable multisampling.
3. w->Render();

Going back to the previous example, if you are using X11, just get rid of line disabling multisampling and we will see the effect of multisampling on points, lines or polygons.

## 4.15 Translucent polygonal geometry

Rendering the geometry as translucent is a powerful tool for visualization. It allows to "see through" the data. It can be used also to focus on a region of interest; the region of interest is rendered as opaque and the context is renderered as translucent.

Rendering translucent geometry is not trivial: the final color of a pixel on the screen is the contribution of all the geometry primitives visible through the pixel. The color of the pixel is the result of blending operations between the colors of all visible primitives. Blending operations themselves are usually order-dependent (ie not commutative). Therefore, for a correct rendering, depth sorting is required. However, depth sorting has a computational cost.

VTK offers three ways to render translucent polygonal geometry. Each of them is a tradeoff between correctness (quality) and cost (of depth sorting).

**Fast and Incorrect.** Start ignoring the previous remark about depth sorting. There is then no extra computational cost but the result on the screen is incorrect. However, depending of the application context, the result might be good enough.
**Slower and Almost Correct.** This method consists in using two filters. First, append all the polygonal geometry with vtkAppendPolyData. Then connect the output port of vtkAppendPolyData to the input port of vtkDepthSortPolyData. Depth sorting is performed per centroid of geometry primitives, not per pixel. For this reason it is not correct but it solves most of the ordering issues and gives a result usually good enough. Look at VTK/Hybrid/Testing/Tcl/depthSort.tcl for an example.
**Very Slow and Correct.** If the graphics card supports it (nVidia only), use "depth peeling". It performs per pixel sorting (better result) but it is really slow. Before the first Render, ask for alpha bits on the vtkRenderWindow:

```cpp
vtkRenderWindow *w=vtkRenderWindow::New();
w->SetAlphaBitPlanes(1);

// Make sure multisampling is disabled:

w->SetMultiSamples(0);
```
On the renderer, enable depth peeling:

```cpp
vtkRenderer *r=vtkRenderer::New();
r->SetUseDepthPeeling(1);
```
Set the depth peeling parameters (the maximum number of rendering passes and the occlusion ratio). The parameters are explained in the next section.

```cpp
r->SetMaximumNumberOfPeels(100);
r->SetOcclusionRatio(0.1);

// Render the scene:

w->Render();

// Finally, you can check that the graphics card supported depth peeling:

r->GetLastRenderingUsedDepthPeeling();
```

**Depth Peeling Parameters.** In order to play with the depth peeling parameters, it is necessary to understand the algorithm itself. The algorithm peels the translucent geometry from front to back until there is no more geometry to render. The iteration loop stops either if it reaches the maximum number of iterations set by the user or if the number of pixels modified by the last peel is less than some ratio of the area of the window (this ratio is set by the user, if the ratio is set to 0.0, it means the user wants the exact result. A ratio of 0.2 will render faster than a ratio of 0.1).

**OpenGL requirements.** The graphics card supports depth peeling, if the following OpenGL extensions are supported:
* GL_ARB_depth_texture or OpenGL>=1.4
* GL_ARB_shadow or OpenGL>=1.4
* GL_EXT_shadow_funcs or OpenGL>=1.5
* GL_ARB_vertex_shader or OpenGL>=2.0
* GL_ARB_fragment_shader or OpenGL>=2.0
* GL_ARB_shader_objects or OpenGL>=2.0
* GL_ARB_occlusion_query or OpenGL>=1.5
* GL_ARB_multitexture or OpenGL>=1.3
* GL_ARB_texture_rectangle
* GL_SGIS_texture_edge_clamp, GL_EXT_texture_edge_clamp or OpenGL>=1.2

In practice, it works with nVidia GeForce 6 series and above or with Mesa (e.g. 7.4). It does not work with ATI cards.

**Example.** Here a complete example that uses depth peeling (you can also look for files having DepthPeeling in their name in VTK/Rendering/Testing/Cxx).

```cpp
#include "vtkRenderWindowInteractor.h"
#include "vtkRenderWindow.h"
#include "vtkRenderer.h"
#include "vtkActor.h"
#include "vtkImageSinusoidSource.h"

#include "vtkImageData.h"
#include "vtkImageDataGeometryFilter.h"
#include "vtkDataSetSurfaceFilter.h"
#include "vtkPolyDataMapper.h"
#include "vtkLookupTable.h"
#include "vtkCamera.h"
int main()
{
vtkRenderWindowInteractor *iren=vtkRenderWindowInteractor::New();
vtkRenderWindow *renWin = vtkRenderWindow::New();
renWin->SetMultiSamples(0);
renWin->SetAlphaBitPlanes(1);
iren->SetRenderWindow(renWin);
renWin->Delete();
vtkRenderer *renderer = vtkRenderer::New();
renWin->AddRenderer(renderer);
renderer->Delete();
renderer->SetUseDepthPeeling(1);
renderer->SetMaximumNumberOfPeels(200);
renderer->SetOcclusionRatio(0.1);
vtkImageSinusoidSource *imageSource=vtkImageSinusoidSource::New();
imageSource->SetWholeExtent(0,9,0,9,0,9);
imageSource->SetPeriod(5);
imageSource->Update();
vtkImageData *image=imageSource->GetOutput();
double range[2];
image->GetScalarRange(range);
vtkDataSetSurfaceFilter *surface=vtkDataSetSurfaceFilter::New();
surface->SetInputConnection(imageSource->GetOutputPort());
imageSource->Delete();
vtkPolyDataMapper *mapper=vtkPolyDataMapper::New();
mapper->SetInputConnection(surface->GetOutputPort());
surface->Delete();
vtkLookupTable *lut=vtkLookupTable::New();
lut->SetTableRange(range);
lut->SetAlphaRange(0.5,0.5);
lut->SetHueRange(0.2,0.7);
lut->SetNumberOfTableValues(256);
lut->Build();
mapper->SetScalarVisibility(1);

mapper->SetLookupTable(lut);
lut->Delete();
vtkActor *actor=vtkActor::New();
renderer->AddActor(actor);
actor->Delete();
actor->SetMapper(mapper);
mapper->Delete();
renderer->SetBackground(0.1,0.3,0.0);
renWin->SetSize(400,400);
renWin->Render();
if(renderer->GetLastRenderingUsedDepthPeeling())
{
cout<<"depth peeling was used"<<endl;
}
else
{
cout<<"depth peeling was not used (alpha blending instead)"<<endl;
}
vtkCamera *camera=renderer->GetActiveCamera();
camera->Azimuth(-40.0);
camera->Elevation(20.0);
renWin->Render();
iren->Start();
}
```

**Painter mechanism: customizing the polydata mapper.** Sometimes you want full control of the steps used to render a polydata. VTK makes it possible with the use of the painter mechanism. Thanks to the factory design pattern, the following line actually creates a vtkPainterPolyDataMapper:

```cpp
vtkPolyDataMapper *m=vtkPolyDataMapper::New();
```
You can have access to the vtkPainterPolyDataMapper API by downcasting: 

```
vtkPainterPolyDataMapper *m2=vtkPainterPolyDataMapper::SafeDownCast(m);
```
This polydata mapper delegates the rendering to a vtkPainter object. SetPainter() and GetPainter() gives access to this delegate.

vtkPainter itself is just an abstract API shared by concrete Painters. Each of them is responsible for one stage of the rendering. This mechanism allows to choose and combine stages. For example vtkPolygonsPainter is responsible for drawing polygons whereas vtkLightingPainter is responsible
for setting lighting parameters. The combination of painters forms a chain of painters. It is a chain
because each painter can delegate part of the execution of the rendering to another painter.

Most of the time, you don't need to explicitly set the chain of painters: vtkDefaultPainter already set a standard chain of painters for you.

**Writing your own painter.** Writing your own painter consists essentially in writing 2 classes: an abstract subclass of vtkPainter, a concrete class with the OpenGL implementation.

Let's take a look at an existing Painter: vtkLightingPainter. vtkLightingPainter derives from vtkPainter and is almost empty. The real implementation is in the concrete class vtkOpenGLLightingPainter which overrides the protected method RenderInternal().

The arguments of RenderInternal() are essentially the renderer and the actor. Implementing RenderInternal() consists in writing the actual rendering stage code and calling the next Painter in the
painter chain (the "delegate") by calling this->Superclass::RenderInternal().

## 4.16 Animation

- Animation is important component of Visualization System, etc.
- It is possible to create simple animations by writing loops that continuously change some parameter on a filter and render. However such implementations can become complicated when multiple parameter changes are involved.
- VTK provides a framework comprising of vtkAnimationCue and vtkAnimationScene to manage animation setup and playback.
- vtkAnimationCue corresponds to an entity that changes with time e.g. position of an actor; while vtkAnimationScene represents a scene or a setup for the animation comprising of instances of vtkAnimationCue.

## Animation Scene (vtkAnimationScene)

vtkAnimationScene represents a scene or a setup for the animation. An animation is generated by rendering frames in a sequence while changing some visualization parameter(s) before rendering each frame. Every frame has an animation time associated with it, which can be used to determine the frame's place in the animation. Animation time is simply a counter that continuously increases over the duration of the animation based on the play-mode.

Following are important methods on a vtkAnimationScene:

`SetStartTime()/SetEndTime()` These represent the start and end times of the animation scene. This is the range that the animation time covers during playback.

`SetPlayMode()` This is used to control they playback mode i.e. how the animation time is changed. There are two modes available:

`Sequence Mode (PLAYMODE_SEQUENCE)` In this mode, the animation time is increased by (1/frame-rate) for every frame until the EndTime is reached. Hence the number of frames rendered in a single run is fixed irrespective of how long each frame takes to render.

`RealTime Mode (PLAYMODE_REALTIME)` In this mode, the animation runs for approximately (EndTime-StartTime) seconds, where the animation time at nth frame is given by (animation time and (n-1)th frame + time to render (n-1)th frame). Thus the number of frames rendered changes depending on how
long each frame takes to render.

`SetFrameRate()` Frame rate is the number of frames per unit time. This is used only in sequence playmode.

`AddCue(), RemoveCue(), RemoveAllCue()` Methods to add/remove animation cues from the scene.

`SetAnimationTime()` SetAnimationTime can be used to explicitly advance to a particular frame.

`GetAnimationTime()` GetAnimationTime() can be called during playback to query the animation clock time.

`Play()` Starts playing the animation.

`SetLoop()` When set to True, Play() results in playing the animation in a loop.

`Animation Cue (vtkAnimationCue)` vtkAnimationCue corresponds to an entity that changes in an animation. vtkAnimationCue does not know how to bring about the changes to the parameters. So the user has to either subclass vtkAnimationCue or use event observers to perform the changes as the animation progresses.

A cue has a start-time and an end-time in an animation scene. During playback, a cue is active when the scene's animation time is within the range specified the start and end times for the cue. When the cue is activated, it fires the vtkCommand::StartAnimationCueEvent. For every subsequent frame, it fires the vtkCommand::AnimationCueTickEvent until the end-time is reached when the vtkCommand::EndAnimationCueEvent is fired. Following are the important methods of vtkAnimationCue

`SetTimeMode` TimeMode defines how the start and time times are specified. There are two modes available.

`Relative (TIMEMODE_RELATIVE)` In this mode the animation cue times are specified relative to the start of the animation scene.

`Normalized (TIMEMODE_NORMALIZED)` In this mode, the cue start and end times are always in the range [0, 1] where 0 corresponds to the start and 1 corresponds to the end of the animation scene.

`SetStartTime/SetEndTime`
These are used to indicate the range of animation time when this cue is active. When the TimeMode is TIMEMODE_RELATIVE, these are specified in the same unit as the animation scene start and end times and are relative to the start of the animation scene. If TimeMode is TIMEMODE_NORMALIZED, these are in the range [0, 1] where 0 corresponds to the start of the animation scene while 1 corresponds to the end of the animation scene.

`GetAnimationTime()` This is provided for the event handler for vtkCommand::AnimationCueTickEvent. It can be used by the handler to determine how far along in the animation the current frame it. It's value depends on the TimeMode. If TimeMode is Relative, then the value will be number of time units since the cue was activated. If TimeMode is Normalized then it will be value in the range [0, 1] where 0 is the start of the cue, while 1 is the end of the cue.

`GetClockTime()` This is same as the animation clock time returned by vtkAnimationScene::GetAnimationTime(). It is valid only in the event handler for vtkCommand::AnimationCueTickEvent.

`GetDeltaTime()` This can be used to obtain the change in animation click time from when the previous frame was rendered, if any. Again, this is valid in only in the event handler for vtkCommand::AnimationCueTickEvent.

`TickInternal(double currentime, double deltatime, double clocktime)` As mentioned earlier, one can subclasses vtkAnimationCue, instead of writing event handlers to do the animation, in which case you can override this method. The arguments correspond to the values returned by GetAnimationTime(), GetDeltaTime() and GetClockTime() respectively.

`StartCueInternal(), EndCueInternal()` These methods can be overridden in subclasses to do setup and cleanup and start and end of the cue during playback. Alternatively, one can add event observers for the vtkCommand::StartAnimationCueEvent and vtkCommand::EndAnimationCueEvent to do the same.

In the following example, we create a simple animation where the StartTheta of a vtkSphereSource is varied over the length of the animation. We use normalized time mode for the animation cue in this example, so that we can change the scene times or the cue times and the code to change the StartTheta value can still remain unchanged.

```cpp
class vtkCustomAnimationCue: public vtkAnimationCue
{
public:

static vtkCustomAnimationCue* New();
vtkTypeRevisionMacro(vtkCustomAnimationCue, vtkAnimationCue);
vtkRenderWindow *RenWin;
vtkSphereSource* Sphere;

protected:
vtkCustomAnimationCue()
{
this->RenWin = 0;
this->Sphere = 0;
}
// Overridden to adjust the sphere's radius depending on the frame we
// are rendering. In this animation we want to change the StartTheta
// of the sphere from 0 to 180 over the length of the cue.
virtual void TickInternal(double currenttime, double deltatime, double clocktime)

{
double new_st = currenttime * 180;
// since the cue is in normalized mode, the currentime will be in the
// range [0,1], where 0 is start of the cue and 1 is end of the cue.
this->Sphere->SetStartTheta(new_st);
this->RenWin->Render();
}
};
vtkStandardNewMacro(vtkCustomAnimationCue);
vtkCxxRevisionMacro(vtkCustomAnimationCue, "$Revision$");
int main(int argc, char *argv[])
{
// Create the graphics structure. The renderer renders into the
// render window.
vtkRenderer *ren1=vtkRenderer::New();
vtkRenderWindow *renWin=vtkRenderWindow::New();
renWin->SetMultiSamples(0);
renWin->AddRenderer(ren1);
vtkSphereSource* sphere = vtkSphereSource::New();
vtkPolyDataMapper* mapper = vtkPolyDataMapper::New();
mapper->SetInputConnection(sphere->GetOutputPort());
vtkActor* actor = vtkActor::New();
actor->SetMapper(mapper);
ren1->AddActor(actor);
ren1->ResetCamera();
renWin->Render();
// Create an Animation Scene
vtkAnimationScene *scene = vtkAnimationScene::New();
scene->SetModeToSequence();
scene->SetFrameRate(30);
scene->SetStartTime(0);
scene->SetEndTime(60);
// Create an Animation Cue to animate the camera.
vtkCustomAnimationCue *cue1 = vtkCustomAnimationCue::New();
cue1->Sphere = sphere;
cue1->RenWin = renWin;
cue1->SetTimeModeToNormalized();
cue1->SetStartTime(0);
cue1->SetEndTime(1.0);
scene->AddCue(cue1);

scene->Play();
scene->Stop();
ren1->Delete();
renWin->Delete();
scene->Delete();
cue1->Delete();
return 0;
}
```