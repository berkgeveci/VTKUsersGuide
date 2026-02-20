# Chapter 11: Time Varying Data

## 11.1 Introduction to temporal support

The visualization toolkit was created for the purpose of allowing people to visualize and thus explore features in data with spatial extent. It allows people to answer questions, such as "Where are the regions of maximum value located within this data?? "What shape and value do they have?" and "How are those shapes distributed throughout?" VTK provides a plethora of techniques for displaying and analyzing data, as it exists at a single moment in time. Exploration of data that has temporal extent is also important. One would also like to answer questions such as. "How do those shapes grow, move and shrink over time?”

That goal is complicated by the fact that VTK represents a point with only X, Y and Z coordinate values. Adding T is impractical because of backward compatibility requirements and the need to conserve RAM in the most common case in which T unimportant. With previous versions of the visualization toolkit, people implemented a variety of workarounds to overcome the basic lack of support for time. For instance, multiple attribute array sets (one set for each time step) were sometimes loaded and filters were told to iterate through the sets.

Creating such workarounds was difficult not only because of the lack of support in VTK but also because of the variety of formats in which time varying data is stored. Some practitioners store an entire dataset in a sequentially named file for each (regularly or irregularly sampled) point in time. Others store just the time varying portions of the data in one or many separate files. Some store the T coordinates alongside the X, Y, and Z coordinates as suggested above, and some store the data in highly compressed encoded formats.

As compute power has grown and become widespread, exploration and analysis of time varying scientific data has become commonplace. Since release 5.2, VTK has included a general-purpose infrastructure for time varying visualization. The infrastructure is not wasteful of memory and is backward compatible. In the common case when time is immaterial, no additional RAM or disk space is consumed, and the majority of filters that are time insensitive did not need any modification. The infrastructure is also opening ended and extensible. In addition to supporting flipbook style animations, which would allow one to answer the temporal question posed above, it also allows one to programmatically answer quantitative questions such as: 
- “At what time do the shapes take on a maximum volume?” 
- “At what point do they move most quickly?” 
- “What are the average attribute values over a particular region of time?” 
- “What does a 2D plot of values for particular elements or locations look like?”

To do so, one finds, or creates a vtkAlgorithm that takes into account the temporal dimension to answer the question, and then builds a pipeline that exercises it. A time-aware filter is one that is capable of: requesting one or more specific time steps from the pipeline behind it, doing some processing once supplied with the requested data objects, and producing an answer (in the form of another data object) for the downstream filters.

The many varieties of temporal representations are facilitated because of the reader abstraction. A reader, as described in Chapter 12, is responsible for reading a file or set of files on the file system, interpreting a specific file format, and producing one or more data objects. A time aware reader is one that additionally tells the pipeline what the available temporal domain is, and is capable of producing an answer (again in the form of a data object) for the specific time (or times) that the downstream pipeline has requested of it.

## 11.2 VTK's implementation of time support

VTK supports time varying data at the pipeline level. vtkExecutives are the glue that hold neighboring vtkAlgorithms together and thus make up the pipeline. Besides linking Algorithms together, Executives are also responsible for telling each Algorithm exactly what to do. The Executives do so by communicating meta-information, small pieces of data (stored in vtkInformation containers), up and down the pipeline before causing their attached Algorithms to execute. For example, each Algorithm is given a vtkInformation object that specifies where, or what spatial sub domain it is to fill. When doing temporal visualization, Executives also tell each Algorithm when, or at what point in time they are to do so. This each Algorithm can now be given a vtkInformation object that specifies what temporal sub domain that processing is supposed to take place in.

To be exact, the pipeline now supports temporal visualization because it recognizes the following meta-information keys, and understands how and when to transport them and react to their presence in order to drive filter execution.

### TIME_RANGE

This key is injected into the pipeline by a reader of time varying data, at the source or beginning of the pipeline. It contains two floating-point numbers, which are the minimum and maximum times that the reader can produce data within, or in other words, the extent of the temporal domain.

### TIME_STEPS

When the data produced by the reader is exact at discrete points in time, this key is also injected into the pipeline by a reader of time varying data. It contains any number of floating point numbers which may be regularly or irregularly placed within the temporal domain.

### UPDATE_TIME_STEPS

This key is injected into the pipeline at downstream end of the pipeline. It contains one or more floating point numbers that correspond to the set of times that are to be processed by the pipeline update. 

### DATA_TIME_STEPS

When the update request reaches the reader, it may or may not be able to provide results for exactly that time. For example the renderer may ask for a time that lies between two points in the TIME_STEPS. The reader injects this key into the pipeline to indicate the exact data time that corresponds to the data it produces in response to the request. 

### CONTINUE_EXECUTING

This flag is injected into the pipeline to cause the pipeline to keep iterating in order to fulfill a set of time requests.

Because time support was added at the pipeline level, one must know something about how the visualization pipeline executes in order to understand the actions that the above meta information cause, and thus understand what VTK's time support can be used for. VTK's standard streaming demand driven pipeline operates in four stages. The same four passes are used for time varying visualization, but they are often (either for a subset of or for the full pipeline) iterated in a loop. 

During the first pass, called REQUEST_DATA_OBJECT , each Executive creates an empty DataObject of whatever type is needed for the Algorithm. A vtkJPEGReader for example, produces an empty vtkImageData. When a time aware filter requests multiple time steps from a non-time aware filter upstream, the Executive will change the filter's output type to be a vtkTemporalDataSet. That output acts as a cache for the actual datasets produces for each requested time.

During the second pass, called REQUEST_INFORMATION, filters produce whatever lightweight meta-information they can about the data they are about to create. A vtkJPEGReader would provide an image extent for example. This pass starts at the upstream end and works forward toward the display. It is during this pass when time aware readers are required to inject their TIME_RANGE and TIME_STEPS keys, which downstream filters and the application can use to guide their actions.

During the third pass, called REQUEST_UPDATE_EXTENT, the filters agree, starting at the downstream end and working back toward the reader, what portion of their input will be required to produce the output they are themselves being asked for. It is at this pass that the UPDATE_TIME_STEPS request moves backwards.

During the last pass, called REQUEST_DATA, Algorithms actually do the work requested of them, which means for time varying data, producing data at the time requested and filling in the DATA_TIME_STEPS parameter. 

At first this appears to still be a brute force approach. One still makes a flipbook animation by stepping through time, updating the pipeline to draw an image at each time. In older versions of VTK iterating over a loop in which a time parameter was set on the reader and then the display was rendered often did this. In modern VTK this is done similarly. The only difference from the user's standpoint is that the requested time is set on the renderer instead of the reader. However, several details in the implementation make VTK's new time support more efficient, easier to use and more flexible than it was previously.

First, Algorithms are free to request and provide multiple times. This makes it possible for any filter to consider more that one time step together, in effect merging a temporal pipeline. This enables more advanced time varying visualizations than flip books, such as interpolation between time steps and advanced motion blur like effects (time trails).

Second, the Executive has the ability to automatically iterate portions of the pipeline that are not time aware. This makes it unnecessary for the programmer to explicitly control individual Algorithms in the pipeline. To compute a running average, one would simply set the width or support as a parameter on an averaging filter and then tell the pipeline to execute once. Before this would have been done by explicitly updating the pipeline over multiple passes and at each pass telling the reader exactly what time is required for the active portion of the running average.

Third, the Executive, and even Algorithms themselves, are able to manipulate the meta-information keys, which enable techniques such as temporal shifting, scaling and reversion. These are useful in cases such as normalize data sources to a common frame of reference.

Finally, the pipeline will, and it is possible to manually cause, caching of temporal results, and to do so without keeping all results from the reader in memory simultaneously. Caching can give substantial speedups and makes techniques like comparative visualization of the same pipeline at different points in time effective.

### Using time support

The default pipeline created by VTK programs consists of Algorithms connected by vtkStreamingDemandDrivenPipeline Executives. This Executive does not do automatic iteration or temporal caching. Thus the first step in doing temporal analysis with VTK is to replace the default pipeline with a newer Executive class that does. The following code fragment does this. To use it, simply place these two lines at the top of your program, before creating any filters. 

```cpp
vtkSmartPointer<vtkCompositeDataPipeline> cdp =
vtkSmartPointer<vtkCompositeDataPipeline>::New();
vtkAlgorithm::SetDefaultExecutivePrototype(cdp);
```

As with any other type of data, the most important step towards using VTK to visualize time varying data is to get the data into a format that the VTK pipeline can process. As Chapter 9 explains, this essentially means finding a reader, which can read the file that you are working with. If the data is time varying, you must also be sure that that the reader knows about the new pipeline features described in (2 above), or in other words is time aware.

There are a growing number of readers in VTK, which are time aware. Examples include (along with subclasses and relatives of the following): 
- vtkExodusReader - readers for Sandia National Lab's Exodus file format 
- vtkEnsightReader - readers CEI's EnSight file format 
- vtkLSDynaReader - reader for Livermore Software Technology Corporation's multiphysics simulation software package files 
- vtkXMLReader - readers for Kitware's newer XML based file format

Once you find such a reader, using it then becomes a matter of instantiating the reader, setting a filename, and calling update. You can programmatically get the available temporal domain from the file by calling UpdateInformation on the reader, and can tell it to update at a specific time by calling SetUpdateTimeStep(int port, double time), followed by a call to Update().

The following code segment illustrates how to instantiate a time aware reader and query it for the time domain in a file. 

```cpp
vtkSmartPointer<vtkGenericEnSightReader> r =
vtkSmartPointer<vtkGenericEnSightReader>::New();
r->SetCaseFileName(".../VTKData/Data/EnSight/naca.bin.case");
// Update meta-data. This reads time information and other meta-data.
r->UpdateInformation();
// The meta-data is in the output information
vtkInformation* outInfo = r->GetExecutive()->GetOutputInformation(0);
if (outInfo.Has(vtkStreamingDemandDrivenPipeline::TIME_STEPS()))
{
cout << "Times are:" << endl;
for(int i=0; i<outInfo->Length(vtkStreamingDemandDrivenPipeline::TIME_STEPS()), i++)
{
cout << outInfo->Get(vtkStreamingDemandDrivenPipeline::TIME_STEPS(),
i) << endl;
}
}
else
{
cout << "That file has not time content." << endl;
}
```

There are a growing number of readers in VTK which are time aware, but there are many more readers that are not. And there are still more file formats for which no reader yet exists. What exactly must a reader do to support temporal visualization? It must do at least two things. It must announce the temporal range that it has data for, and it must respect the time that is requested of it by the pipeline.

Announcing the range happens during the REQUEST_INFORMATION pipeline pass. Do this by populating the TIME_STEPS and TIME_RANGE keys.

```cpp
int vtkTimeAwareReader::RequestInformation(
vtkInformation* vtkNotUsed(request),
vtkInformationVector** vtkNotUsed(inputVector),
vtkInformationVector* outputVector )
{
vtkInformation* outInfo = outputVector->GetInformationObject(0);
// Read the time information from the file here.
// ...
// Let timeValues be an array of times (type double)
// nSteps is the number of time steps in the array.
outInfo->Set(vtkStreamingDemandDrivenPipeline::TIME_STEPS(),
timeValue, nSteps);
double timeRange[2];
timeRange[0] = timeValue[0];
timeRange[1] = timeValue[nSteps - 1];
outInfo->Set(vtkStreamingDemandDrivenPipeline::TIME_RANGE(),
timeRange, 2);
return 1;
}
```

The reader finds out during the REQUEST_DATA pass, what time or times it is being asked of at present and responds accordingly. The time request comes in the UPDATE_TIME_STEPS key.

```cpp
int vtkTimeAwareReader::RequestData(
vtkInformation* vtkNotUsed(request),
vtkInformationVector** vtkNotUsed(inputVector),
vtkInformationVector* outputVector )
{
vtkInformation* outInfo = outputVector->GetInformationObject(0);
if (outInfo->Has(
vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS()))
{
// Get the requested time steps.
int numRequestedTimeSteps = outInfo->Length(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS());

double* requestedTimeValues = outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS());
double firstTime = requestedTimeValues[0];
double lastTime = requestedTimeValues[numRequestedTimeSteps-1];
// ...
}
// ..
return 1;
}
```

The reader is free to interpret this request however it likes. Most use a floor function to find the nearest lesser exact time value for which they have data. For this reason it is useful to provide the exact time the data produced by the reader actually corresponds to. Placing the DATA_TIME_STEPS key in the output data object does this.

```cpp
double myAnswerTime = this->Floor_in_timeValue(firstTime);
vtkDataObject *output= outInfo->Get(vtkDataObject::DATA_OBJECT());
output->GetInformation()->Set(vtkDataObject::DATA_TIME_STEPS(),
&myAnswerTime, 1);
```

Many readers can satisfy only a single time request in any given call. In this case they are free to produce any particular vtkDataSet subclass. They typically only honor the first requested value as in the preceding code. Other readers can efficiently satisfy multiple time requests. An example might be a reader for a file format the stores only changed values in subsequent time steps. In that case shallow copies of the constant portions of the data are effective. When the reader can provide data at multiple times, it must produce a vtkTemporalDataSet and fill it with the data for each answer. Here is how a filter would create a temporal dataset that has data at times 0.1 and 0.3. 

```cpp
vtkSmartPointer<vtkTemporalDataSet>tds =
vtkSmartPointer<vtkTemporalDataSet>::New();
vtkSmartPointer<vtkPolyData> pd0 = vtkSmartPointer<vtkPolyData>::New();
pd0->GetInformation()->Append(vtkDataObject::DATA_TIME_STEPS(), 0.1);
tds->SetTimeStep(0, pd0);
vtkSmartPointer<vtkPolyData> pd1 = vtkSmartPointer<vtkPolyData>::New();
pd1->GetInformation()->Append(vtkDataObject::DATA_TIME_STEPS(), 0.3);
tds->SetTimeStep(1, pd1);
```

### Time aware filters

There are also a growing number of time aware filters in VTK. The temporal statistics filter is an example. It computes statistics such as the average, minimum, and maximum values as well as the standard deviation of, all attribute values for every point and cell in the input data over all time steps. For the most part, given that you are using the proper Executive and have a time aware source or reader somewhere in the pipeline, using a time aware filter is no different than using any standard filter. Simply set up the pipeline and call update. The following code illustrates. 

```cpp
vtkSmartPointer<vtkTemporalStatistics> ts = vtkSmartPointer<vtkTemporalStatistics>::New()
ts->SetInputConnection(r->GetOutputPort())
ts->Update()

cout << ts->GetOutput()->GetBlock(0)->GetPointData()->GetArray(1)->GetName() << endl;

cout << ts->GetOutput()->GetBlock(0)->GetPointData()->GetArray(1)->GetTuple1(0) < endl;
```

Although the number of time aware filters in VTK is growing, it will never cover every possible temporal analysis technique. When you find that the toolkit lacks a technique that you need, you can write a new filter.

A time aware filter must be able to cooperate with the Executive in order to manipulate the temporal dimension in order to do its work. For example, the temporal statistics filter examines all time steps on its input and summarizes the information. In doing so, it removes time from consideration from downstream filters. A graphing filter that plots value changes over time does the same. The output graph, which has time along the X-axis, is "timeless" and does not itself change as time moves. Filters that act like that should remove the TIME keys from their output in the REQUEST_INFORMATION pass.

```cpp
int vtkTemporalStatistics::RequestInformation(
vtkInformation *vtkNotUsed(request),

vtkInformationVector **vtkNotUsed(inputVector),
vtkInformationVector *outputVector)
{
vtkInformation *outInfo = outputVector->GetInformationObject(0);
// The output data of this filter has no time associated with it. It is the
// result of computations that happen over all time.
outInfo->Remove(vtkStreamingDemandDrivenPipeline::TIME_STEPS());
outInfo->Remove(vtkStreamingDemandDrivenPipeline::TIME_RANGE());
return 1;
}
```

The temporal statistics filter produces a single value, but it needs to ask its own input to produce all of the time steps that it can. It populates the UPDATE_TIME_STEPS key to ask the input filter what times to produce data for. Note, this filter only needs to examine one time step at a time, in effect streaming time as it aggregates results. Thus in this example we ask for only the next time step. Other filters may request more than one time step, or all of them, but should be careful not to overrun memory when doing so.

```cpp
int vtkTemporalStatistics::RequestUpdateExtent(
vtkInformation *vtkNotUsed(request),
vtkInformationVector **inputVector,
vtkInformationVector *vtkNotUsed(outputVector))
{
vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
// The RequestData method will tell the pipeline Executive to iterate the
// upstream pipeline to get each time step in order. On every iteration,
// this method will be called first which gives this filter the opportunity
// to ask for the next time step.
double *inTimes = inInfo-
>Get(vtkStreamingDemandDrivenPipeline::TIME_STEPS());
if (inTimes)
{
inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS(),
&inTimes[this->CurrentTimeIndex], 1);
}
return 1;
}
```

This filter examines one time step at a time, so it needs to iterate over all the time steps to produce the correct result. The application does not have to do the iteration for us, because the filter can tell the Executive to do it on its own. It sets the CONTINUE_EXECUTING() flag to make the Executive loop. On the first call, the filter sets up the loop and set the flag. That causes the REQUEST_UPDATE_EXTENT and REQUEST_DATA passes to happen continuously until the filter decides to remove the flag. At each iteration, the filter asks for a different time step (see RequestUpdateExtent above). After examining all time steps, it clears the flag. At this point the output will have the computed overall statistics.

```cpp
int vtkTemporalStatistics::RequestData(vtkInformation *request,
vtkInformationVector **inputVector,
vtkInformationVector *outputVector)
{
vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
vtkInformation *outInfo = outputVector->GetInformationObject(0);
vtkDataObject *input = vtkDataObject::GetData(inInfo);
vtkDataObject *output = vtkDataObject::GetData(outInfo);

if (this->CurrentTimeIndex == 0)
{
// First execution, initialize arrays.
this->InitializeStatistics(input, output);
}
else
{
// Subsequent execution, accumulate new data.
this->AccumulateStatistics(input, output);
}
this->CurrentTimeIndex++;
if ( this->CurrentTimeIndex < inInfo->Length(vtkStreamingDemandDrivenPipeline::TIME_STEPS()))
{
// There is still more to do.
request->Set(vtkStreamingDemandDrivenPipeline::CONTINUE_EXECUTING(), 1);
}
else
{
// We are done. Finish up.
this->PostExecute(input, output);
request->Remove(vtkStreamingDemandDrivenPipeline::CONTINUE_EXECUTING());
this->CurrentTimeIndex = 0;
}
return 1;
}
```

In the previous example, the filter was written to operate by looking at one time step at a time. For other operation, that may not be practical, geometric interpolation for example requires two time steps. This example demonstrates how a filter can request multiple time steps simultaneously and process them together. To request multiple time steps, you set UPDATE_TIME_STEPS to contain more than one value during the REQUEST_UPDATE_EXTENT pass.

```cpp
int vtkSimpleTemporalInterpolator::RequestUpdateExtent (
vtkInformation * vtkNotUsed(request),
vtkInformationVector **inputVector,
vtkInformationVector *outputVector)
{
// get the info objects
vtkInformation* outInfo = outputVector->GetInformationObject(0);
vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
// Find the time step requested by downstream

if (outInfo->Has(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS()))
{
if (outInfo->Length(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS()) != 1)
{
vtkErrorMacro("This filter can only handle 1 time request");
return 0;
}
upTime = outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS())[0];
double inUpTimes[2];
// Find two time steps that surround upTime here and set inUpTimes
// This requests two time steps from upstream.
inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS(),
inUpTimes, 2);
}
return 1;
}
```

Now REQUEST_DATA will be called only once, but when it does it will be given a temporal data set which contains two time steps. These can be extracted and processed as in the following:

```cpp
int vtkSimpleTemporalInterpolator::RequestData(
vtkInformation *vtkNotUsed(request),
vtkInformationVector **inputVector,
vtkInformationVector *outputVector)
{
vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
vtkInformation *outInfo = outputVector->GetInformationObject(0);
vtkTemporalDataSet *inData = vtkTemporalDataSet::SafeDownCast(
inInfo->Get(vtkDataObject::DATA_OBJECT()));
vtkTemporalDataSet *outData = vtkTemporalDataSet::SafeDownCast(
outInfo->Get(vtkDataObject::DATA_OBJECT()));
// get the input times
double *inTimes = inData->GetInformation()-
>Get(vtkDataObject::DATA_TIME_STEPS());
int numInTimes = inData->GetInformation()-
>Length(vtkDataObject::DATA_TIME_STEPS());
// get the requested update time
upTime = outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEPS())[0];
vtkDataObject *in0 = inData->GetTimeStep(0);
vtkDataObject *in1 = inData->GetTimeStep(1);
// Interpolate in0 and in1 at upTime and produce outData here.
// set the resulting time
outData->GetInformation()->Set(vtkDataObject::DATA_TIME_STEPS(),
upTime, 1);
return 1;
}
```
