# Chapter 7: Volume Rendering

Volume rendering is a term used to describe a rendering process applied to 3D data where information exists throughout a 3D space instead of simply on 2D surfaces defined in 3D space. There is not a clear dividing line between volume rendering and geometric rendering techniques. Often two different approaches can produce similar results, and in some cases one approach may be considered both a volume rendering and a geometric rendering technique. For example, you can use a contouring technique to extract triangles representing an isosurface in an image dataset (see "Contouring" on page 93) and then use geometric rendering techniques to display these triangles, or you can use a volumetric ray casting technique on the image dataset and terminate the ray traversal at a particular isovalue. These two different approaches produce similar (although not necessarily identical) results. Another example is the technique of employing texture mapping hardware in order to perform composite volume rendering. This one method may be considered a volume rendering technique since it works on image data, or a geometric technique since it uses geometric primitives and standard graphics hardware.

In VTK a distinction is made between volume rendering techniques and geometric rendering techniques in order to customize the properties of the data being rendered. As you have seen throughout the many examples shown thus far, rendering data typically involves creating a vtkActor, a vtkProperty, and some subclass of a vtkMapper. The vtkActor is used to hold position, orientation and scaling information about the data, as well as a pointer to both the property and the mapper. The vtkProperty object captures various parameters that control the appearance of the data such as the ambient lighting coefficient and whether the object is flat, Gouraud, or Phong shaded. Finally, the vtkMapper subclass is responsible for actually rendering the data. For volume rendering, a different set of classes with very similar functionality are utilized. A vtkVolume is used in place of a vtkActor to represent the data in the scene. Just like the vtkActor, the vtkVolume represents the position, orientation and scaling of the data within the scene. However, a vtkVolume contains references to a vtkVolumeProperty and a vtkAbstractVolumeMapper. The vtkVolumeProperty represents those parameters that affect the appearance of the data in a volume rendering process, which is a different set of parameters than those used during geometric rendering. A vtkAbstractVolumeMapper subclass is responsible for the volume rendering process and ensures that the input data is of the correct type for the mapper's specific algorithm.

In VTK, volume rendering techniques have been implemented for both regular rectilinear grids (vtkImageData) and unstructured data (vtkUnstructuredGrid). The SetInput() method of the specific subclass of vtkAbstractVolumeMapper that you utilize will accept a pointer to only the correct type of data (vtkImageData or vtkUnstructuredGrid) as appropriate for that mapper. Note that you can resample irregular data into a regular image data format in order to take advantage of the vtkImageData rendering techniques described in this chapter (see "Probing" on page 100). Alternatively, you can tetrahedralize your data to produce an unstructured mesh to use the vtkUnstructuredGrid rendering techniques described in this chapter.

There are several different volume rendering techniques available for each supported data type. We will begin this chapter with some simple examples written using several different rendering techniques. Then we will cover the objects/parameters common to all of these techniques. Next, each of the volume rendering techniques will be discussed in more detail, including information on parameters specific to that rendering method. This will be followed by a discussion on achieving interactive rendering rates that is applicable to all volume rendering methods.

## 7.1 Historical Note on Supported Data Types

The first volume rendering methods incorporated into VTK were designed solely for vtkImageData. The superclass vtkVolumeMapper was developed to define the API for all vtkImageData volume rendering methods. Later, volume rendering of vtkUnstructuredGrid datasets was added to VTK. In order to preserve backwards compatibility, a new abstract superclass was introduced as the superclass for all types of volume rendering. Hence vtkAbstractVolumeMapper is the superclass of both vtkVolumeMapper (whose subclasses render only vtkImageData datasets) and vtkUnstructuredGridVolumeMapper (whose subclasses render only vtkUnstructuredGrid datasets).

## 7.2 A Simple Example

Consider the simple volume rendering example shown below and illustrated in Figure 7–1 (refer to VTK/Examples/VolumeRendering/Tcl/SimpleRayCast.tcl).

![Figure 7-1](images/Figure_7-1.png)

*Figure 7–1 Volume rendering.*

This example is written for volumetric ray casting of vtkImageData, but only the portion of the Tcl script highlighted with bold text is specific to this rendering technique. Following this example you will find the alternate versions of the bold portion of the script that would instead perform the volume rendering task with other mappers, including a texture mapping approach to rendering vtkImageData and a projection-based method for volume rendering vtkUnstructuredGrid datasets. You will notice that switching volume rendering techniques, at least in this simple case, requires only a few minor changes to the script, since most of the functionality is defined in the superclass API and is therefore common to all volume mappers.

```tcl
# Create the reader for the data
vtkStructuredPointsReader reader
reader SetFileName "$VTK_DATA_ROOT/Data/ironProt.vtk"
# Create transfer mapping scalar value to opacity
vtkPiecewiseFunction opacityTransferFunction
opacityTransferFunction AddPoint 20 0.0
opacityTransferFunction AddPoint 255 0.2
# Create transfer mapping scalar value to color
vtkColorTransferFunction colorTransferFunction
colorTransferFunction AddRGBPoint 0.0 0.0 0.0 0.0
colorTransferFunction AddRGBPoint 64.0 1.0 0.0 0.0
colorTransferFunction AddRGBPoint 128.0 0.0 0.0 1.0
colorTransferFunction AddRGBPoint 192.0 0.0 1.0 0.0
colorTransferFunction AddRGBPoint 255.0 0.0 0.2 0.0
# The property describes how the data will look
vtkVolumeProperty volumeProperty
volumeProperty SetColor colorTransferFunction
volumeProperty SetScalarOpacity opacityTransferFunction
# The mapper / ray cast functions know how to render the data
vtkVolumeRayCastCompositeFunction compositeFunction
vtkVolumeRayCastMapper volumeMapper
volumeMapper SetVolumeRayCastFunction compositeFunction
volumeMapper SetInputConnection [reader GetOutputPort]
# The volume holds the mapper and the property and
# can be used to position/orient the volume
vtkVolume volume
volume SetMapper volumeMapper
volume SetProperty volumeProperty
ren1 AddProp volume
renWin Render
```

In this example we start by reading in a data file from disk. We then define the functions that map scalar value into opacity and color which are used in the vtkVolumeProperty. Next we create the objects specific to volumetric ray casting—a vtkVolumeRayCastCompositeFunction that performs the compositing of samples along the ray, and a vtkVolumeRayCastMapper that performs some of the basic ray casting operations such as transformations and clipping. We set the input of the mapper to the data we read off the disk, and we create a vtkVolume (a subclass of vtkProp3D similar to vtkActor) to hold the mapper and property. Finally, we add the volume to the renderer and render the scene.

If you decided to implement the above script with a 2D texture mapping approach instead of volumetric ray casting, the bold portion of the script would instead be:

```tcl
# Create the objects specific to 2D texture mapping approach
vtkVolumeTextureMapper2D volumeMapper
volumeMapper SetInputConnection [reader GetOutputPort]
```

If your graphics card has the required support for 3D texture mapping (nearly all recent cards do have this support), then you may decide to implement the above script with a 3D texture mapping approach. The bolded portion of the script would instead be:

```tcl
# Create the objects specific to 3D texture mapping approach
vtkVolumeTextureMapper3D volumeMapper
volumeMapper SetInputConnection [reader GetOutputPort]
```

The vtkFixedPointVolumeRayCastMapper is an alternative to the vtkVolumeRayCastMapper, and is for most situations the recommended software mapper. The vtkFixedPointVolumeRayCastMapper handles all data types as well as multicomponent data, and uses fixed pointed computations and space leaping for high performance. However, it is not extensible since the blending operations are hardcoded for performance, rather than customizable by writing new ray cast functions. To change this example over to using the vtkFixedPointVolumeRayCastMapper, the bold portion of the script would instead be:

```tcl
# Create the fixed point ray cast mapper
vtkFixedPointVolumeRayCastMapper volumeMapper
volumeMapper SetInputConnection [reader GetOutputPort]
```

 If you would like to use an unstructured grid volume rendering technique instead, the replacement code becomes slightly more complex in order to perform the conversion from vtkImageData to vtkUnstructuredGrid before passing the data as input to the mapper. In this case we will use the unstructured grid rendering method that projects a tetrahedral representation of the grid using the graphics hardware. The replacement code would be:

```tcl
# Convert data to unstructured grid
vtkDataSetTriangleFilter tetraFilter
tetraFilter SetInputConnection [reader GetOutputPort]
# Create the objects specific to the Projected Tetrahedra method
vtkProjectedTetrahedraMapper volumeMapper
volumeMapper SetInputConnection [tetraFilter GetOutputPort]
```

Note that it is not recommended to convert from vtkImageData to vtkUnstructuredGrid for rendering since the mappers that work directly on vtkImageData are typically more efficient, both in memory consumption and rendering performance, than the mappers for vtkUnstructuredGrid data.

## 7.3 Why Multiple Volume Rendering Techniques?

As you can see, in this simple example the main thing that changes between rendering strategies is the type of volume mapper that is instantiated, and perhaps some rendering-method-specific parameters such as the ray cast function used in the ray casting technique. This may lead you to the following questions: why are there different volume rendering strategies in VTK? Why can’t VTK simply pick the “best” strategy? First, it is not always easy to predict which strategy will work best—ray casting may out-perform texture mapping if the image size is reduced, more processors become available, or the graphics hardware is the bottleneck to the rendering rate. These are parameters that differ from platform to platform, and in fact may change continuously at run time. Second, due to its computational complexity, most volume rendering techniques only produce an approximation of the desired rendering equation. For example, techniques that take samples through the volume and composite them with an alpha blending function are only approximating the true integral through the volume. Under different circumstances, different techniques perform better or worse than others in terms of both quality and speed. In addition, some techniques work only under certain special conditions. For example, some techniques support data with only a single scalar component of unsigned char or unsigned short type, while other techniques support any scalar type and multi-component data. The “best” technique will depend on your specific data, your performance and image quality requirements, and the hardware configuration of the system on which the code is run. In fact, the “best” technique may actually be a combination of techniques. A section of this chapter is dedicated to describing the multi-technique level-of-detail strategies that may be employed to achieve interactive volume rendering in a cross-platform manner.

## 7.4 Creating a vtkVolume

A vtkVolume is a subclass of vtkProp3D intended for use in volume rendering. Similar to a vtkActor (that is intended for geometric rendering), a vtkVolume holds the transformation information such as position, orientation, and scale, and pointers to a mapper and property. Additional information on how to control the transformation of a vtkVolume is covered in “Controlling 3D Props” on page52.

The vtkVolume class accepts objects that are subclasses of vtkAbstractVolumeMapper as input to SetMapper(), and accepts a vtkVolumeProperty object as input to SetProperty(). vtkActor and vtkVolume are two separate objects in order to enforce the different types of the mappers and properties. These different types are necessary due to the fact that some parameters of geometric rendering do not make sense in volume rendering and vice versa. For example, the SetRepresentationToWireframe() method of vtkProperty is meaningless in volume rendering, while the SetInterpolationTypeToNearest() method of vtkVolumeProperty has no value in geometric rendering.

## 7.5 Using vtkPiecewiseFunction

In order to control the appearance of a 3D volume of scalar values, several mappings or transfer functions must be defined. Generally, two transfer functions are required for all volume rendering techniques. The first required transfer function, known as the scalar opacity transfer function, maps the scalar value into an opacity or an opacity per unit length value. The second transfer function, referred to simply as the color transfer function, maps the scalar value into a color. An optional transfer function employed in some of the structured volume rendering methods is known as the gradient opacity transfer function, which maps the magnitude of the gradient of the scalar value into an opacity multiplier. Any of these mappings can be defined as a single value to single value mapping, which can be represented with a vtkPiecewiseFunction. For the scalar value to color mapping, a vtkColorTransferFunction can also be used to define RGB rather than grayscale colors.

From a user’s point of view, vtkPiecewiseFunction has two types of methods—those that add information to the mapping, and those that clear out information from the mapping. When information is added to a mapping, it is considered to be a point sample of the mapping with interpolation used to determine values between the specified ones. For example, consider the following section of a script on the left that produces the transfer function draw on the right:

![tf](images/Figure_7-2-1.png)

```tcl
vtkPiecewiseFunction tfun
tfun AddPoint 50 0.2
tfun AddPoint 200 1.0
```

The value of the mapping for the scalar values of 50 and 200 are given as 0.2 and 1.0 respectively, and all other mapping values can Scalar Value be obtained by linearly interpolating between these two values. If Clamping is on (it is by default) then the mapping of any value below 50 will be 0.2, and the mapping of any value above 200 will be 1.0. If Clamping is turned off, then out-of-range values map to 0.0.

Points can be added to the mapping at any time. If a mapping is redefined it replaces the existing mapping. In addition to adding a single point, a segment can be added which will define two mapping points and clear any existing points between the two. As an example, consider the following two modification steps and the corresponding pictorial representations of the transfer functions:

<table>
  <tr>
    <td>
      <img src="images/Figure_7-2-2.png" alt="tf1" width="400">
    </td>
    <td>

```tcl
tfun RemovePoint 50
tfun AddPoint 50 0.0
tfun AddSegment 100 0.8 150 0.2
```

  </tr>

  <tr>
    <td>
      <img src="images/Figure_7-2-3.png" alt="tf2" width="400">
    </td>
    <td>

```tcl
tfun AddPoint 50 0.2
tfun AddSegment 60 0.4 190 0.8
tfun ClampingOff
```

  </tr>
</table>

In the first step, we change the mapping of scalar value 50 by removing the point and then adding it again, and we add a segment. In the second step, we change the mapping of scalar value 50 by simply adding a new mapping without first removing the old one. We also add a new segment which eliminates the mappings for 100 and 150 since they lie within the new segment, and we turn clamping off.

## 7.6 Using vtkColorTransferFunction

A vtkColorTransferFunction can be used to specify a mapping of scalar value to color using either an RGB or HSV color space. The methods available are similar to those provided by vtkPiecewiseFunction, but tend to come in two flavors. For example, AddRGBPoint() and AddHSVPoint() both add a point into the transfer function with one accepting an RGB value as input and the other accepting an HSV value as input. The following Tcl example shows how to specify a transfer function from red to green to blue with RGB interpolation performed for values in between those specified: rep yticapO htgneL tinU 1 0 50 200 Scalar Value rep yticapO htgneL tinU 1 0 50 200 Scalar Value rep yticapO htgneL tinU 1 0 50 200

```tcl
vtkColorTransferFunction ctfun
ctfun SetColorSpaceToRGB
ctfun AddRGBPoint 0 1 0 0
ctfun AddRGBPoint 127 0 1 0
ctfun AddRGBPoint 255 0 0 1
```

## 7.7 Controlling Color / Opacity with a vtkVolumeProperty

In the previous two sections we have discussed the basics of creating transfer functions, but we have not yet discussed how these control the appearance of the volume. Typically, defining the transfer functions is the hardest part of achieving an effective volume visualization since you are essentially performing a classification operation that requires you to understand the meaning of the underlying data values.

For rendering techniques that map a pixel to a single location in the volume (such as an isosurface rendering or a maximum intensity projection) the ScalarOpacity transfer function maps the scalar value to an opacity. When a compositing technique is used, the ScalarOpacity function maps scalar value to an opacity that is accumulated per unit length for a homogenous region of that value. The specific mapper then utilizes a form of compositing to accumulate the continuously changing color and opacity values through the volume to form a final color and opacity that is stored in the corresponding pixel.

![Figure 7-2](images/Figure_7-2.png)

*Figure 7–2 CT torso data classified using the ScalarOpacity, Color, and GradientOpacity transfer functions.*

The ScalarOpacity and Color transfer functions are typically used to perform a simple classification of the data. Scalar values that are part of the background, or that are considered noise, are mapped to an opacity of 0.0, eliminating them from contributing to the image. The remaining scalar values can be divided into different “materials” which have different opacities and colors. For example, data acquired from a CT scanner can often be categorized as air, soft tissue, or bone based on the density value contained in the data (Figure 7–2). The scalar values defined as air would be given an opacity of 0.0, the soft tissue scalar values might be given a light red-brown color and the bone values might be given a white color. By varying the  of these last two materials, you can visualize the skin surface or the bone surface, or potentially see the bone through the translucent skin. This process of determining the dividing line between materials in the data can be tedious, and in some cases not possible based on the raw input data values. For example, liver and kidney sample locations may have overlapping CT density values. In this case, a segmentation filter may need to be applied to the volume to either alter the data values so that materials can be classified solely on the basis of the scalar value, or to extract out one specific material type. These segmentation operations can be based on additional information such as location or a comparison to a reference volume.

![Figure 7-3](images/Figure_7-3.png)

*Figure 7–3 CT head data classified using the ScalarOpacity, Color, and GradientOpacopacity transfer functions*

Two examples of segmenting CT data using only the transfer functions defined in the vtkVolumeProperty are shown here, one for a torso (Figure 7–2) and the other for a head study (Figure 7– 3). In both of these examples, the third transfer function maps the magnitude of the gradient of the scalar value to an opacity multiplier, and is used to enhance the contribution of transition regions of the volume. For example, a large gradient magnitude can be found where the scalar value transitions from air to soft tissue, or soft tissue to bone, while within the soft tissue and bone regions the magnitude remains relatively small. Below is a code fragment that defines a typical gradient opacity transfer function for 8-bit unsigned data.

```tcl
vtkPiecewiseFunction gtfun
gtfun AddPoint 0 0.0
gtfun AddPoint 3 0.0
gtfun AddPoint 6 1.0
gtfun AddPoint 255 1.0
```

This function eliminates nearly homogeneous regions by defining an opacity multiplier of 0.0 for any gradient magnitude less than 3. This multiplier follows a linear ramp from 0.0 to 1.0 on gradient magnitudes between 3 and 6, and no change in the opacity value is performed on samples with magnitudes above 6. Noisier data may require a more aggressive edge detection (so the 3 and the 6 would be higher values). Note that the gradient magnitude transfer function is currently only supported in volume mappers that rendering vtkImageData. For volume mappers that render vtkUnstructuredGrid datasets, gradients are not computed and therefore neither the gradient magnitude transfer function nor shading are available in these mappers.

There are a few methods in vtkVolumeProperty that relate to the color and opacity transfer functions. The SetColor() method accepts either a vtkPiecewiseFunction (if your color function defines only grayscale values) or a vtkColorTransferFunction. You can query the number of color channels with GetColorChannels() which will return 1 if a vtkPiecewiseFunction was set as the color, or 3 if a vtkColorTransferFunction was used to specify color. Once you know how many color channels are in use, you can call either GetGrayTransferFunction() or GetRGBTransferFunction() to get the appropriate function.

The SetScalarOpacity() method accepts a vtkPiecewiseFunction to define the scalar opacity transfer function, and there is a corresponding GetScalarOpacity() method that returns this function. Similarly, there are two methods for the gradient opacity transfer function: SetGradientOpacity() and GetGradientOpacity().

The discussion thus far has considered only single component scalar data where one set of transfer functions define the appearance of the data. Alternatively, multi-component data may be rendered in one of two ways. If the components are independent, then one set of transfer functions can be defined per component. An example of independent data may be an unstructured grid produced through a simulation process that produces both temperature and density values on the grid. Another example of independent components is the data produced by confocal microscopy where the specimen is scanned multiple times with different fluorescent dyes used to highlight different structures within the specimen. When rendering multi-component data where the components are independent, you must define the appearance parameters per component. The SetColor(), SetScalarOpacity(), and SetGradientOpacity() methods accept an optional index value as the first argument to set the transfer function for a specific component. 

Multi-component data may also represent not independent properties, but instead a set of values that define one property. For example, when utilizing a physical sectioning technique, you may have three or four component data representing RGB or RGBA. Or perhaps you have two components representing luminance and alpha. Volume mappers that support multiple components support two forms of non-independent components. The first is two component data where the first component is passed through the color transfer function in order to determine the sample color, and the second component is passed through the scalar opacity function to define the sample alpha. The second type of non-independent multi-component data is four component data where the first three components are taken directly as RGB, and the fourth is passed through the scalar opacity transfer function in order to define alpha. In both of these non-independent cases, the last component is used to compute gradients, and therefore controls the gradient magnitude opacity transfer function as well.

Note that not all mappers support multi-component data, please consult the mapper-specific documentation provided in the remainder of this chapter for further information on supported functionality. For mappers that do support multiple components, the limit is typically four components.

## 7.8 Controlling Shading with a vtkVolumeProperty

Controlling shading of a volume with a volume property is similar to controlling the shading of a geometric actor with a property (see “Actor Properties” on page53 and “Actor Color” on page54). There is a flag for shading, and four basic parameters: the ambient coefficient, the diffuse coefficient, the specular coefficient and the specular power. Generally, the first three coefficients will sum to 1.0 but exceeding this value is often desirable in volume rendering to increase the brightness of a rendered volume. The exact interpretation of these parameters will depend on the illumination equation used by the specific volume rendering technique that is being used. In general, if the ambient term dominates then the volume will appear unshaded, if the diffuse term dominates then the volume will appear rough (like concrete) and if the specular term dominates then the volume will appear smooth (like glass). The specular power can be used to control how smooth the appearance is (such as brushed metal versus polished metal).

By default, shading is off. You must explicitly call ShadeOn() for the shading coefficients to affect the scene. Setting the shading flag off is generally the same as setting the ambient coefficient to 1.0, the diffuse coefficient to 0.0 and the specular coefficient to 0.0. Note that currently volume mappers that render vtkUnstructuredGrid datasets do not support shading. In addition, some volume rendering techniques for vtkImageData, such as volume ray casting with a maximum intensity ray function, do not consider the shading coefficients regardless of the value of the shading flag.

The shaded appearance of a volume (when the shading flag is on) depends not only on the values of the shading coefficients in the vtkVolumeProperty, but also on the collection of light sources contained in the renderer, and their properties. The appearance of a rendered volume will depend on the number, position, and color of the light sources in the scene.

If possible, the volume rendering technique attempts to reproduce the lighting equations defined by OpenGL. Consider the following example.

![Figure 7-4](images/Figure_7-4.png)

*Figure 7–4 A geometric sphere (right) vtkActor actor and a volumetric sphere (left) rendered with the same lighting coefficients.*


```tcl
#Create a geometric sphere
vtkSphereSource sphere
sphere SetRadius 20
sphere SetCenter 70 25 25
sphere SetThetaResolution 50
sphere SetPhiResolution 50
vtkPolyDataMapper mapper
mapper SetInput [sphere GetOutput]
actor SetMapper mapper
[actor GetProperty] SetColor 1 1 1
[actor GetProperty] SetAmbient 0.01
[actor GetProperty] SetDiffuse 0.7
[actor GetProperty] SetSpecular 0.5
[actor GetProperty] SetSpecularPower 70.0
#Read in a volumetric sphere
vtkSLCReader reader
reader SetFileName "$VTK_DATA_ROOT/Data/sphere.slc"
# Use this tfun for both opacity and color
vtkPiecewiseFunction opacityTransferFunction
opacityTransferFunction AddSegment 0 1.0 255 1.0
# Make the volume property match the geometric one
vtkVolumeProperty volumeProperty
volumeProperty SetColor opacityTransferFunction
volumeProperty SetScalarOpacity tfun
volumeProperty ShadeOn
volumeProperty SetInterpolationTypeToLinear
volumeProperty SetDiffuse 0.7
volumeProperty SetAmbient 0.01
volumeProperty SetSpecular 0.5
volumeProperty SetSpecularPower 70.0
vtkVolumeRayCastCompositeFunction compositeFunction
vtkVolumeRayCastMapper volumeMapper
volumeMapper SetInput [reader GetOutput]
volumeMapper SetVolumeRayCastFunction compositeFunction
vtkVolume volume
volume SetMapper volumeMapper
volume SetProperty volumeProperty
# Add both the geometric and volumetric spheres to the renderer
ren1 AddProp volume
ren1 AddProp actor
# Create a red, green, and blue light
vtkLight redlight
redlight SetColor 1 0 0
redlight SetPosition 1000 25 25
redlight SetFocalPoint 25 25 25
redlight SetIntensity 0.5
vtkLight greenlight
greenlight SetColor 0 1 0
greenlight SetPosition 25 1000 25
greenlight SetFocalPoint 25 25 25
greenlight SetIntensity 0.5
vtkLight bluelight
bluelight SetColor 0 0 1
bluelight SetPosition 25 25 1000
bluelight SetFocalPoint 25 25 25
bluelight SetIntensity 0.5
# Add the lights to the renderer
ren1 AddLight redlight
ren1 AddLight greenlight
ren1 AddLight bluelight
#Render it!
renWin Render
```

In the image shown for this example (Figure 7–4), the left sphere is rendered with volumetric ray casting, and the right sphere is rendered with OpenGL using surface rendering. Since the vtkProperty used for the vtkActor, and the vtkVolumeProperty used for the vtkVolume were set up with the same ambient, diffuse, specular, and specular power values, and the color of both spheres is white, they have similar appearances.

When rendering data with multiple independent components, you must set the shading parameters per component. Each of the SetAmbient(), SetDiffuse(), SetSpecular(), and SetSpecularPower() methods takes an optional first parameter indicating the component index. Although the vtkVolumeProperty API allows shading to be enable / disabled independently per component, currently no volume mapper in VTK supports this. Therefore all Shade instance variables should be set On or Off.

## 7.9 Creating a Volume Mapper

vtkAbstractVolumeMapper is an abstract superclass and is never created directly. Instead, you would create a mapper subclass of the specific type desired. In VTK 5.4, the choices for vtkImageData are vtkVolumeRayCastMapper, vtkVolumeTextureMapper2D, vtkFixedPointVolumeRayCastMapper, vtkVolumeTextureMapper3D, or VTKVolumeProVP1000Mapper. For vtkUnstructuredGrid datasets, the available mappers are vtkUnstructuredGridVolumeRayCastMapper, vtkUnstructuredGridZSweepMapper, vtkProjectedTetrahedraMapper, or VTKHAVSVolumeMapper.

All volume mappers support the SetInput() method with an argument of a pointer to a vtkImageData object or a vtkUnstructuredGrid object as appropriate. For vtkImageData volume mappers, each of the rendering techniques support only certain types of vtkImageData. For example, the vtkVolumeRayCastMapper and the vtkVolumeTextureMapper2D both support only VTK_UNSIGNED_CHAR and VTK_UNSIGNED_SHORT data with a single component. The vtkVolumeTextureMapper3D supports any scalar type, but only one component, or multiple nonindependent components. The vtkFixedPointVolumeRayCastMapper is the most flexible, supporting all data types and up to four components.

## 7.10 Cropping a Volume

Since volume rendered images of large, complex volumes can produce images that are difficult to interpret, it is often useful to view only a portion of the volume. The two techniques that can be used to limit the amount of data rendered are known as cropping and clipping.

Cropping is a method of defining visible regions of the structured volume using six planes—two along each of the z max major axes. Cropping is applicable only to volume mappers that operate on vtkImageData. Clipping is applicable to both vtkIm- y ageData and vtkUnstructuredGrid volume mappers. The six z y max min min axis-aligned cropping planes are defined in data coordinates and x x are therefore dependent on the origin and spacing of the data, min max but are independent of any transformation applied to the volume. The most common way to use these six planes is to define a subvolume of interest as shown in the figure to the right.

To crop a subvolume, you must turn cropping on, set the cropping region flags, and set the cropping region planes in the volume mapper as shown below.

```tcl
set xmin 10.0
set xmax 50.0
set ymin 0.0
set ymax 33.0
set zmin 21.0
set zmax 47.0
vtkVolumeRayCastMapper mapper
mapper CroppingOn
mapper SetCroppingRegionPlanes $xmin $xmax $ymin $ymax $zmin $zmax
mapper SetCroppingRegionFlagsToSubVolume
```

Note that the above example is shown for a vtkVolumeRayCastMapper, but it could have instead used any concrete subclass of vtkVolumeMapper since the cropping methods are all defined in the superclass.

The six planes that are defined by the x<sub>min</sub>, x<sub>max</sub> , y<sub>min</sub> , y<sub>max</sub> , z<sub>min</sub> , and z<sub>max</sub> values break the volume into 27 regions (a 3x3 grid). The CroppingRegionFlags is a 27 bit number with one bit representing each of these regions, where a value of 1 indicates that data within that region is visible, and a value of 0 indicating that data within that region will be cropped. The region of the volume Fence Inverted Fence that is less than x , y , and z is represented by min min min the first bit, with regions ordered along the x axis first, then the y axis and finally the z axis.

![Figure 7-5](images/Figure_7-5.png)

*Figure 7–5 Cropping operations.*

The SetCroppingRegionFlagsToSubVolume() method is a convenience method that sets the flags to 0x0002000—just the center region is visible. Although any 27 bit number can be used to define the cropping operation, in practice there are only a few that are used. Four additional convenience methods are provided for setting these flags: SetCroppingRegionFlagsToFence(), SetCroppingResgionFlagsToInvertedFence(), SetCroppingRegionFlagsToCross(), and SetCroppingRegionFlagsToInvertedCross(), as depicted in Figure 7–5.

## 7.11 Clipping a Volume

![Figure 7-6](images/Figure_7-6.png)

*Figure 7–6 Clipping planes are used to define a thick slab.*

In addition to the cropping functionality supplied by the vtkVolumeMapper, arbitrary clipping planes are provided in the vtkAbstractMapper3D. For subclasses of vtkAbstractMapper3D that use OpenGL to perform the clipping in hardware such as vtkPolyDataMapper, vtkVolumeTextureMapper2D, and vtkProjectedTetrahedraMapper, an error message may be displayed if you attempt to use more than the maximum number of clipping planes supported by OpenGL, which is typically 6. Software rendering techniques such as vtkVolumeRayCastMapper can support an arbitrary number of clipping planes. The vtkVolumeProMapper does not support these clipping planes directly, although the class does contain methods for specify ing one clipping box using a plane and a thickness value.

The clipping planes are specified by creating a vtkPlane, defining the plane parameters, then adding this plane to the mapper using the AddClippingPlane() method. One common use of these arbitrary clipping planes in volume rendering is to specify two planes parallel to each other in order to perform a thick reformatting operation. An example of this applied to CT data is shown in Figure 7–6. For unstructured data, clipping planes can be used essentially as cropping planes to view only a subregion of the data, which is often necessary when trying to visualize internal details in a complex structure.

## 7.12 Controlling the Normal Encoding

The standard illumination equation relies on a surface normal in order to calculate the diffuse and specular components of shading. In volume rendering of vtkImageData, the gradient at a location in the volumetric data is considered to point in the opposite direction of the “surface normal” at that location. A finite differences technique is typically used to estimate the gradient, but this tends to be an expensive calculation, and would make shaded volume rendering prohibitively slow if it had to be performed at every sample along every ray.

One way to avoid these expensive computations is to precompute the normals at the grid locations, and to use some form of interpolation in between. If done naively, this would require three floating point numbers per location, and we would still need to take a square root to determine the magnitude. Alternatively, we could store the magnitude so that each normal would require four floating point values. Since volumes tend to be quite large, this technique requires too much memory, so we must somehow quantize the normals into a smaller number of bytes.

In some of the VTKImageData volume mappers we have chosen to quantize the normal direction into two byes, and the magnitude into one. The calculation of the normal is performed by a subclass of vtkEncodedGradientEstimator (currently only vtkFiniteDifferenceGradientEstimator) and the encoding of the direction into two bytes is performed by a subclass of vtkDirectionEncoder (currently vtkRecursiveSphere-DirectionEncoder and VTKSphericalDirectionEncoder). For mappers that use normal encoding (vtkVolumeRayCastMapper and vtkVolumeTextureMapper2D), these objects are created automatically so the typical user need not be concerned with these objects. In the case where one volume dataset is to be rendered by multiple mappers into the same image, it is often useful to create one gradient estimator for use by all the mappers. This will conserve space and computational time since otherwise there would be one copy of the normal volume per mapper. An example fragment of code is shown below:

```tcl
# Create the gradient estimator
vtkFiniteDifferenceGradientEstimator gradientEstimator
# Create the first mapper
vtkVolumeRayCastMapper volumeMapper1
volumeMapper1 SetGradientEstimator gradientEstimator
volumeMapper1 SetInput [reader GetOutput]
# Create the second mapper
vtkVolumeRayCastMapper volumeMapper2
volumeMapper2 SetGradientEstimator gradientEstimator
volumeMapper2 SetInput [reader GetOutput]
```

If you set the gradient estimator to the same object in two different mappers, then it is important that these mappers have the same input. Otherwise, the gradient estimator will be out-of-date each time the mapper asks for the normals, and will regenerate them for each volume during every frame rendered. In the above example, the direction encoding objects were not explicitly created, therefore each gradient estimator created its own encoding object. Since this object does not have any significant storage requirements, this is generally an acceptable situation. Alternatively, one vtkRecursiveSphereDirectionEncoder could be created, and the SetDirectionEncoder() method would be used on each estimator.

![Figure 7-7](images/Figure_7-7.png)

*Figure 7–7 Volume rendering via ray casting.*

The vtkFixedPointVolumeRayCastMapper class does support shading and does use these same gradient estimators and normal encoders, but these classes are not exposed at the API level and therefore encoded normals cannot be shared between mappers. The vtkVolumeTextureMapper3D class* also supports shading, but does so by storing a 3 byte representation of the normal directly in texture memory.

## 7.13 Volumetric Ray Casting for vtkImageData

The vtkVolumeRayCastMapper is a volume mapper that employs a software ray casting technique to perform volume rendering. It is generally the most accurate mapper, and also the slowest on most platforms. The ray caster is threaded to make use of multiple processors when available.

There are a few parameters that are specific to volume ray casting that have not yet been discussed. First, there is the ray cast function that must be set in the mapper. This is the object that does the actual work of considering the data values along the ray and determining a final RGBA value to return. Currently, there are three supported subclasses of vtkVolumeRayCastFunction: the vtkVolumeRayCastIsosurfaceFunction that can be used to render isosurfaces within the volumetric data, the vtkVolumeRayCastMIPFunction that can be used to generate maximum intensity projections of the volume, and vtkVolumeRayCastCompositeFunction that can be used to render the volume with an alpha compositing technique. An example of the images that can be generated using these different methods is Figure 7–7. The upper left image was generated using a maximum intensity projection. The other two upper images were generated using compositing, while the lower two images were generated using an isosurface function. Note that it is not always easy to distinguish an image generated using a compositing technique from one generated using an isosurface technique, especially when a sharp opacity ramp is used

There are some parameters that can be set in each of the ray cast functions that impact the rendering process. In vtkVolumeRayCastIsosurfaceFunction, there is a SetIsoValue() method that can be used to set the value of the rendered isosurface. In vtkVolumeRayCastMIPFunction, you can call SetMaximizeMethodToScalarValue() (the default) or SetMaximizeMethodToOpacity() to change the behavior of the maximize operation. In the first case, the scalar value is considered at each sample point along the ray. The sample point with the largest scalar value is selected, then this scalar value is passed through the color and opacity transfer functions to produce a final ray value. If the second method is called, the opacity of the sample is computed at each step along the ray, and the sample with the highest opacity value is selected.

![Figure 7-8](images/Figure_7-8.png)
*Figure 7–8 The effect of interpolation order in composite ray casting.*

In vtkVolumeRayCastCompositeFunction, you can call SetCompositeMethodToInterpolateFirst() (the default) or SetCompositeMethodToClassifyFirst() to change the order of interpolation and classification (Figure 7–8). This setting will only have an impact when trilinear interpolation is being used. In the first case, interpolation will be performed to determine the scalar value at the sample point, then this value will be used for classification (the application of the color and opacity transfer functions). In the second case, classification is done at the eight vertices of the cell containing the sample location, then Classify First the final RGBA value is interpolated from the computed RGBA values at the vertex locations. Interpolating first generally produces “prettier” images as can be seen on the left where a geometric sphere is contained within a volumetric “distance to point” field, with the transfer functions defined to highlight three concentric spherical shells in the volume. The interpolate first method makes the underlying assumption that if two neighboring data points have values of 10 and 100, then a value of 50 exists somewhere between the two data points. In the case where material is being classified by scalar value, this may not be the case. For example, consider CT data where values below Interpolate First 20 are air (transparent), values from 20 to 80 are soft tissue, and values above 80 are bone. If interpolation is performed first, then bone can never be adjacent to air - there must always be  soft tissue between the bone and air. This is not true inside the mouth where teeth meet air. If you render an image with interpolation performed first and a high enough sample rate, it will look like the teeth have a layer of skin on top of them.

![Figure 7-9](images/Figure_7-9.png)
*Figure 7-9 Different methods for interpolation. On the left, nearest neighbor interpolation. On the right, trilinear interpolation.

The value of the interpolation type instance variable in the vtkVolumeProperty is important to ray casting. There are two options: SetInterpolationTypeToNearest() (the default) which will use a nearest neighbor approximation when sampling along the ray, and SetInterpolationTypeToLinear() which will use trilinear interpolation during sampling. Using the trilinear interpolation produces smoother images with less artifacts, but generally takes a bit longer. The difference in image quality obtained with these two methods is shown in Figure 7–9. A sphere is voxelized into a 50x50x50 voxel volume, and rendered using alpha compositing with nearest neighbor interpolation on the left and trilinear interpolation on the right. In the image of the full sphere it may be difficult to distinguish between the two interpolation methods, but by zooming up on just a portion of the sphere it is easy to see the individual voxels in the left image.

Another parameter of vtkVolumeRayCastMapper that affects the image is the SampleDistance. This is the distance in world coordinates between sample points for ray functions that take samples. For example, the alpha compositing ray function performs a discrete approximation of the continuous volume rendering integral by sampling along the ray. The accuracy of the approximation increases with the number of samples taken, but unfortunately so does the rendering time. The maximum intensity ray function also takes samples to locate the maximum value. The isosurface ray function does not take samples but instead computes the exact location of the intersection according to the current interpolation function.

By default samples are taken 1 unit apart in world coordinates. In practice you should adjust this spacing based on the sample spacing of the 3D data being rendered, and the rate of change of not only the scalar values but also the color and opacity assigned to the scalar values through the transfer functions. An example is shown below of a voxelized vase with a 1x1x1 spacing between samples in the dataset. The scalar values vary smoothly in the data, but a sharp change has been introduced in the transfer functions by having the color change rapidly from black to white. You can clearly see artifacts of the “undersampling” of ray casting in the image created with a step size of 2.0. Even with a step size of 1.0 there are some artifacts since the color of the vase changes significantly within a world space distance of 1.0. If the sample distance is set to 0.1 the image appears smooth. Of course, this smooth image on the left takes nearly 20 times as long to generate as the one on the right.

![Figure 7-10](images/Figure_7-10.png)

*Figure 7–10 The effects or varying sample distance along the ray. As the sample distance increases, sampling artifacts create the dramatic black and white banding. However, the cost of volume rendering increases inversely proportional to the sample size, i.e., the difference in rendering time for sample distance 0.1 is 20x faster than for 2.0.*

## 7.14 Fixed Point Ray Casting

The vtkFixedPointVolumeRayCastMapper is a volume mapper for vtkImageData that employs fixed point arithmetic in order to improve performance. The vtkFixedPointVolumeRayCastMapper supports all scalar types from unsigned char through double, and supports up to four independent components, each with their own transfer functions and shading parameters. In addition, this mapper supports two varieties of non-independent multi-component data. The first variety is two component data where the first component is used to look up a color, while the second component is used to derive a normal value and to look up opacity. This is useful when some property such as density is stored in the second component, while the first is used as perhaps an index to indicate different material types that can each have their own color, opacity, and shading style. The second variety is four component unsigned char data where the first three components directly represent RGB, with the fourth passed through the scalar opacity transfer function to obtain alpha.

The vtkFixedPointVolumeRayCastMapper employs a form of space leaping to avoid processing in “empty” (entirely transparent) regions of the volume. Early ray termination is also employed to terminate processing once full opacity is reached. Therefore, significant performance improvements can be obtained when rendering data with a sharp “surface” appearance.

## 7.15 2D Texture Mapping

As an alternative to ray casting, volume rendering of vtkImageData can be performed by texture mapping the volume onto polygons, and projecting these with the graphics hardware. If your graphic board provides reasonable texture mapping acceleration, this method will be significantly faster than ray casting, but at the expense of accuracy since partial accumulation results are stored at the resolution of the framebuffer (usually 8 or less bits per component) rather than in floating point. To use 2D texture mapping, quads are generated along the axis of the volume which is most closely aligned with the viewing direction. As the viewing direction changes, the sample distance between quads will change, and at some point the set of quads will jump to a new axis which may cause temporal artifacts. Generally these artifacts will be most noticeable on small volumes.

The current implementation of vtkVolumeTextureMapper2D supports only alpha compositing. Bilinear interpolation on the slice is used for texture mapping but since quads are only created on the data planes, there is no notion of interpolation between slices. Therefore, the value of the InterpolationType instance variable in the vtkVolumeProperty is ignored by this mapper.

Shading is supported in software for the texture mapping approach. If shading is turned off in the vtkVolumeProperty, then software shading calculations do not need to be performed, and therefore the performance of this mapper will be better than if shading is turned on.

## 7.16 3D Texture Mapping

Most current graphics cards now support 3D texture mapping where a three-dimensional buffer is stored on the graphics boards and accessed using 3D texture coordinates. A vtkImageData volume may then be rendered by storing this volume as a texture and projecting a set of polygons parallel to the view plane. This removes the “popping” artifacts inherent in the 2D texture mapping approach since there is no longer a sudden change in underlying geometry based on major viewing direction. However, the 3D texture mapping approach currently available in VTK uses the frame buffer for compositing, which is still generally limited to 8 bits. Therefore with large volumes that are fairly translucent, banding artifacts will occur and small features may be lost in the image.

The 3D texture mapper is a single-pass mapper that requires the entire volume to be in memory. Therefore a limit is placed on the size of the data transferred to the texture memory. This limit is based on the type of the data, the number of components, the texture memory available on the graphics board, and some hard-coded limits used to avoid problems in buggy OpenGL drivers that report the ability to utilize more texture memory than truly available. This is a silent limit - the input data set will be downsampled to fit within the available texture memory with no warning or error messages produced. This mapper supports single component data or any scalar type, and four component dependent data (RGBA) that is unsigned char. For single component data, the hard-coded limit is 256x256x128 voxels, with any aspect ratio provided that each dimension is a power of two. With four component data, the limit is 256x128x128 voxels.

The 3D volume texture mapper supports two main families of graphics hardware: nVidia and ATI. There are two different implementations of 3D texture mapping used - one based on the GL_NV_texture_shader2 and GL_NV_register_combiners2 extensions (supported on some older nVidia cards), and one based on the GL_ARB_fragment_shader extension (supported by most current nVidia and ATI boards). To use this class in an application that will run on various hardware configurations, you should have a back-up volume rendering method. You should create a vtkVolumeTextureMapper3D, assign its input, make sure you have a current OpenGL context (you've rendered at least once), then call IsRenderSupported() with a vtkVolumeProperty as an argument. This method will return 0 if the input has more than one independent component, or if the graphics hardware does not support the set of required extensions for using at least one of the two implemented methods.

## 7.17 Volumetric Ray Casting for vtkUnstructuredGrid

The vtkUnstructuredGridVolumeRayCastMapper is a volume mapper that employs a software ray casting technique to perform volume rendering on unstructured grids. Using the default ray cast function and integration methods, this mapper is more accurate than the vtkProjectedTetrahedra method, but is also significantly slower. This mapper is generally faster than the vtkUnstructuredGridZSweepMapper, but obtains this speed at the cost of memory consumption and is therefore best used with small unstructured grids. The ray caster is threaded to make use of multiple processors when available. As with all mappers that render vtkUnstructuredGrid data, this mapper requires that the input dataset is composed entirely of tetrahedral elements, and may employ a filter to tetrahedralize the input data if necessary.

This ray cast mapper is customizable in two ways. First, you may specify the method used to traverse the ray through the unstructured grid using the SetRayCastFunction() method. The specified function must be a subclass of vtkUnstructuredGridVolumeRayCastFunction. Currently one such subclass exists within VTK: vtkUnstructuredGridBunykRayCastFunction. This class is based on the method described in "Simple, Fast, Robust Ray Casting of Irregular Grids" by Paul Bunyk, Arie Kaufman, and Claudio Silva. This method is quite memory intensive (with extra explicit copies of the data) and therefore should not be used for very large data.

![Figure 7-11](images/Figure_7-11.png)

*Figure 7–11 Comparison of three volume rendering techniques for vtkUnstructuredGrid datasets.*

You may also specify a method for integrating along the ray between the front entry point and back exit point for the length of ray intersecting a tetrahedra using the SetRayIntegrator() method. The specified method must be a subclass of vtkUnstructuredGridVolumeRayIntegrator. Several available subclasses exist in VTK, and when left unspecified the mapper will select an appropriate subclass for you. The vtkUnstructuredGridHomogeneousRayIntegrator class is applicable when rendering cell scalars. The vtkUnstructuredGridLinearRayIntegrator performs piecewise linear ray integration. Considering that transfer functions in VTK 5.4 are piecewise linear, this class should give
the "correct" integration under most circumstances. However, the computations performed are fairly hefty and should, for the most part, only be used as a benchmark for other, faster methods. The vtkUnstructuredGridPartialPreIntegration also performs piecewise linear ray integration, and will give the same results as vtkUnstructuredGridLinearRayIntegration (with potentially an error due to table lookup quantization), but should be notably faster. The algorithm used is given by Moreland and Angel, "A Fast High Accuracy Volume Renderer for Unstructured Data." The vtkUnstructuredGridPreIntegration performs ray integration by looking into a precomputed table. The result should be equivalent to that computed by vtkUnstructuredGridLinearRayIntegrator and vtkUnstructuredGridPartialPreIntegration, but faster than either one. The pre-integration algorithm was first introduced by Roettger, Kraus, and Ertl in "Hardware-Accelerated Volume And Isosurface Rendering Based On Cell-Projection."

Similar to the structured ray cast mapper, the unstructured grid ray cast mapper will automatically adjust the number of rays cast in order to achieve a desired update rate. Since this is a softwareonly technique, this method utilizes multiple processors when available to improve performance.

## 7.18 ZSweep

The vtkUnstructuredGridVolumeZSweepMapper rendering method is based on an algorithm described in “ZSWEEP: An Efficient and Exact Projection Algorithm for Unstructured Volume Rendering” by Ricardo Farias, Joseph S. B. Mitchell and Claudio T. Silva. This is a software projection technique that will work on any platform, but is generally the slowest of the unstructured grid volume rendering methods available in VTK. It is less memory intensive than the ray cast mapper (using the Bunyk function) and is therefore able to render larger volumes. Similar to the ray cast mapper, the specific ray integrator may be specified using the SetRayIntegrator() method. Again, leaving this as NULL will allow the mapper to select an appropriate integrator for you.

## 7.19 Projected Tetrahedra

The vtkProjectedTetrahedraMapper rendering method is an implementation of the classic Projected Tetrahedra algorithm presented by Shirley and Tuchman in "A Polygonal Approximation to Direct Scalar Volume Rendering". This method utilizes OpenGL to improve rendering performance by converting tetrahedra into triangles for a given view point, then rendering these triangles with hardware acceleration. However, the OpenGL methods utilized in this class are not necessarily supported by all driver implementations, and may produce artifacts. Typically this mapper will be used in conjunction with either the ray caster or the ZSweep mapper to form a level-of-detail approach that provides fast rendering during interactivity followed by a more accurate technique to produce the final image.

In Figure 7–11 you can see a comparison of images generated with the three techniques for volume rendering unstructured grids. The projected tetrahedra technique is interactive, while the other two technique require a few seconds per image on a standard desktop system.

The vtkHAVSVolumeMapper is an implementation of the algorithm presented in "HardwareAssisted Visibility Sorting for Unstructured Volume Rendering" by S. P. Callahan, M. Ikits, J. L. D. Comba, and C. T. Silva.

The code was written and contributed by Steven P. Callahan. The Hardware-Assisted Visibility Sorting (HAVS) algorithm works by first sorting the triangles of the tetrahedral mesh in object space, then they are sorted in image space using a fixed size A-buffer implemented on the GPU called the k buffer. The HAVS algorithm excels at rendering large datasets quickly. The trade-off is that the algorithm may produce some rendering artifacts due to an insufficient k size (currently 2 or 6 is supported) or read/write race conditions.

A built in level-of-detail (LOD) approach samples the geometry using one of two heuristics (field or area). If LOD is enabled, the amount of geometry that is sampled and rendered changes dynamically to stay within the target frame rate. The field sampling method generally works best for datasets with cell sizes that don't vary much in size. On the contrary, the area sampling approach gives better approximations when the volume has a lot of variation in cell size. For more information on the level-of-detail method, please see "Interactive Rendering of Large Unstructured Grids Using Dynamic Level-of-Detail" by S. P. Callahan, J. L. D. Comba, P. Shirley, and C. T. Silva.

The HAVS algorithm uses several advanced features on graphics hardware. The k-buffer sorting network is implemented using framebuffer objects (FBOs) with multiple render targets (MRTs). Therefore, only cards that support these features can run the algorithm (at least an ATI 9500 or an NVidia NV40 (6600)).

## 7.20 Speed vs. Accuracy Trade-offs

If you do not have a VolumePro volume rendering board, many fast CPUs, or high-end graphics hardware, you will probably not be satisfied with the rendering rates achieved when one or more volumes are rendered in a scene. It is often necessary to achieve a certain frame rate in order to effectively interact with the data, and it may be necessary to trade off accuracy in order to achieve speed. Fortunately, there are ways to do this for many of the volume rendering approach. In fact, several of them will provide this functionality for you automatically by determining an appropriate accuracy level in order to obtain the desired update rate specified in the vtkRenderWindow.

![Figure 7-12](images/Figure_7-12.png)
*Figure 7–12 The effect of changing image sample distance on image quality.*

The support for achieving a desired frame rate for vtkVolumeRayCastMapper, vtkFixedPointVolumeRayCastMapper, vtkUnstructuredGridVolumeRayCastMapper, and vtkUnstructuredGridVolumeZSweepMapper is available by default in VTK. You can set the desired update rate in the vtkRenderWindow, or the StillUpdateRate and the DesiredUpdateRate in the interactor if you are using one. Due to the fact that the time required for these rendering techniques is mostly dependent on the size of the image, the mapper will automatically attempt to achieve the desired rendering rate by reducing the number of rays that arecast, or the size of the image is generated. By default, the automatic adjustment is on. In order to maintain interactivity, an abort check procedure should be specified in the render window so that the user will be able to interrupt the higher resolution image in order to interact with the data again.

There are limits on how blocky the image will become in order to achieve the desired update rate. By default, the adjustment will allow the image to become quite blocky - for example, casting only 1 ray for every 10x10 neighborhood of pixels if necessary to achieve the desired update rate. Also by default these mappers will not generate an image larger than necessary to fill the window on the screen. These limits can be adjusted in the mapper by setting the MinimumImageSampleDistance and MaximumImageSampleDistance. In addition AutoAdjustSampleDistances can be turned off, and the specified ImageSampleDistance will be used to represent the spacing between adjacent pixels on the image plane. Results for one example are shown in Figure 7–12.

This technique of reducing the number of rays in order to achieve interactive frame rates can be quite effective. For example, consider the full resolution image shown on the left in Figure 7–12. This image may require 4 seconds to compute, which is much too slow for data interaction such as rotating or translating the data, or interactively adjusting the transfer function. If we instead subsample every other ray along each axis by setting the ImageSampleDistance to 2.0, we will get an image like the one shown in the middle in only about 1 second. Since this still may be too slow for effective interaction, we could subsample every fourth ray, and achieve rendering rates of nearly 4 frames per second with the image shown on the right. It may be blocky, but it is far easier to rotate a blocky volume at 4 frames per second than a full resolution volume at one frame every four seconds.

There are no built-in automatic techniques for trading off accuracy for speed in a texture mapping approach. This can be done by the user fairly easily by creating a lower resolution volume using vtkImageResample, and rendering this new volume instead. Since the speed of the texture mapping approach is highly dependent on the size of the volume, this will achieve similar results to reducing the number of rays in a ray casting approach. Another option is to reduce the number of planes sampled through the volume. By default, the number of textured quads rendered will be equal to the number of samples along the major axis of the volume (as determined by the viewing direction). You may set the MaximumNumberOfPlanes instance variable to decrease the number of textured quads and

## 7.21 Using a vtkLODProp3D to Improve Performance

The vtkLODProp3D is a 3D prop that allows for the collection of multiple levels-of-detail and decides which to render for each frame based on the allocated rendering time of the prop (see “vtkLODProp3D” on page57). The allocated rendering time of a prop is dependent on the desired update rate for the rendering window, the number of renderers in the render window, the number of props in the renderer, and any possible adjustment that a culler may have made based on screen coverage or other importance factors. 

Using a vtkLODProp3D, it is possible to collect several rendering techniques into one prop, and allow the prop to decide which technique to use. These techniques may span several different classes of rendering including geometric approaches that utilize a vtkPolyDataMapper, and volumetric methods for both structured and unstructured data.

Consider the following simple example of creating a vtkLODProp3D with three different forms of volume rendering for vtkImageData:

```tcl
vtkImageResample resampler
resampler SetAxisMagnificationFactor 0 0.5
resampler SetAxisMagnificationFactor 1 0.5
resampler SetAxisMagnificationFactor 2 0.5
vtkVolumeTextureMapper2D lowresMapper
lowresMapper SetInput [resampler GetOutput]
vtkVolumeTextureMapper2D medresMapper
medresMapper SetInput [reader GetOutput]
vtkVolumeRayCastMapper hiresMapper
hiresMapper SetInput [reader GetOutput]
vtkLODProp3D volumeLOD
volumeLOD AddLOD lowresMapper volumeProperty 0.0
volumeLOD AddLOD medresMapper volumeProperty 0.0
volumeLOD AddLOD hiresMapper volumeProperty 0.0
```

For clarity, many steps of reading the data and setting up visualization parameters have been left out of this example. At render time, one of the three levels-of-detail (LOD) for this prop will be selected based on the estimated time that it will take to render the LODs and the allocated time for this prop. In this case, all three LODs use the same property, but they could have used different properties if desired. Also, in this case all three mappers are subclasses of vtkVolumeMapper, but we could add a bounding box representation as another LOD. If we are rendering a large vtkUnstructuredGrid dataset, we could form an LOD by adding an outline representation using a vtkPolyDataMapper for the lowest resolution, we could resample the data into a vtkImageData and add a level-of-detail that renders this with 3D texture mapping, and we could add the full resolution unstructured data rendered with the ZSweep mapper as the best level-of-detail.

The last parameter of the AddLOD() method is an initial time to use for the estimated time required to render this level-of-detail. Setting this value to 0.0 requires that the LOD be rendered once before an estimated render time can be determined. When a vtkLODProp3D has to decide which LOD to render, it will choose one with 0.0 estimated render time if there are any. Otherwise, it will choose the LOD with the greatest time that does not exceed the allocated render time of the prop, if it can find such an LOD. Otherwise, it will choose the LOD with the lowest estimated render time. The time required to draw an LOD for the current frame replaces the estimated render time of that LOD for future frames.
