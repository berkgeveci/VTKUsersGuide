# Chapter 11: Time Varying Data

## 11.1 Introduction to temporal support

The visualization toolkit was created for the purpose of allowing people to visualize and thus explore features in data with spatial extent. It allows people to answer questions, such as "Where are the regions of maximum value located within this data?" "What shape and value do they have?" and "How are those shapes distributed throughout?" VTK provides a plethora of techniques for displaying and analyzing data, as it exists at a single moment in time. Exploration of data that has temporal extent is also important. One would also like to answer questions such as "How do those shapes grow, move and shrink over time?"

That goal is complicated by the fact that VTK represents a point with only X, Y and Z coordinate values. Adding T is impractical because of backward compatibility requirements and the need to conserve RAM in the most common case in which T is unimportant. With previous versions of the visualization toolkit, people implemented a variety of workarounds to overcome the basic lack of support for time. For instance, multiple attribute array sets (one set for each time step) were sometimes loaded and filters were told to iterate through the sets.

Creating such workarounds was difficult not only because of the lack of support in VTK but also because of the variety of formats in which time varying data is stored. Some practitioners store an entire dataset in a sequentially named file for each (regularly or irregularly sampled) point in time. Others store just the time varying portions of the data in one or many separate files. Some store the T coordinates alongside the X, Y, and Z coordinates as suggested above, and some store the data in highly compressed encoded formats.

As compute power has grown and become widespread, exploration and analysis of time varying scientific data has become commonplace. VTK includes a general-purpose infrastructure for time varying visualization. The infrastructure is not wasteful of memory and is backward compatible. In the common case when time is immaterial, no additional RAM or disk space is consumed, and the majority of filters that are time insensitive do not need any modification. The infrastructure is also open ended and extensible. In addition to supporting flipbook style animations, which would allow one to answer the temporal question posed above, it also allows one to programmatically answer quantitative questions such as:
- "At what time do the shapes take on a maximum volume?"
- "At what point do they move most quickly?"
- "What are the average attribute values over a particular region of time?"
- "What does a 2D plot of values for particular elements or locations look like?"

To do so, one finds or creates a vtkAlgorithm that takes into account the temporal dimension to answer the question, and then builds a pipeline that exercises it. A time-aware filter is one that is capable of: requesting one or more specific time steps from the pipeline behind it, doing some processing once supplied with the requested data objects, and producing an answer (in the form of another data object) for the downstream filters.

The many varieties of temporal representations are facilitated because of the reader abstraction. A reader, as described in Chapter 12, is responsible for reading a file or set of files on the file system, interpreting a specific file format, and producing one or more data objects. A time aware reader is one that additionally tells the pipeline what the available temporal domain is, and is capable of producing an answer (again in the form of a data object) for the specific time that the downstream pipeline has requested of it.

## 11.2 VTK's implementation of time support

VTK supports time varying data at the pipeline level. vtkExecutives are the glue that hold neighboring vtkAlgorithms together and thus make up the pipeline. Besides linking Algorithms together, Executives are also responsible for telling each Algorithm exactly what to do. The Executives do so by communicating meta-information, small pieces of data (stored in vtkInformation containers), up and down the pipeline before causing their attached Algorithms to execute. For example, each Algorithm is given a vtkInformation object that specifies where, or what spatial sub domain it is to fill. When doing temporal visualization, Executives also tell each Algorithm when, or at what point in time they are to do so. Thus each Algorithm can now be given a vtkInformation object that specifies what temporal sub domain that processing is supposed to take place in.

To be exact, the pipeline now supports temporal visualization because it recognizes the following meta-information keys, and understands how and when to transport them and react to their presence in order to drive filter execution.

### TIME_RANGE

This key is injected into the pipeline by a reader of time varying data, at the source or beginning of the pipeline. It contains two floating-point numbers, which are the minimum and maximum times that the reader can produce data within, or in other words, the extent of the temporal domain.

### TIME_STEPS

When the data produced by the reader is exact at discrete points in time, this key is also injected into the pipeline by a reader of time varying data. It contains any number of floating point numbers which may be regularly or irregularly placed within the temporal domain.

### UPDATE_TIME_STEP

This key is injected into the pipeline at the downstream end of the pipeline. It contains a single floating point number that corresponds to the time that is to be processed by the pipeline update.

### DATA_TIME_STEP

When the update request reaches the reader, it may or may not be able to provide results for exactly that time. For example, the renderer may ask for a time that lies between two discrete points in the TIME_STEPS. The reader injects this key into the pipeline to indicate the exact data time that corresponds to the data it produces in response to the request.

### CONTINUE_EXECUTING

This flag is injected into the pipeline to cause the pipeline to keep iterating in order to fulfill a set of time requests.

Because time support was added at the pipeline level, one must know something about how the visualization pipeline executes in order to understand the actions that the above meta information cause, and thus understand what VTK's time support can be used for. VTK's standard streaming demand driven pipeline operates in four stages. The same four passes are used for time varying visualization, but they are often (either for a subset of or for the full pipeline) iterated in a loop.

During the first pass, called REQUEST_DATA_OBJECT, each Executive creates an empty DataObject of whatever type is needed for the Algorithm. A vtkJPEGReader for example, produces an empty vtkImageData.

During the second pass, called REQUEST_INFORMATION, filters produce whatever lightweight meta-information they can about the data they are about to create. A vtkJPEGReader would provide an image extent for example. This pass starts at the upstream end and works forward toward the display. It is during this pass when time aware readers are required to inject their TIME_RANGE and TIME_STEPS keys, which downstream filters and the application can use to guide their actions.

During the third pass, called REQUEST_UPDATE_EXTENT, the filters agree, starting at the downstream end and working back toward the reader, what portion of their input will be required to produce the output they are themselves being asked for. It is at this pass that the UPDATE_TIME_STEP request moves backwards.

During the last pass, called REQUEST_DATA, Algorithms actually do the work requested of them, which means for time varying data, producing data at the time requested and filling in the DATA_TIME_STEP parameter.

At first this appears to still be a brute force approach. One still makes a flipbook animation by stepping through time, updating the pipeline to draw an image at each time. In older versions of VTK, iterating over a loop in which a time parameter was set on the reader and then the display was rendered often did this. In modern VTK, the requested time is set on the renderer or via `SetUpdateTimeStep()` on the pipeline, and the pipeline propagates this information to all upstream filters and readers automatically.

Several details in the implementation make VTK's time support efficient, easy to use, and flexible:

First, Algorithms are free to request and provide multiple times. This makes it possible for any filter to consider more than one time step together. This enables more advanced time varying visualizations than flip books, such as interpolation between time steps and motion blur effects.

Second, the Executive has the ability to automatically iterate portions of the pipeline that are not time aware. This makes it unnecessary for the programmer to explicitly control individual Algorithms in the pipeline. To compute a running average, one would simply set the width or support as a parameter on an averaging filter and then tell the pipeline to execute once.

Third, the Executive, and even Algorithms themselves, are able to manipulate the meta-information keys, which enable techniques such as temporal shifting, scaling and reversion. These are useful in cases such as normalizing data sources to a common frame of reference.

Finally, VTK supports caching of temporal results, and can do so without keeping all results from the reader in memory simultaneously. Caching can give substantial speedups and makes techniques like comparative visualization of the same pipeline at different points in time effective.

### Using time support

As with any other type of data, the most important step towards using VTK to visualize time varying data is to get the data into a format that the VTK pipeline can process. As Chapter 12 explains, this essentially means finding a reader which can read the file that you are working with. If the data is time varying, you must also be sure that the reader is time aware.

There are many readers in VTK which are time aware. Examples include (along with subclasses and relatives of the following):
- vtkExodusIIReader — readers for Sandia National Lab's Exodus file format
- vtkGenericEnSightReader — readers for Ansys EnSight file format
- vtkLSDynaReader — reader for Livermore Software Technology Corporation's multiphysics simulation software package files
- vtkXMLReader — readers for VTK's XML-based file format

Once you find such a reader, using it becomes a matter of instantiating the reader, setting a filename, and calling update. You can programmatically get the available temporal domain from the file by calling `UpdateInformation()` on the reader, and can tell it to update at a specific time by calling `SetUpdateTimeStep()` on the output information, followed by a call to `Update()`.

The following code segment illustrates how to instantiate a time aware reader and query it for the time domain in a file.

```cpp
#include <vtkGenericEnSightReader.h>
#include <vtkInformation.h>
#include <vtkNew.h>
#include <vtkStreamingDemandDrivenPipeline.h>

#include <iostream>

vtkNew<vtkGenericEnSightReader> reader;
reader->SetCaseFileName("naca.bin.case");

// Update meta-data. This reads time information and other meta-data.
reader->UpdateInformation();

// The meta-data is in the output information
vtkInformation* outInfo =
    reader->GetExecutive()->GetOutputInformation(0);

if (outInfo->Has(
        vtkStreamingDemandDrivenPipeline::TIME_STEPS()))
{
    std::cout << "Times are:" << std::endl;
    int numSteps = outInfo->Length(
        vtkStreamingDemandDrivenPipeline::TIME_STEPS());
    for (int i = 0; i < numSteps; i++)
    {
        std::cout << outInfo->Get(
            vtkStreamingDemandDrivenPipeline::TIME_STEPS(), i)
                  << std::endl;
    }
}
else
{
    std::cout << "That file has no time content." << std::endl;
}
```

There are many readers in VTK which are time aware, but there are many more readers that are not. And there are still more file formats for which no reader yet exists. What exactly must a reader do to support temporal visualization? It must do at least two things. It must announce the temporal range that it has data for, and it must respect the time that is requested of it by the pipeline.

Announcing the range happens during the REQUEST_INFORMATION pipeline pass. Do this by populating the TIME_STEPS and TIME_RANGE keys.

```cpp
int vtkTimeAwareReader::RequestInformation(
    vtkInformation* vtkNotUsed(request),
    vtkInformationVector** vtkNotUsed(inputVector),
    vtkInformationVector* outputVector)
{
    vtkInformation* outInfo = outputVector->GetInformationObject(0);

    // Read the time information from the file here.
    // ...
    // Let timeValues be an array of times (type double)
    // nSteps is the number of time steps in the array.
    outInfo->Set(vtkStreamingDemandDrivenPipeline::TIME_STEPS(),
        timeValues, nSteps);

    double timeRange[2];
    timeRange[0] = timeValues[0];
    timeRange[1] = timeValues[nSteps - 1];
    outInfo->Set(vtkStreamingDemandDrivenPipeline::TIME_RANGE(),
        timeRange, 2);

    return 1;
}
```

The reader finds out during the REQUEST_DATA pass what time it is being asked for and responds accordingly. The time request comes in the UPDATE_TIME_STEP key.

```cpp
int vtkTimeAwareReader::RequestData(
    vtkInformation* vtkNotUsed(request),
    vtkInformationVector** vtkNotUsed(inputVector),
    vtkInformationVector* outputVector)
{
    vtkInformation* outInfo = outputVector->GetInformationObject(0);

    if (outInfo->Has(
            vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEP()))
    {
        double requestedTime = outInfo->Get(
            vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEP());
        // Read data for the requested time...
    }
    // ...
    return 1;
}
```

The reader is free to interpret this request however it likes. Most use a floor function to find the nearest lesser exact time value for which they have data. For this reason it is useful to provide the exact time the data produced by the reader actually corresponds to. Placing the DATA_TIME_STEP key in the output data object does this.

```cpp
double myAnswerTime = this->FindNearestTimeValue(requestedTime);
vtkDataObject* output = outInfo->Get(vtkDataObject::DATA_OBJECT());
output->GetInformation()->Set(
    vtkDataObject::DATA_TIME_STEP(), myAnswerTime);
```

### Time aware filters

There are a growing number of time aware filters in VTK. Several useful ones include:

- **vtkTemporalStatistics** — computes statistics (average, minimum, maximum, standard deviation) of all attribute values over all time steps
- **vtkTemporalInterpolator** — interpolates data between time steps
- **vtkTemporalShiftScale** — shifts and scales time values for normalization
- **vtkTemporalSnapToTimeStep** — snaps to the nearest available time step
- **vtkTemporalDataSetCache** — caches time steps in memory for performance
- **vtkTemporalPathLineFilter** — tracks particle paths over time
- **vtkTemporalSmoothing** — smooths data across time steps

For the most part, given that you have a time aware source or reader somewhere in the pipeline, using a time aware filter is no different than using any standard filter. Simply set up the pipeline and call update. The following code illustrates using vtkTemporalStatistics.

```cpp
#include <vtkGenericEnSightReader.h>
#include <vtkNew.h>
#include <vtkTemporalStatistics.h>

vtkNew<vtkTemporalStatistics> stats;
stats->SetInputConnection(reader->GetOutputPort());
stats->Update();

// Access computed statistics from the output
vtkDataSet* output = vtkDataSet::SafeDownCast(
    stats->GetOutput()->GetBlock(0));
std::cout << output->GetPointData()->GetArray(1)->GetName()
          << std::endl;
std::cout << output->GetPointData()->GetArray(1)->GetTuple1(0)
          << std::endl;
```

Although the number of time aware filters in VTK is growing, it will never cover every possible temporal analysis technique. When you find that the toolkit lacks a technique that you need, you can write a new filter.

### Writing a time-aware filter that iterates over all time steps

A time aware filter must cooperate with the Executive in order to manipulate the temporal dimension. For example, the temporal statistics filter examines all time steps on its input and summarizes the information. In doing so, it removes time from consideration for downstream filters. A graphing filter that plots value changes over time does the same. The output graph, which has time along the X-axis, is "timeless" and does not itself change as time moves. Filters that act like that should remove the TIME keys from their output in the REQUEST_INFORMATION pass.

```cpp
int vtkTemporalStatistics::RequestInformation(
    vtkInformation* vtkNotUsed(request),
    vtkInformationVector** vtkNotUsed(inputVector),
    vtkInformationVector* outputVector)
{
    vtkInformation* outInfo = outputVector->GetInformationObject(0);
    // The output data of this filter has no time associated with it.
    // It is the result of computations that happen over all time.
    outInfo->Remove(vtkStreamingDemandDrivenPipeline::TIME_STEPS());
    outInfo->Remove(vtkStreamingDemandDrivenPipeline::TIME_RANGE());
    return 1;
}
```

The temporal statistics filter produces a single value, but it needs to ask its own input to produce all of the time steps that it can. It populates the UPDATE_TIME_STEP key to ask the input filter what time to produce data for. Note, this filter only needs to examine one time step at a time, in effect streaming time as it aggregates results. Thus in this example we ask for only the next time step. Other filters may request more than one time step, but should be careful not to overrun memory when doing so.

```cpp
int vtkTemporalStatistics::RequestUpdateExtent(
    vtkInformation* vtkNotUsed(request),
    vtkInformationVector** inputVector,
    vtkInformationVector* vtkNotUsed(outputVector))
{
    vtkInformation* inInfo = inputVector[0]->GetInformationObject(0);

    // The RequestData method will tell the pipeline Executive to
    // iterate the upstream pipeline to get each time step in order.
    // On every iteration, this method will be called first which
    // gives this filter the opportunity to ask for the next time step.
    double* inTimes = inInfo->Get(
        vtkStreamingDemandDrivenPipeline::TIME_STEPS());
    if (inTimes)
    {
        inInfo->Set(
            vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEP(),
            inTimes[this->CurrentTimeIndex]);
    }
    return 1;
}
```

This filter examines one time step at a time, so it needs to iterate over all the time steps to produce the correct result. The application does not have to do the iteration, because the filter can tell the Executive to do it on its own. It sets the `CONTINUE_EXECUTING()` flag to make the Executive loop. On the first call, the filter sets up the loop and sets the flag. That causes the REQUEST_UPDATE_EXTENT and REQUEST_DATA passes to happen continuously until the filter decides to remove the flag. At each iteration, the filter asks for a different time step (see RequestUpdateExtent above). After examining all time steps, it clears the flag. At this point the output will have the computed overall statistics.

```cpp
int vtkTemporalStatistics::RequestData(
    vtkInformation* request,
    vtkInformationVector** inputVector,
    vtkInformationVector* outputVector)
{
    vtkInformation* inInfo = inputVector[0]->GetInformationObject(0);
    vtkInformation* outInfo = outputVector->GetInformationObject(0);
    vtkDataObject* input = vtkDataObject::GetData(inInfo);
    vtkDataObject* output = vtkDataObject::GetData(outInfo);

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
    if (this->CurrentTimeIndex <
        inInfo->Length(
            vtkStreamingDemandDrivenPipeline::TIME_STEPS()))
    {
        // There is still more to do.
        request->Set(
            vtkStreamingDemandDrivenPipeline::CONTINUE_EXECUTING(),
            1);
    }
    else
    {
        // We are done. Finish up.
        this->PostExecute(input, output);
        request->Remove(
            vtkStreamingDemandDrivenPipeline::CONTINUE_EXECUTING());
        this->CurrentTimeIndex = 0;
    }
    return 1;
}
```

### Writing a filter that requires multiple time steps simultaneously

In the previous example, the filter was written to operate by looking at one time step at a time. For other operations, that may not be practical — geometric interpolation, for example, requires two time steps. VTK provides the `vtkMultiTimeStepAlgorithm` base class for filters that need to process multiple time steps simultaneously.

A subclass of `vtkMultiTimeStepAlgorithm` overrides `RequestUpdateExtent` to specify which time steps it needs, then overrides `Execute` to receive all requested time steps as a vector of data objects. This example demonstrates how a temporal interpolation filter can request two time steps and process them together.

```cpp
#include <vtkMultiTimeStepAlgorithm.h>

class vtkSimpleTemporalInterpolator
    : public vtkMultiTimeStepAlgorithm
{
public:
    static vtkSimpleTemporalInterpolator* New();
    vtkTypeMacro(vtkSimpleTemporalInterpolator,
        vtkMultiTimeStepAlgorithm);

protected:
    int RequestUpdateExtent(
        vtkInformation* vtkNotUsed(request),
        vtkInformationVector** inputVector,
        vtkInformationVector* outputVector) override
    {
        vtkInformation* outInfo =
            outputVector->GetInformationObject(0);
        vtkInformation* inInfo =
            inputVector[0]->GetInformationObject(0);

        if (outInfo->Has(
                vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEP()))
        {
            double upTime = outInfo->Get(
                vtkStreamingDemandDrivenPipeline::UPDATE_TIME_STEP());

            // Find two time steps that surround upTime
            std::vector<double> requestedTimes = {
                timeBefore, timeAfter};
            this->SetTimeSteps(requestedTimes);
        }
        return 1;
    }

    int Execute(
        vtkInformation* request,
        const std::vector<vtkSmartPointer<vtkDataObject>>& inputs,
        vtkInformationVector* outputVector) override
    {
        // inputs[0] is data at timeBefore
        // inputs[1] is data at timeAfter
        vtkDataObject* in0 = inputs[0];
        vtkDataObject* in1 = inputs[1];

        vtkInformation* outInfo =
            outputVector->GetInformationObject(0);
        vtkDataObject* output =
            vtkDataObject::GetData(outInfo);

        // Interpolate in0 and in1 and produce output here.
        // ...
        return 1;
    }
};
```

The `vtkMultiTimeStepAlgorithm` base class takes care of the pipeline iteration needed to collect all requested time steps. The `Execute` method is called once with all the requested data available in the `inputs` vector.
