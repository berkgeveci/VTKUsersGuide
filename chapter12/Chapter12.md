# Chapter 12: Reading and Writing Data

In this chapter we briefly describe various ways to read, write, import, and export data. Readers ingest a single dataset, while importers create an entire scene, which may include one or more datasets, actors, lights, cameras, and so on. Writers output a single dataset to disk (or stream), and exporters output an entire scene. In some cases, you may want to interface to data that is not in standard VTK format, or in any other common format that VTK supports. In such circumstances, you may wish to treat data as field data, and convert it in the visualization pipeline into datasets that the standard visualization techniques can properly handle.

## 12.1 Readers

We saw in “Reader Source Object” on page44 how to use a reader to bring data into the visualization pipeline. Using a similar approach, we can read many other types of data. Using a reader involves instantiating the reader, supplying a filename, and calling Update() somewhere down the pipeline.

There are many different readers in the VTK library, all of which exist to read files and produce data structures that can be processed and visualized by the rest of the visualization pipeline. A reader then, is any vtkAlgorithm, which does not require input connections and which knows how to read files to produce vtkDataObjects.

There are many different readers in VTK because there are many important file formats for scientific data. The different file formats exist to make permanent different varieties of data such as structured, unstructured, polygonal, tabular, or graph. As a user of VTK, an important task is to determine what VTK data structure corresponds to the data of interest to you and then to find a reader that reads in the files you work with to produce that structure. This section introduces some of the available readers.

There are some points to make note of before diving into the list of readers. For all VTK data structure types there exists one or two VTK native reader classes. These classes were written in concert with developing or extending the corresponding data type. The older native reader class reads files with the ".vtk" extension, and the newer reads XML based files with the ".vt?" extension (where ? describes the type). Both old and new formats support writing data in text or binary formats. The newer format is more involved, but it fully supports the most recent vtk features including named arrays, 32 bit / 64 bit encoding, streamed processing and the all of the latest data structures. Both formats have parallel processing extensions, which are implemented with meta files which refer to external serial files that are meant to be read independently. See “VTK File Formats” on page469., for details of the native file formats.

This chapter lists the VTK native readers for each data type as well as a selection of the readers that interface with the more well known third party file formats and produce that type.

Finally note that, if a suitable reader does not exist one can write one in C++, or use the techniques described in“Working With Field Data” on page249 to coerce the output of the most generic reader, vtkProgrammableDataObjectSource, into the proper data type.

### Data Object Readers

- vtkProgrammableDataObjectSource - an algorithm that executes a user specified function to produce a vtkDataObject.. The user specified function can be written to read in any particular file format, or procedurally generate data without reading any file. 
- vtkGenericDataObjectReader - read a ".vtk" file, the legacy file format for all of VTK's data structures and populate a vtkDataObject or the most specific subclass thereof with the structure defined in the file. This reader will produce vtkTable for example, if the .vtk file contains Tabular Data, and vtkUnstructuredGrid if the chosen .vtk file contains an Unstructured Grid. This class reads the header information to find out what type of data is in the file and then delegates the rest of the processing to one of the more specific classes described below. 
- vtkDataObjectReader - read a ".vtk" file and populate a DataObject with Field associated arrays. This differs from vtkGenericDataObjectReader in that it will not produce the specific data structure best suited to the contents of the file and instead always produces the most general one, vtkDataObject.

### Dataset Readers

These readers produce generic vtkDataSet as output. Typically, the reader requires an Update() invocation to determine what kind of concrete vtkDataSet subclass is created. 
- vtkDataSetReader - like vtkDataObjectReader, but this class is limited to the more common vtkDataSet subclasses. 
- vtkPDataSetReader - like vtkDataSetReader, but reads parallel vtk (.pvtk) format files, which are meta files that references several legacy .vtk files which are meant to be processed by different processors simultaneously 
- vtkGenericEnSightReader (and subclasses) - read EnSight files

### Image and Volume Readers 

- vtkStructuredPointsReader - reads ".vtk" legacy format files containing image data 
- vtkXMLImageDataReader - reads ".vti" files, one of the newer XML based VTK file formats

- vtkXMLPImageDataReader - reads ".pvti" XML based parallel partitioned files that reference individual ".vti" files 
- vtkImageReader - reads raw image data. Since the file format is a raw dump, you must specify the image extent, byte ordering, scalar type etc in order to get the correct result from the file. 
- vtkDICOMImageReader - reads DICOM (Digital Imaging and Communications in Medicine) images 
- vtkGESignaReader - reads GE Signa Imaging files 
- vtkMINCImageReader - a netCDF based reader for MINC (Montreal Neurological Institute Center) files 
- vtkJPEGReader - reads JPEG files 
- vtkPNMReader - reads PNM files 
- vtkTIFFReader - reads TIFF files

### Rectilinear Grid Readers

- vtkRectilinearGridReader - reads ".vtk" legacy format files containing rectilinear grid data 
- vtkXMLRectilinearGridReader - reads ".vtr" XML based VTK files 
- vtkXMLPRectilinearGridDataReader - reads ".pvtr" XML based parallel partitioned files that reference individual ".vtr" files 
- vtkSESAMEReader - reads Los Alamos National Lab Equation of state data base files (http:// t1web.lanl.gov/doc/SESAME_3Ddatabase_1992.html) 

### Structured Grid Readers 
- vtkStructuredGridReader - reads ".vtk" legacy format files containing structured grid data 
- vtkXMLStructuredGridReader - reads ".vts" XML based VTK files 
- vtkXMLPStructuredGridReader - reads ".pvts" XML based parallel partitioned files that reference individual ".vts" files 
- vtkPLOT3DReader - reads NASA PLOT3D structured CFD computation datasets (http://people.nas.nasa.gov/~rogers/plot3d/intro.html)

### Polygonal Data Readers 
- vtkPolyDataReader - reads ".vtk" legacy format files containing polygonal data 
- vtkXMLPolyDataReader - reads ".vtp" XML based VTK files 
- vtkXMLPPolyDataReader - reads ".pvtp" XML based parallel partitioned files that reference individual ".vtp" files 
- vtkOBJReader - reads Wavefront .obj files 
- vtkPLYReader - reads Stanford University .ply files 
- vtkParticleReader - reads particle with scalar data x,y,z,value in ascii or binary format
- vtkSTLReader - read stereo-lithography files 
- vtkSimplePointsReader - example reader, reads points written as X Y Z floating point form and produce edges and vtk_vertex cells in vtkPolyData (PD) 
- vtkSLACParticleReader - reads netCDF files written with conventions for Stanford Linear Accelerator Center processing tools. Output corresponds to particles in space. This differs from vtkNetCDFReader in that although both understand the NetCDF format, this reader adds conventions suited to a particular area of scientific research.

### Unstructured Grid Readers 
- vtkUnstructuredGridReader - reads ".vtk" legacy format files containing unstructured grid data 
- vtkXMLUnstructuredGridReader - reads ".vtu" XML based VTK files 
- vtkXMLPUnstructuredGridReader - reads ".pvtu" XML based parallel partitioned files that reference individual ".vtu" files 
- vtkCosmoReader - read Los Alamos National Lab cosmology binary data format files 
- vtkExodusReader - read Sandia National Lab Exodus format files 
- vtkPExodusReader - parallel processing specialization of vtkExodusReader in which each processor reads its own portion of the blocks from the file simultaneously 
- vtkChacoReader - reads Sandia Chaco graph package format files and produces UnstructuredGrid data 
- vtkPChacoReader - reads Sandia Chaco graph format packages on one processor and internally distributes portions of the data to other parallel processors

### Graph Readers 

- vtkGraphReader - read ".vtk" legacy format files containing general Graph data 
- vtkTreeReader - read ".vtk" legacy format files to produce more specialized Trees 
- vtkXMLTreeReader - reads XML based VTK files 
- vtkChacoGraphReader - reads a file written in the Sandia Chaco graph package format. This differs from vtkChacoReader in that it produces a vtkUndirectedGraph instead of the more spatially oriented vtkUnstructuredGrid. 
- vtkPBGLGraphSQLReader - read vertex and edge tables from an Parallel Boost Graph Library SQL database 
- vtkSQLGraphReader - read vertex and edge tables from an SQL database 
- vtkRISReader - read a RIS format bibliographic citation file and produce a vtkTable (TA)

### Table Readers 
- vtkTableReader - - read ".vtk" legacy format files containing general tabular data 
- vtkDelimitedTextReader - read text files in which newlines separate each row and a single user specified delimiter character, for example, comma, tab or space, separates columns 
- vtkFixedWidthTextReader - read text files in which newlines separate each row and where each column has a fixed width
- vtkISIReader - read bibliographic citation records in ISI format 

### Composite Data Readers

vtkCompositeDataSet’s concrete subclasses vtkMultiPieceDataSet, vtkHierarchicalBoxDataSet, and vtkMultiBlockDataSet are VTK's way of representing compound data objects, or data objects which contain other data objects. These structures are useful in parallel processing, for adaptively refined simulations and to represent hierarchical relationships between related parts. Several readers import complex data and produce composite data outputs. The contents of the composite data may be any or all of the above atomic types, and/or additional composite data objects. 
- vtkXMLCompositeDataReader - and its subclasses read XML based VTK files. The standard extensions for these files include ".vtm", ".vth" and ".vtb". 
- vtkExodusIIReader - read Sandia Exodus2 format files and directly produce MultiBlock datasets. This differs from vtkExodusReader in that the output is not converted to a single vtkUnstructuredGrid, which can potentially conserve memory when the data is regular. 
- vtkPExodusIIReaderparallel processing specialization of the preceding each processor independently and simultaneously reads its own subset of the blocks 
- vtkOpenFOAMReader - read file written in OpenFOAM (computational fluid dynamics) format

## 12.2 Writers

Writers output vtkDataObjects to the file system. A writer is any vtkAlgorithm which takes in a vtkDataObject, usually one produced by the vtkAlgorithm connected to the writer's input, and writes it to the file system in some standard format. There are many different writers in VTK because there are many important file formats.

Typically, using a writer involves setting an input and specifying and output file name (or sometimes names) as shown in the following.

```tcl
vtkPolyDataWriter writer
writer SetInput [aFilter GetOutput]
writer SetFileName “outFile.vtk”
writer SetFileTypeToBinary
writer Write
```

The legacy VTK writers offer you the option of writing binary (SetFileTypeToBinary()) or ASCII (SetFileTypeToASCII()) files. (Note: binary files may not be transportable across computers. VTK takes care of swapping bytes, but does not handle transport between 64-bit and 32-bit computers.)

The VTK XML writers also allow you to write in binary (SetDataModeToBinary()) or ASCII (SetDataModeToAscii()); and appended binary mode is also available (SetDataModeToAppended()). The VTK XML readers and writers do handle transporting data between 32-bit and 64-bit computers in addition to taking care of byte swapping.

The following is a list of available writers.

### Data Object Writers

- vtkGenericDataObjectWriter - Writes any type of vtkDataObject to file in the legacy ".vtk" file format. 
- vtkDataObjectWriter -- Write only the vtkDataObject's field data in legacy ".vtk" file format.

### Data Set Writers 
- vtkDataSetWriter - Writes any type of vtkDataSet to file in legacy ".vtk" file format 
- vtkPDataSetWriter - Writes any type of vtkDataSet to file in legacy ".pvtk" parallel partitioned file format 
- vtkXMLDataSetWriters - Writes any type of vtkDataSet to file in the newer XML based ".vt?" format.

### Image and Volume Writers 
- vtkStructuredPointsWriter - Write image data in legacy ".vtk" format 
- vtkPImageWriter - A parallel processing specialization of the preceding 
- vtkXMLImageDataWriter - Write image data in XML based ".vti" format 
- vtkMINCImageWriter - A netCDF based writer for MINC (Montreal Neurological Institute Center) files 
- vtkPostScriptWriter - write image into post script format 
- vtkJPEGWriter - write into JPEG format 
- vtkPNMWriter - write into PNM format 
- vtkTIFFWriter - write into TIFF format

### Rectilinear Grid Writers 
- vtkRectilinearGridWriter - Write rectilinear grid in legacy ".vtk" format 
- vtkXMLRectilinearGridWriter - Write rectilinear grid in XML based ".vtr" format 
- vtkXMLPRectilinearGridWriter - A parallel processing specialization of the preceding

### Structured Grid Writers 
- vtkStructuredGridWriter - Write structured grid in legacy ".vtk" format 
- vtkXMLStructuredGridWriter - Write structured grid in XML based ".vts" format 
- vtkXMLPStructuredGridWriter - A parallel processing specialization of the preceding

### Polygonal Data Writers 
- vtkPolyDataWriter - Write polygonal data in legacy ".vtk" format 
- vtkXMLPolyDataWriter - Write polygonal data in XML based ".vtp" format
- vtkXMLPPolyDataWriter - A parallel processing specialization of the preceding 
- vtkSTLWriter - Write stereo-lithography files 
- vtkIVWriter - Write into OpenInventor 2.0 format 
- vtkPLYWriter - Writer Stanford University ".ply" files

### Unstructured Grid Writers 
- vtkUnstructuredGridWriter - Write unstructured data in legacy ".vtk" format 
- vtkXMLUnstructuredGridWriter - Write unstructured data in XML based ".vtu" format 
- vtkXMLPUnstructuredGridWriter - A parallel processing specialization of the preceding 
- vtkEnSightWriter - Write vtk unstructured grid data as an EnSight file 

### Graph Writers 
- vtkGraphWriter - write vtkGraph data to a file in legacy ".vtk" format 
- vtkTreeWriter - write vtkTree data to a file in legacy ".vtk" format 

### Table Writers 
- vtkTableWriter - write vtkTable data to file in legacy ".vtk" format 

### Composite Data Writers 
- vtkXMLCompositeDataWriter (and its subclasses) - writers for composite data structures including hierarchical box (multires image data) and multi-block (related datasets) data types 
- vtkExodusIIWriter - Write composite data in Exodus II format

## 12.3 Importers

Importers accept data files that contain multiple datasets and/or the objects that compose a scene (i.e., lights, cameras, actors, properties, transformation matrices, etc.). Importers will either generate an instance of vtkRenderWindow and/or vtkRenderer, or you can specify them. If specified, the importer will create lights, cameras, actors, and so on, and place them into the specified instance(s). Otherwise, it will create instances of vtkRenderer and vtkRenderWindow, as necessary. The following example shows how to use an instance of vtkImporter (in this case a vtk3DSImporter—imports 3D Studio files). This Tcl script was taken from VTK/Examples/IO/Tcl/flamingo.tcl (see Figure 12–1).

![Figure 12-1](images/Figure_12-1.png)

*Figure 12–1 Importing a file.*

```tcl
vtk3DSImporter importer
importer ComputeNormalsOn
importer SetFileName \
"$VTK_DATA_ROOT/Data/iflamigm.3ds"
importer Read

set renWin [importer GetRenderWindow]
vtkRenderWindowInteractor iren
iren SetRenderWindow $renWin
```

The Visualization Toolkit supports the following importers. (Note that the superclass vtkImporter is available for developing new subclasses.) 
- vtk3DSImporter — import 3D Studio files 
- vtkVRMLImporter — import VRML version 2.0 files

## 12.4 Exporters

Exporters output scenes in various formats. Instances of vtkExporter accept an instance of vtkRenderWindow, and write out the graphics objects supported by the exported format.

```tcl
vtkRIBExporter exporter
exporter SetRenderWindow renWin
exporter SetFilePrefix “anExportedFile”
exporter Write
```

The vtkRIBExporter shown above writes out multiple files in RenderMan format. The FilePrefix instance variable is used to write one or more files (geometry and texture map(s), if any). The Visualization Toolkit supports the following exporters. 
- vtkGL2PSExporter — export a scene as a PostScript file using GL2PS 
- vtkIVExporter — export an Inventor scene graph 
- vtkOBJExporter — export a Wavefront .obj files 
- vtkOOGLExporter — export a scene into GeomView OOGL format 
- vtkRIBExporter — export RenderMan files 
- vtkVRMLExporter — export VRML version 2.0 files 
- vtkPOVExporter - export into file format for the Persistence of Vision Raytracer (www.povray.org) 
- vtkX3DExporter - export into X3D format (an XML based 3d scene format similar to VRML)

## 12.5 Creating Hardcopy

Creating informative images is a primary objective of VTK, and to document what you’ve done, saving images and series of images (i.e., animations) is important. This section describes various ways to create graphical output.

### Saving Images

The simplest way to save images is to use the vtkWindowToImageFilter which grabs the output buffer of the render window and converts it into vtkImageData. This image can then be saved using one of the image writers (see “Writers” on page164 for more information). Here is an example

```tcl
vtkWindowToImageFilter w2i
w2i SetInput renWin
vtkJPEGWriter writer
writer SetInput [w2i GetOutput]
writer SetFileName "DelMesh.jpg"
writer Write
```

Note that it is possible to use the off-screen mode of the render window when saving an image. The off-screen mode can be turned on by setting OffScreenRenderingOn() for the render window.

### Saving Large (High-Resolution)

Images The images saved via screen capture or by saving the render window vary greatly in quality depending on the graphics hardware and screen resolution supported on your computer. To improve the quality of your images, there are two approaches that you can try. The first approach allows you to use the imaging pipeline to render pieces of your image and then combine them into a very high-resolution final image. We’ll refer to this as tiled imaging. The second approach requires external software to perform high resolution rendering. We’ll refer to this as the RenderMan solution.

**Tiled Rendering.** Often we want to save an image of resolution greater than the resolution of the computer hardware. For example, generating an image of 4000 x 4000 pixels is not easy on a 1280x1024 computer display. The Visualization Toolkit makes this trivial with the class vtkRenderLargeImage. This class breaks up the rendering process into separate pieces, each piece containing just a portion of the final image. The pieces are assembled into a final image, which can be saved to file using one of the VTK image writers. Here’s how it works (Tcl script taken from VTK/ Examples/Rendering/Tcl/RenderLargeImage.tcl).

```tcl
vtkRenderLargeImage renderLarge
renderLarge SetInput ren
renderLarge SetMagnification 4
vtkTIFFWriter writer
writer SetInputConnection [renderLarge GetOutputPort]
writer SetFileName largeImage.tif
writer Write
```

The Magnification instance variable (an integer value) controls how much to magnify the input renderer’s current image. If the renderer’s image size is (400,400) and the magnification factor is 5, the final image will be of resolution (2000,2000). In this example, the resulting image is written to a file with an instance of vtkTIFFWriter. Of course, other writer types could be used.

**RenderMan.** RenderMan is a high-quality software rendering system currently sold by Pixar, the graphics animation house that created the famous Toy Story movie. RenderMan is a commercial package. A license for a single computer RenderMan rendering plugin for Maya costs $995 at the time of this writing.. Fortunately, there is at least one modestly priced (or free system if you’re non-commercial) RenderMan compatible system that you can download and use: Pixie (Blue Moon Ray Tracer). Pixie is slower than RenderMan, but it also offers several features that RenderMan does not.

In an earlier section (“Exporters” on page166) we saw how to export a RenderMan .rib file (and associated textures). You can adjust the size of the image RenderMan produces using the SetSize() method in the vtkRIBExporter. This method adds a line to the rib file that causes RenderMan (or RenderMan compatible system such as Pixie) to create an output TIFF image of size (xres, yres) pixels.

## 12.6 Creating Movie Files

In addition to writing a series of images, VTK also has three classes that allow you to write movie files directly: vtkAVIWriter, vtkFFMPEGWriter and vtkMPEG2Writer. Both are subclasses of vtkGenericMovieWriter. vtkAVIWriter uses Microsoft's multimedia API to create movie files, and is thus only available on Windows machines. The FFMPEG and MPEG2 media formats are available on all platforms, but because of license incompatibilities are provided only in source code format, and not within the VTK library itself. To use either of these interface classes you must manually download and compile the library on your machine and then configure and build VTK to link to them. Instructions for doing so and the library source code are available at http://www.vtk.org/VTK/resources/software.html#addons. Both of these classes take a 2D vtkImageData as input – often the output of the vtkWindowToImageFilter. The important methods in these classes are as follows. 
- Start — Call this method once to start writing a movie file. 
- Write— Call this method once per frame added to the movie file. 
- End — Call this method once to end the writing process.

Similar to the other writers, the movie writers also have SetInput and SetFileName methods. Example Tcl code for writing a movie file with 100 frames follows.

```tcl
vtkMPEG2Writer writer
writer SetInput [aFilter GetOutput]
writer SetFileName "movie.mpg"
writer Start

for {set i 0} {$i < 100} {incr i} {
writer Write
# modify input to create next frame of movie …
}
writer End
```

![Figure 12-2](images/Figure_12-2.png)

*Figure 12–2 Structure of field data—an array of arrays. Each array may be of a different native data type and may have one or more components.*

## 12.7 Working With Field Data

Many times data is organized in a form different from that found in VTK. For example, your data may be tabular, or possibly even higher-dimensional. And sometimes you’d like to be able to rearrange your data, assigning some data as scalars, some as point coordinates, and some as other attribute data. In such situations VTK’s field data, and the filters that allow you to manipulate field data, are essential.

To introduce this topic a concrete example is useful. In the previous chapter (“Gaussian Splatting” on page156) we saw an example that required writing custom code to read a tabular data file, then extracting specified data to form points and scalars (look at the function ReadFinancialData() found in VTK/Examples/Modelling/Cxx/finance.cxx). While this works fine for this example, it does require a lot of work and is not very flexible. In the following example we’ll do the same thing using field data.

The data is in the following tabular format.
```
NUMBER_POINTS 3188
TIME_LATE
29.14 0.00 0.00 11.71 0.00 0.00 0.00 0.00
0.00 29.14 0.00 0.00 0.00 0.00 0.00 0.00
....
MONTHLY_PAYMENT
7.26 5.27 8.01 16.84 8.21 15.75 10.62 15.47
5.63 9.50 15.29 15.65 11.51 11.21 10.33 10.78
....
```

This format repeats for each of the following fields: time late in paying the loan (TIME_LATE); the monthly payment of the loan (MONTHLY_PAYMENT); the principal left on the loan (UNPAID_PRINCIPAL); the original amount of the loan (LOAN_AMOUNT); the interest rate on the loan (INTEREST_RATE); and the monthly income of the borrower (MONTHLY_INCOME). These six fields form a matrix of 3188 rows and 6 columns.

We start by parsing the data file. The class vtkProgrammableDataObjectSource is useful for defining special input methods without having to modify VTK. All we need to do is to define a function that parses the file and puts the results into a VTK data object. (Recall that vtkDataObject is the most general form of data representation.) Reading the data is the most challenging part of this example, found in VTK/Examples/DataManipulation/Tcl/FinancialField.tcl.

```tcl
set xAxis INTEREST_RATE
set yAxis MONTHLY_PAYMENT
set zAxis MONTHLY_INCOME
set scalar TIME_LATE

# Parse an ascii file and manually create a field. Then construct a # dataset from the field.

vtkProgrammableDataObjectSource dos
dos SetExecuteMethod parseFile
proc parseFile {} {
global VTK_DATA_ROOT # Use Tcl to read an ascii file
set file [open "$VTK_DATA_ROOT/Data/financial.txt" r]
set line [gets $file]
scan $line "%*s %d" numPts
set numLines [expr (($numPts - 1) / 8) + 1 ]

# Get the data object's field data and allocate # room for 4 fields
set fieldData [[dos GetOutput] GetFieldData]
$fieldData AllocateArrays 4

# read TIME_LATE - dependent variable
# search the file until an array called TIME_LATE is found
while { [gets $file arrayName] == 0 } {}
# Create the corresponding float array
vtkFloatArray timeLate
timeLate SetName TIME_LATE

# Read the values
for {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
set m [scan $line "%f %f %f %f %f %f %f %f" \
v(0) v(1) v(2) v(3) v(4) v(5) v(6) v(7)]

for {set j 0} {$j < $m} {incr j} {timeLate InsertNextValue $v($j)}
}

# Add the array
$fieldData AddArray timeLate

# MONTHLY_PAYMENT - independent variable
while { [gets $file arrayName] == 0 } {}

vtkFloatArray monthlyPayment
monthlyPayment SetName MONTHLY_PAYMENT
for {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
set m [scan $line "%f %f %f %f %f %f %f %f" \
v(0) v(1) v(2) v(3) v(4) v(5) v(6) v(7)]

for {set j 0} {$j < $m} {incr j} {monthlyPayment InsertNextValue
$v($j)}
}
$fieldData AddArray monthlyPayment

# UNPAID_PRINCIPLE - skip
while { [gets $file arrayName] == 0 } {}
or {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
}

# LOAN_AMOUNT - skip
while { [gets $file arrayName] == 0 } {}
for {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
}

# INTEREST_RATE - independent variable
while { [gets $file arrayName] == 0 } {}

vtkFloatArray interestRate
interestRate SetName INTEREST_RATE
for {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
set m [scan $line "%f %f %f %f %f %f %f %f" \
v(0) v(1) v(2) v(3) v(4) v(5) v(6) v(7)]
for {set j 0} {$j < $m} {incr j} {interestRate InsertNextValue $v($j)}
}
$fieldData AddArray interestRate

# MONTHLY_INCOME - independent variable
while { [gets $file arrayName] == 0 } {}

vtkIntArray monthlyIncome
monthlyIncome SetName MONTHLY_INCOME
for {set i 0} {$i < $numLines} {incr i} {
set line [gets $file]
set m [scan $line "%d %d %d %d %d %d %d %d" \
v(0) v(1) v(2) v(3) v(4) v(5) v(6) v(7)]

for {set j 0} {$j < $m} {incr j} {monthlyIncome InsertNextValue $v($j)}
}
$fieldData AddArray monthlyIncome
}
```

Now that we've read the data, we have to rearrange the field data contained by the output vtkDataObject into a form suitable for processing by the visualization pipeline (i.e., the vtkGaussianSplatter). This means creating a subclass of vtkDataSet, since vtkGaussianSplatter takes an instance of vtkDataSet as input. There are two steps required. First, the filter vtkDataObjectToDataSetFilter is used to convert the vtkDataObject to type vtkDataSet. Then, vtkRearrangeFields and vtkAssignAttribute are used to move a field from the vtkDataObject to the vtkPointData of the newly created vtkDataSet and label it as the active scalar field.

```tcl
vtkDataObjectToDataSetFilter do2ds
do2ds SetInputConnection [dos GetOutputPort]
do2ds SetDataSetTypeToPolyData
do2ds DefaultNormalizeOn
do2ds SetPointComponent 0 $xAxis 0
do2ds SetPointComponent 1 $yAxis 0
do2ds SetPointComponent 2 $zAxis 0

vtkRearrangeFields rf
rf SetInputConnection [do2ds GetOutputPort]
rf AddOperation MOVE $scalar DATA_OBJECT POINT_DATA

vtkAssignAttribute aa
aa SetInputConnection [rf GetOutputPort]
aa Assign $scalar SCALARS POINT_DATA
aa Update
```

There are several import techniques in use here.

1. All filters pass their input vtkDataObject through to their output unless instructed otherwise (or unless they modify vtkDataObject). We will take advantage of this in the downstream filters.
2. We set up vtkDataObjectToDataSetFilter tocreate an instance of vtkPolyData as its output, with the three named arrays of the field data serving as x, y, and z coordinates. In this case we use vtkPolyData because the data is unstructured and consists only of points.
3. We normalize the field values to range between (0,1) because the axes' ranges are different enough that we create a better visualization by filling the entire space with data.
4. The filter vtkRearrangeFields copies/moves fields between vtkDataObject, vtkPointData and vtkCellData. In this example, an operation to move the field called $scalar from the data object of the input to the point data of the output is added.
5. The filter vtkAssignAttribute labels fields as attributes. In this example, the field called $scalar (in the point data) is labeled as the active scalar field.

The Set___Component() methods are the key methods of vtkDataObjectToDataSetFilter. These methods refer to the data arrays in the field data by name and by component number. (Recall that a data array may have more than one component.) It is also possible to indicate a (min,max) tuple range from the data array, and to perform normalization. However, make sure that the number of tuples extracted matches the number of items in the dataset structure (e.g., the number of points or cells). 

There are several related classes that do similar operations. These classes can be used to rearrange data arbitrarily to and from field data, into datasets, and into attribute data. These filters include: 
- vtkDataObjectToDataSetFilter — Create a vtkDataSet, building the dataset’s geometry, topology and attribute data from the chosen arrays within the vtkDataObject’s field data. 
- vtkDataSetToDataObjectFilter — Transform vtkDataSet into vtkFieldData contained in a vtkDataObject. 
- vtkRearrangeFields — Move/copy fields between field data, point data, and cell data. 
- vtkAssignAttribute — Label a field as an attribute.
- vtkMergeFields — Merge multiple fields into one. 
- vtkSplitField — Split a field into multiple single component fields. 
- vtkDataObjectReader — Read a VTK formatted field data file. 
- vtkDataObjectWriter — Write a VTK formatted field data file. 
- vtkProgrammableDataObjectSource — Define a method to read data of arbitrary form and represent it as field data (i.e., place it in a vtkDataObject).
