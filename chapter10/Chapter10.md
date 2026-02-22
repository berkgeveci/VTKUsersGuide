# Chapter 10: Building Models

We have seen how to use source objects (both readers and procedural objects) to create geometry. (See Section 4.1.) VTK provides several other techniques to generate more complex models. Three techniques covered in this chapter are implicit modeling, extrusion, and surface reconstruction from unorganized points.

If you are working with data in a form that lacks topological or geometric structure, VTK can represent this information as field data (using class vtkDataObject), which can be further processed to produce datasets for visualization with the techniques in this chapter. For example, an n-dimensional financial record can be reduced to three dimensions by choosing three variables as independent variables. Then the techniques described here—Delaunay triangulation, Gaussian splatting, and surface reconstruction—can be used to create structure suitable for visualization by standard methods.

## 10.1 Implicit Modeling

Implicit modeling is a powerful technique employing 3D contouring (isosurface generation) to create polygonal surface meshes. The contouring operation is applied to a vtkImageData dataset (a regular volume) whose scalar values have been synthetically generated. The key to implicit modeling is that the scalar field can be generated using a wide variety of techniques. These techniques include producing a distance field from generating primitives (e.g., a field representing the distance from a set of lines and/or polygons) as well as using boolean set operations to combine the scalar fields.

### Creating An Implicit Model

Here's an example that uses some lines to generate a complex, polygonal surface. The lines are arranged to spell the word "HELLO" and serve as the generating seed geometry (Figure 10–1).

![Figure 10-1](images/Figure_10-1.png)

*Figure 10–1 Implicit modeling from lines spelling the word "hello."*

```python
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# Create lines which serve as the "seed" geometry
reader = vtkPolyDataReader()
reader.SetFileName("hello.vtk")

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(reader.GetOutputPort())
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Create implicit model with distance field and contour it
imp = vtkImplicitModeller()
imp.SetInputConnection(reader.GetOutputPort())
imp.SetSampleDimensions(110, 40, 20)
imp.SetMaximumDistance(0.25)
imp.SetModelBounds(-1.0, 10.0, -1.0, 3.0, -1.0, 1.0)

contour = vtkContourFilter()
contour.SetInputConnection(imp.GetOutputPort())
contour.SetValue(0, 0.25)

imp_mapper = vtkPolyDataMapper()
imp_mapper.SetInputConnection(contour.GetOutputPort())
imp_mapper.ScalarVisibilityOff()

imp_actor = vtkActor()
imp_actor.SetMapper(imp_mapper)
imp_actor.GetProperty().SetColor(0.2, 0.6, 0.6)
imp_actor.GetProperty().SetOpacity(0.5)
```

What's happening in this script is that the lines that stroke out the word "hello" serve as the generating primitives. The vtkImplicitModeller class computes the distance from the lines (taking the closest distance to any line) to the points in the output vtkImageData and assigns this distance as the scalar value at each point in the dataset. The output is then passed to the vtkContourFilter which generates a polygonal isosurface. (The isosurface value is the distance from the generating primitives.)

There are a couple of important parameters in vtkImplicitModeller. The MaximumDistance instance variable controls how far from the generating primitives to continue the distance calculation. This instance variable, expressed as a fraction of the grid length, has a great effect on the speed of calculation: smaller values result in faster computation, but the isosurface may become choppy or break up if the values are too small. The SampleDimensions instance variable controls the resolution of the output vtkImageData, and ModelBounds controls the position and size of the dataset in space.

### Sampling Implicit Functions

Another powerful modeling technique is the use of implicit functions. Implicit functions have the form

$F(x,y,z) = constant$

Spheres, cones, ellipsoids, planes, and many other useful geometric entities can be described with implicit functions. For example, a sphere S of radius R centered at the origin can be described by the equation $F(x,y,z) = R^2 - x^2 - y^2 - z^2$. When $F(x,y,z)=0$, the equation describes S exactly. When $F(x,y,z) < 0$, we describe a sphere that lies inside the sphere S, and when $F(x,y,z) > 0$, we describe a sphere that lies outside the sphere S. As its name implies, an implicit function defines a surface implicitly; producing an explicit representation of the surface (e.g., polygons) requires sampling the function over a volume and then performing an isocontouring operation as demonstrated in the next example.

![Figure 10-2](images/Figure_10-2.png)

*Figure 10–2 Implicit modeling using boolean combinations.*

Besides modeling, implicit functions can also be combined using the set operations union, intersection, and difference. These operations allow you to create complex geometry using combinations of implicit functions. Here's an example script that models an ice cream cone by using a sphere (ice cream), a cone intersected by two planes (to create a cone of finite extent), and another sphere to simulate the "bite" out of the ice cream.

```python
from vtkmodules.vtkCommonDataModel import (
    vtkCone, vtkImplicitBoolean, vtkPlane, vtkSphere,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

# Create implicit function primitives
cone = vtkCone()
cone.SetAngle(20)
vert_plane = vtkPlane()
vert_plane.SetOrigin(0.1, 0, 0)
vert_plane.SetNormal(-1, 0, 0)
base_plane = vtkPlane()
base_plane.SetOrigin(1.2, 0, 0)
base_plane.SetNormal(1, 0, 0)
ice_cream = vtkSphere()
ice_cream.SetCenter(1.333, 0, 0)
ice_cream.SetRadius(0.5)
bite = vtkSphere()
bite.SetCenter(1.5, 0, 0.5)
bite.SetRadius(0.25)

# Combine primitives to build ice-cream cone
the_cone = vtkImplicitBoolean()
the_cone.SetOperationTypeToIntersection()
the_cone.AddFunction(cone)
the_cone.AddFunction(vert_plane)
the_cone.AddFunction(base_plane)

# Take a bite out of the ice cream
the_cream = vtkImplicitBoolean()
the_cream.SetOperationTypeToDifference()
the_cream.AddFunction(ice_cream)
the_cream.AddFunction(bite)

# Sample and contour the cone
cone_sample = vtkSampleFunction()
cone_sample.SetImplicitFunction(the_cone)
cone_sample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
cone_sample.SetSampleDimensions(60, 60, 60)
cone_sample.ComputeNormalsOff()

cone_surface = vtkContourFilter()
cone_surface.SetInputConnection(cone_sample.GetOutputPort())
cone_surface.SetValue(0, 0.0)
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_surface.GetOutputPort())
cone_mapper.ScalarVisibilityOff()
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(0.82, 0.41, 0.12)  # chocolate

# Sample and contour the ice cream
cream_sample = vtkSampleFunction()
cream_sample.SetImplicitFunction(the_cream)
cream_sample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
cream_sample.SetSampleDimensions(60, 60, 60)
cream_sample.ComputeNormalsOff()

cream_surface = vtkContourFilter()
cream_surface.SetInputConnection(cream_sample.GetOutputPort())
cream_surface.SetValue(0, 0.0)
cream_mapper = vtkPolyDataMapper()
cream_mapper.SetInputConnection(cream_surface.GetOutputPort())
cream_mapper.ScalarVisibilityOff()
cream_actor = vtkActor()
cream_actor.SetMapper(cream_mapper)
cream_actor.GetProperty().SetColor(0.74, 0.99, 0.79)  # mint
```

The classes vtkSampleFunction and vtkContourFilter are the keys to building the polygonal geometry. vtkSampleFunction evaluates the implicit function (actually the boolean combination of implicit functions) to generate scalars across a volume (vtkImageData) dataset. vtkContourFilter is then used to generate an isosurface which approximates the implicit function. The accuracy of the approximation depends on the nature of the implicit function, as well as the resolution of the volume generated by vtkSampleFunction (specified using the `SetSampleDimensions()` method).

A couple of usage notes: Boolean combinations can be nested to arbitrary depth. Just make sure the hierarchy does not contain self-referencing loops. Also, you may wish to use vtkDecimatePro to reduce the number of primitives output by the contour filter since the number of triangles can be quite large. See Section 5.6 for more information.

## 10.2 Extrusion

![Figure 10-3](images/Figure_10-3.png)

*Figure 10–3 Rotational extrusion.*

Extrusion is a modeling technique that sweeps a generating object along a path to create a surface. For example, we can sweep a line in a direction perpendicular to it to create a plane.

The Visualization Toolkit offers two methods of extrusion: linear extrusion and rotational extrusion. In VTK, the generating object is a vtkPolyData dataset. Lines, vertices, and "free edges" (edges used by only one polygon) are used to generate the extruded surface. The vtkLinearExtrusionFilter sweeps the generating primitives along a straight line path; the vtkRotationalExtrusionFilter sweeps them along a rotational path. (Translation during rotation is also possible.)

In this example we will use an octagonal polygon (i.e., an approximation to a disk) to sweep out a combined rotational/translational path to model a "spring" (Figure 10–3). The filter extrudes its input (generating primitives) around the z axis while also translating (during rotation) along the z axis and adjusting the sweep radius. By default, the instance variable Capping is on, so the extruded surface (a hollow tube) is capped by the generating primitive. Also, we must set the Resolution instance variable to generate a reasonable approximation.

```python
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

# Create spring profile (an octagonal approximation to a disk)
points = vtkPoints()
points.InsertPoint(0, 1.0, 0.0, 0.0)
points.InsertPoint(1, 1.0732, 0.0, -0.1768)
points.InsertPoint(2, 1.25, 0.0, -0.25)
points.InsertPoint(3, 1.4268, 0.0, -0.1768)
points.InsertPoint(4, 1.5, 0.0, 0.0)
points.InsertPoint(5, 1.4268, 0.0, 0.1768)
points.InsertPoint(6, 1.25, 0.0, 0.25)
points.InsertPoint(7, 1.0732, 0.0, 0.1768)

poly = vtkCellArray()
poly.InsertNextCell(8, [0, 1, 2, 3, 4, 5, 6, 7])

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetPolys(poly)

# Extrude profile to make spring
extrude = vtkRotationalExtrusionFilter()
extrude.SetInputData(profile)
extrude.SetResolution(360)
extrude.SetTranslation(6)
extrude.SetDeltaRadius(1.0)
extrude.SetAngle(2160.0)  # six revolutions

normals = vtkPolyDataNormals()
normals.SetInputConnection(extrude.GetOutputPort())
normals.SetFeatureAngle(60)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

spring = vtkActor()
spring.SetMapper(mapper)
spring.GetProperty().SetColor(0.69, 0.77, 0.87)
spring.GetProperty().SetDiffuse(0.7)
spring.GetProperty().SetSpecular(0.4)
spring.GetProperty().SetSpecularPower(20)
spring.GetProperty().BackfaceCullingOn()
```

The vtkLinearExtrusionFilter is similar, but it is simpler to use than vtkRotationalExtrusionFilter. Linear extrusion can be performed along a user-specified vector (`SetExtrusionTypeToVectorExtrusion()`) or towards a user-specified point (`SetExtrusionTypeToPointExtrusion()`); or the extrusion can be performed in the direction of the surface normals of the generating surface (`SetExtrusionTypeToNormalExtrusion()`).

## 10.3 Constructing Surfaces

Often we wish to construct a surface from a set of unstructured points or other data. The points may come from a laser digitizing system or may be assembled from multi-variate data. In this section we examine techniques to build new surfaces from data of this form. You may also wish to refer to Section 10.1 for other methods to create surfaces from generating primitives (i.e., implicit modeling).

### Delaunay Triangulation

The Delaunay triangulation is widely used in computational geometry. The basic application of the Delaunay triangulation is to create a simplicial mesh (i.e., triangles in 2D, tetrahedra in 3D) from a set of points. The resulting mesh can then be used in a variety of ways, including processing with standard visualization techniques. In VTK, there are two objects for creating Delaunay triangulations: vtkDelaunay2D and vtkDelaunay3D.

**vtkDelaunay2D.** The vtkDelaunay2D object takes vtkPointSet (or any of its subclasses) as input and generates a vtkPolyData on output. Typically the output is a triangle mesh, but if you use a non-zero Alpha value it is possible to generate meshes consisting of triangles, lines, and vertices. (This parameter controls the "size" of output primitives. The size of the primitive is measured by an n-dimensional circumsphere; only those pieces of the mesh whose circumsphere has a circumradius less than or equal to the alpha value are sent to the output. For example, if an edge of length L is less than 2*Alpha, the edge would be output).

In the following example we generate points using a random distribution in the (0,1) x-y plane. (vtkDelaunay2D ignores the z-component during execution, although it does output the z value.) To create a nicer picture we use vtkTubeFilter and vtkGlyph3D to create tubes around mesh edges and spheres around the mesh points.

![Figure 10-4](images/Figure_10-4.png)

*Figure 10–4 2D Delaunay triangulation.*

```python
from vtkmodules.vtkCommonCore import vtkMath, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay2D, vtkExtractEdges, vtkGlyph3D, vtkTubeFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

# Generate some random points
math = vtkMath()
points = vtkPoints()
for i in range(50):
    points.InsertPoint(i, math.Random(0, 1), math.Random(0, 1), 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Perform a 2D Delaunay triangulation
delny = vtkDelaunay2D()
delny.SetInputData(profile)
delny.SetTolerance(0.001)

mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(delny.GetOutputPort())
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(0.1, 0.2, 0.4)

# Wrap edges in tubes
extract = vtkExtractEdges()
extract.SetInputConnection(delny.GetOutputPort())
tubes = vtkTubeFilter()
tubes.SetInputConnection(extract.GetOutputPort())
tubes.SetRadius(0.01)
tubes.SetNumberOfSides(6)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(0.2, 0.6, 0.6)

# Place spheres at the points
ball = vtkSphereSource()
ball.SetRadius(0.025)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)
balls = vtkGlyph3D()
balls.SetInputConnection(delny.GetOutputPort())
balls.SetSourceConnection(ball.GetOutputPort())

ball_mapper = vtkPolyDataMapper()
ball_mapper.SetInputConnection(balls.GetOutputPort())
ball_actor = vtkActor()
ball_actor.SetMapper(ball_mapper)
ball_actor.GetProperty().SetColor(1.0, 0.38, 0.68)
```

The Tolerance instance variable is used to determine whether points are coincident. Points located a distance Tolerance apart (or less) are considered coincident, and one of the points may be discarded. Tolerance is expressed as a fraction of the length of the diagonal of the bounding box of the input points.

Another useful feature of vtkDelaunay2D is the ability to define constraint edges and polygons. Normally, vtkDelaunay2D will generate a Delaunay triangulation of an input set of points satisfying the circumsphere criterion. However, in many cases additional information specifying edges in the triangulation (constraint edges) or "holes" in the data (constraint polygons) may be available. By specifying constraint edges and polygons, vtkDelaunay2D can be used to generate sophisticated triangulations of points. The following example demonstrates this.

```python
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D

# Define points and constraint polygons
points = vtkPoints()
points.InsertPoint(0, 1, 4, 0)
points.InsertPoint(1, 3, 4, 0)
points.InsertPoint(2, 7, 4, 0)
# ...(more points defined)...

polys = vtkCellArray()
polys.InsertNextCell(12)
polys.InsertCellPoint(0)
polys.InsertCellPoint(1)
polys.InsertCellPoint(2)
# ...(a total of two polygons defined)...

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(polys)

# Generate constrained triangulation
delny = vtkDelaunay2D()
delny.SetInputData(poly_data)
delny.SetSourceData(poly_data)
```

![Figure 10-5](images/Figure_10-5.png)

*Figure 10–5 Constrained Delaunay triangulation. On the left, a constraint polygon defines a hole in the triangulation. On the right, constraint edges define fault lines in a geological horizon.*

In this example, a second input to vtkDelaunay2D has been defined (with the `SetSourceData()` method). This input defines two polygons, one ordered counter-clockwise and defining the outer rectangular boundary, and the second clockwise-ordered polygon defining the "vtk" hole in the triangulation.

Using constraint edges is much simpler since the ordering of the edges is not important. Constraint edges (lines and polylines provided to the second input Source) are used to constrain the triangulation along a set of edges. (See the right side of Figure 10–5.)

**vtkDelaunay3D.** vtkDelaunay3D is similar to vtkDelaunay2D. The major difference is that the output of vtkDelaunay3D is an unstructured grid dataset (i.e., a tetrahedral mesh).

![Figure 10-6](images/Figure_10-6.png)

*Figure 10–6 3D Delaunay triangulation with non-zero alpha.*

```python
from vtkmodules.vtkCommonCore import vtkMath, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

# Generate random points in the unit cube
math = vtkMath()
points = vtkPoints()
for i in range(25):
    points.InsertPoint(i, math.Random(0, 1),
                       math.Random(0, 1), math.Random(0, 1))

profile = vtkPolyData()
profile.SetPoints(points)

# 3D Delaunay triangulation with alpha filtering
delny = vtkDelaunay3D()
delny.SetInputData(profile)
delny.SetTolerance(0.01)
delny.SetAlpha(0.2)
delny.BoundingTriangulationOff()

# Shrink the result to help see it better
shrink = vtkShrinkFilter()
shrink.SetInputConnection(delny.GetOutputPort())
shrink.SetShrinkFactor(0.9)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

triangulation = vtkActor()
triangulation.SetMapper(mapper)
triangulation.GetProperty().SetColor(1, 0, 0)
```

In this example we triangulate a random set of points in 3D space ranging between (0,1) along each of the coordinate axes. A non-zero Alpha is used, so the mesh consists of a collection of tetrahedra, triangles, lines, and points. The resulting tetrahedral mesh is shrunk with vtkShrinkFilter and mapped with vtkDataSetMapper.

### Gaussian Splatting

Many times data has no inherent structure, or the dimension of the data is high relative to what 2D, 3D, or 4D (3D with animation) visualization techniques can represent. An example of one such data set is scalar values (i.e., temperature) located at random points in space from a thermocouple measuring system. Multidimensional financial data (i.e., many records each record having several variables), is another example. One of the simplest and most robust procedures that can used to treat such data is to resample the data on a volume (i.e., vtkImageData dataset) and then visualize the resampled dataset. The following C++ example demonstrates this with multivariate financial data.

The data consists of an ASCII text file with 3188 financial records. Each record contains the following information: the time late in paying the loan (TIME_LATE); the monthly payment of the loan (MONTHLY_PAYMENT); the principal left on the loan (UNPAID_PRINCIPAL); the original amount of the loan (LOAN_AMOUNT); the interest rate on the loan (INTEREST_RATE); and the monthly income of the loanee (MONTHLY_INCOME).

The purpose of the visualization is to understand the relationship of these variables to the variable of major concern: TIME_LATE. Building a mathematical model or understanding of this data helps financial institutions make less risky loans. What we will do in the example is to show the late paying loans in context with the total loan population. We begin by choosing MONTHLY_PAYMENT as the x-axis, INTEREST_RATE as the y-axis, and LOAN_AMOUNT as the z-axis, and then choose TIME_LATE as the dependent variable (i.e., we reduce the dimensionality of the data by selecting three variables and ignoring the others). The class vtkGaussianSplatter is used to take the reduced financial data and "splat" them into a vtkImageData dataset using Gaussian ellipsoids. Then vtkContourFilter is used to generate an isosurface. Note that the first instance of vtkGaussianSplatter splats the entire dataset without scaling the splats, while the second instance of vtkGaussianSplatter scales the splats according to the scalar value (i.e., TIME_LATE). The late loans are rendered in red while the total population is rendered in a translucent white color. (See Figure 10–7.)

![Figure 10-7](images/Figure_10-7.png)

*Figure 10–7 Splatting data.*

Following is the C++ code demonstrating Gaussian splatting.

```cpp
#include <vtkContourFilter.h>
#include <vtkGaussianSplatter.h>
#include <vtkNew.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkAxesActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>

// ...read data into dataSet...

// Construct pipeline for original population
vtkNew<vtkGaussianSplatter> popSplatter;
popSplatter->SetInputData(dataSet);
popSplatter->SetSampleDimensions(50, 50, 50);
popSplatter->SetRadius(0.05);
popSplatter->ScalarWarpingOff();

vtkNew<vtkContourFilter> popSurface;
popSurface->SetInputConnection(popSplatter->GetOutputPort());
popSurface->SetValue(0, 0.01);

vtkNew<vtkPolyDataMapper> popMapper;
popMapper->SetInputConnection(popSurface->GetOutputPort());
popMapper->ScalarVisibilityOff();

vtkNew<vtkActor> popActor;
popActor->SetMapper(popMapper);
popActor->GetProperty()->SetOpacity(0.3);
popActor->GetProperty()->SetColor(0.9, 0.9, 0.9);

// Construct pipeline for delinquent population
vtkNew<vtkGaussianSplatter> lateSplatter;
lateSplatter->SetInputData(dataSet);
lateSplatter->SetSampleDimensions(50, 50, 50);
lateSplatter->SetRadius(0.05);
lateSplatter->SetScaleFactor(0.005);

vtkNew<vtkContourFilter> lateSurface;
lateSurface->SetInputConnection(lateSplatter->GetOutputPort());
lateSurface->SetValue(0, 0.01);

vtkNew<vtkPolyDataMapper> lateMapper;
lateMapper->SetInputConnection(lateSurface->GetOutputPort());
lateMapper->ScalarVisibilityOff();

vtkNew<vtkActor> lateActor;
lateActor->SetMapper(lateMapper);
lateActor->GetProperty()->SetColor(1.0, 0.0, 0.0);

// Create axes
vtkNew<vtkAxesActor> axes;

// Set up rendering
vtkNew<vtkRenderer> renderer;
vtkNew<vtkRenderWindow> renderWindow;
renderWindow->AddRenderer(renderer);
vtkNew<vtkRenderWindowInteractor> interactor;
interactor->SetRenderWindow(renderWindow);

renderer->AddActor(lateActor);
renderer->AddActor(axes);
renderer->AddActor(popActor);
renderer->SetBackground(1, 1, 1);
renderWindow->SetSize(800, 800);

interactor->Initialize();
interactor->Start();
```

What's interesting about this example is that the majority of late payments occur in a region of a high interest rate (expected) and lower monthly payment amount. Therefore, it's the smaller loans with higher interest rates which are the problem in this data.

Another filter for resampling data into a volume is vtkShepardMethod. You may wish to modify the previous C++ example to use this class.

### Surfaces from Unorganized Points

In computer graphics applications, surfaces are often represented as three-dimensional unorganized points. Laser and other digitizers are often the source of these point sets. Reconstructing surfaces from point clouds is both computationally and algorithmically challenging. While the methods described previously (Delaunay triangulation and Gaussian splatting) may be used with varying levels of success to reconstruct surfaces from point clouds, VTK has a class designed specifically for this purpose.

vtkSurfaceReconstructionFilter can be used to reconstruct surfaces from point clouds. This filter takes as input a vtkDataSet defining points assumed to lie on the surface of a 3D object. The following script shows how to use the filter. Figure 10–8 shows the results.

![Figure 10-8](images/Figure_10-8.png)

*Figure 10–8 Surface reconstruction.*

```python
import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkImagingHybrid import vtkSurfaceReconstructionFilter
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkReverseSense
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

# Read points from file
points = vtkPoints()
with open("cactus.3337.pts") as f:
    for line in f:
        tokens = line.split()
        if tokens and tokens[0] == "p":
            x, y, z = float(tokens[1]), float(tokens[2]), float(tokens[3])
            points.InsertNextPoint(x, y, z)

point_cloud = vtkPolyData()
point_cloud.SetPoints(points)

# Construct the surface and create isosurface
surf = vtkSurfaceReconstructionFilter()
surf.SetInputData(point_cloud)

cf = vtkContourFilter()
cf.SetInputConnection(surf.GetOutputPort())
cf.SetValue(0, 0.0)

# Reverse normals (they may point inward)
reverse = vtkReverseSense()
reverse.SetInputConnection(cf.GetOutputPort())
reverse.ReverseCellsOn()
reverse.ReverseNormalsOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reverse.GetOutputPort())
mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(mapper)
surface_actor.GetProperty().SetDiffuseColor(1.0, 0.39, 0.28)
surface_actor.GetProperty().SetSpecularColor(1, 1, 1)
surface_actor.GetProperty().SetSpecular(0.4)
surface_actor.GetProperty().SetSpecularPower(50)
```

The example begins by reading points from a file. vtkSurfaceReconstructionFilter takes the points and generates a volumetric representation (similar to what vtkGaussianSplatter did in the previous section). The volume is contoured (with an isosurface value=0.0) to generate a surface and vertex normals. Because of the nature of the data, the vertex normals point inward so vtkReverseSense is used to reverse the normals and polygon ordering. (On some systems inward pointing normals will result in black surfaces during rendering.)

The algorithm works reasonably well as long as the points are close enough together. The instance variable SampleSpacing can be set to control the dimensions of the output volume. If SampleSpacing is given a negative value, the algorithm makes a guess at the voxel size. The output volume bounds the input point cloud.
