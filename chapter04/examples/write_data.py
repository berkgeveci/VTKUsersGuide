"""Demonstrate writing VTK data to several common file formats."""
import os
import sys
import tempfile

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOGeometry import vtkSTLWriter
from vtkmodules.vtkIOLegacy import vtkPolyDataWriter
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter

# Generate a simple sphere dataset.
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.Update()

output_dir = tempfile.mkdtemp(prefix="vtk_write_")

# --- XML format (.vtp) — preferred for VTK-to-VTK workflows ---
xml_writer = vtkXMLPolyDataWriter()
xml_writer.SetFileName(os.path.join(output_dir, "sphere.vtp"))
xml_writer.SetInputConnection(sphere.GetOutputPort())
xml_writer.Write()
print(f"Wrote {xml_writer.GetFileName()}")

# --- STL format — widely used for 3-D printing and CAD exchange ---
stl_writer = vtkSTLWriter()
stl_writer.SetFileName(os.path.join(output_dir, "sphere.stl"))
stl_writer.SetInputConnection(sphere.GetOutputPort())
stl_writer.Write()
print(f"Wrote {stl_writer.GetFileName()}")

# --- Legacy VTK format (.vtk) — simple, human-readable ---
legacy_writer = vtkPolyDataWriter()
legacy_writer.SetFileName(os.path.join(output_dir, "sphere.vtk"))
legacy_writer.SetInputConnection(sphere.GetOutputPort())
legacy_writer.Write()
print(f"Wrote {legacy_writer.GetFileName()}")

print(f"\nAll files written to {output_dir}")
