#!/usr/bin/env python
#
# This example demonstrates how to embed a VTK render window inside a
# Qt application using PySide6. A cone is rendered in a
# QVTKRenderWindowInteractor widget placed as the central widget of a
# QMainWindow.
#

import sys

# Use QOpenGLWidget as the base class for the VTK widget.  This must
# be set before importing QVTKRenderWindowInteractor.
import vtkmodules.qt
vtkmodules.qt.QVTKRWIBase = "QOpenGLWidget"

from PySide6.QtWidgets import QApplication, QMainWindow

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
)

# Ensure an OpenGL rendering backend and interactor style are loaded
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkInteractionStyle  # noqa: F401

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("VTK Qt Cone Example")
window.resize(800, 600)

# Create the VTK widget and place it in the main window.
vtk_widget = QVTKRenderWindowInteractor(window)
window.setCentralWidget(vtk_widget)

# Build a VTK pipeline.
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(30)

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
