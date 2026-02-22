#!/usr/bin/env python3
"""Gaussian splatting of multivariate financial data.

Reads financial.txt containing 3188 loan records, selects three
variables (monthly payment, interest rate, loan amount) as spatial
axes and TIME_LATE as the scalar, then uses vtkGaussianSplatter
to visualize both the full population and delinquent loans.
"""

import os

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor, vtkPolyDataMapper, vtkRenderer,
    vtkRenderWindow, vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def read_financial_data(filename, x_name, y_name, z_name, s_name):
    """Read financial data file and return an unstructured grid.

    Selects four named columns: three for spatial coordinates and
    one for the scalar value. Data is normalized to [0, 1].
    """
    with open(filename) as f:
        lines = f.read().split("\n")

    # First line: NUMBER_POINTS <n>
    npts = int(lines[0].split()[1])

    # Parse all columns
    columns = {}
    current_tag = None
    current_data = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()
        # Check if this is a tag line (single non-numeric token)
        try:
            float(tokens[0])
            is_data = True
        except ValueError:
            is_data = False

        if not is_data:
            if current_tag is not None:
                columns[current_tag] = current_data
            current_tag = tokens[0]
            current_data = []
        else:
            current_data.extend(float(t) for t in tokens)

    if current_tag is not None:
        columns[current_tag] = current_data

    # Normalize each selected column
    def normalize(data):
        lo = min(data)
        hi = max(data)
        rng = hi - lo if hi != lo else 1.0
        return [lo + v / rng for v in data]

    xv = normalize(columns[x_name])
    yv = normalize(columns[y_name])
    zv = normalize(columns[z_name])
    sv = normalize(columns[s_name])

    # Build unstructured grid
    points = vtkPoints()
    scalars = vtkFloatArray()
    for i in range(npts):
        points.InsertPoint(i, xv[i], yv[i], zv[i])
        scalars.InsertValue(i, sv[i])

    dataset = vtkUnstructuredGrid()
    dataset.SetPoints(points)
    dataset.GetPointData().SetScalars(scalars)
    return dataset


dataset = read_financial_data(
    os.path.join(data_dir, "financial.txt"),
    "MONTHLY_PAYMENT", "INTEREST_RATE", "LOAN_AMOUNT", "TIME_LATE",
)

# Pipeline for original population (all loans)
pop_splatter = vtkGaussianSplatter()
pop_splatter.SetInputData(dataset)
pop_splatter.SetSampleDimensions(50, 50, 50)
pop_splatter.SetRadius(0.05)
pop_splatter.ScalarWarpingOff()

pop_surface = vtkContourFilter()
pop_surface.SetInputConnection(pop_splatter.GetOutputPort())
pop_surface.SetValue(0, 0.01)

pop_mapper = vtkPolyDataMapper()
pop_mapper.SetInputConnection(pop_surface.GetOutputPort())
pop_mapper.ScalarVisibilityOff()

pop_actor = vtkActor()
pop_actor.SetMapper(pop_mapper)
pop_actor.GetProperty().SetOpacity(0.3)
pop_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

# Pipeline for delinquent population (scaled by TIME_LATE)
late_splatter = vtkGaussianSplatter()
late_splatter.SetInputData(dataset)
late_splatter.SetSampleDimensions(50, 50, 50)
late_splatter.SetRadius(0.05)
late_splatter.SetScaleFactor(0.005)

late_surface = vtkContourFilter()
late_surface.SetInputConnection(late_splatter.GetOutputPort())
late_surface.SetValue(0, 0.01)

late_mapper = vtkPolyDataMapper()
late_mapper.SetInputConnection(late_surface.GetOutputPort())
late_mapper.ScalarVisibilityOff()

late_actor = vtkActor()
late_actor.SetMapper(late_mapper)
late_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Axes
axes = vtkAxesActor()
axes.SetTotalLength(0.15, 0.15, 0.15)

# Rendering
renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(late_actor)
renderer.AddActor(axes)
renderer.AddActor(pop_actor)
renderer.SetBackground(1, 1, 1)
render_window.SetSize(800, 800)

renderer.ResetCamera()
render_window.Render()
interactor.Start()
