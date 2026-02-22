// Gaussian splatting of multivariate financial data.
//
// Reads financial.txt containing 3188 loan records, uses three variables
// as spatial axes (monthly payment, interest rate, loan amount) and
// TIME_LATE as the scalar.  Gaussian splatting creates isosurfaces
// showing the full population (translucent white) and late loans (red).
//
// Usage: Finance <path-to-financial.txt>

#include <vtkActor.h>
#include <vtkAxesActor.h>
#include <vtkContourFilter.h>
#include <vtkFloatArray.h>
#include <vtkGaussianSplatter.h>
#include <vtkNew.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkUnstructuredGrid.h>

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

// Read the financial data file and build a dataset from four named columns.
static vtkSmartPointer<vtkUnstructuredGrid> ReadFinancialData(
  const std::string& filename, const std::string& xName,
  const std::string& yName, const std::string& zName,
  const std::string& sName)
{
  std::ifstream file(filename);
  if (!file.is_open())
  {
    std::cerr << "ERROR: Cannot open " << filename << std::endl;
    return nullptr;
  }

  // First non-empty line: NUMBER_POINTS <n>
  std::string line;
  int npts = 0;
  while (std::getline(file, line))
  {
    std::istringstream iss(line);
    std::string tag;
    if (iss >> tag >> npts)
    {
      break;
    }
  }

  if (npts <= 0)
  {
    std::cerr << "ERROR: Invalid number of points" << std::endl;
    return nullptr;
  }

  // Parse columns: each column starts with a tag name followed by npts floats
  std::unordered_map<std::string, std::vector<float>> columns;
  std::string currentTag;
  std::vector<float> currentData;

  while (std::getline(file, line))
  {
    if (line.empty())
    {
      continue;
    }
    std::istringstream iss(line);
    // Try to read as a float to determine if this is data or a tag
    float val;
    if (iss >> val)
    {
      // It's data - first value already read
      currentData.push_back(val);
      while (iss >> val)
      {
        currentData.push_back(val);
      }
    }
    else
    {
      // It's a tag line
      if (!currentTag.empty())
      {
        columns[currentTag] = currentData;
      }
      iss.clear();
      iss.str(line);
      iss >> currentTag;
      currentData.clear();
    }
  }
  if (!currentTag.empty())
  {
    columns[currentTag] = currentData;
  }

  // Normalize a column to [0, 1] range
  auto normalize = [](std::vector<float>& data) {
    float lo = data[0], hi = data[0];
    for (float v : data)
    {
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }
    float range = (hi != lo) ? (hi - lo) : 1.0f;
    for (float& v : data)
    {
      v = (v - lo) / range;
    }
  };

  normalize(columns[xName]);
  normalize(columns[yName]);
  normalize(columns[zName]);
  normalize(columns[sName]);

  // Build unstructured grid
  vtkNew<vtkPoints> points;
  vtkNew<vtkFloatArray> scalars;
  for (int i = 0; i < npts; i++)
  {
    points->InsertPoint(i,
      columns[xName][i], columns[yName][i], columns[zName][i]);
    scalars->InsertValue(i, columns[sName][i]);
  }

  auto dataset = vtkSmartPointer<vtkUnstructuredGrid>::New();
  dataset->SetPoints(points);
  dataset->GetPointData()->SetScalars(scalars);
  return dataset;
}

int main(int argc, char* argv[])
{
  if (argc < 2)
  {
    std::cerr << "Usage: " << argv[0] << " <financial.txt>" << std::endl;
    return EXIT_FAILURE;
  }

  auto dataSet = ReadFinancialData(
    argv[1], "MONTHLY_PAYMENT", "INTEREST_RATE", "LOAN_AMOUNT", "TIME_LATE");
  if (!dataSet)
  {
    return EXIT_FAILURE;
  }

  // Pipeline for original population
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

  // Pipeline for delinquent population
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

  // Axes
  vtkNew<vtkAxesActor> axes;

  // Rendering
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

  renderer->ResetCamera();
  renderWindow->Render();
  interactor->Initialize();
  interactor->Start();

  return EXIT_SUCCESS;
}
