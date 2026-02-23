# VTK Users Guide - Markdown Edition

This repository contains a Markdown conversion of the **VTK Users Guide**, transforming the original PDF documentation into clean, accessible, and version-controllable format.

## About VTK

The [Visualization Toolkit (VTK)](https://vtk.org) is an open-source software system for 3D computer graphics, image processing, and visualization. VTK consists of a C++ class library and interpreted interfaces for Tcl/Tk, Java, and Python.

## About This Project

The VTK Users Guide is a comprehensive manual covering VTK's architecture, core concepts, and practical examples. This repository converts the original PDF into well-formatted Markdown with high-resolution extracted images, making the content:

- ✅ Easier to read on any device or platform
- ✅ Searchable and indexable
- ✅ Compatible with static site generators (Jekyll, Hugo, MkDocs, Docusaurus)
- ✅ Version controllable with Git
- ✅ Accessible for modern documentation workflows

## Repository Contents

```
VTKUsersGuide/
├── VTKUsersGuide.pdf          # Original PDF source
├── chapter03/                  # Chapter 3: System Overview
│   ├── Chapter3.md
│   ├── images/                 # 7 high-resolution figures (300 DPI)
│   └── README.md
├── chapter04/                  # Chapter 4: The Basics
│   ├── Chapter4.md
│   └── images/                 # 16 figures
├── chapter05/                  # Chapter 5: Visualization Techniques
│   ├── Chapter5.md
│   └── images/                 # 14 figures
├── chapter06/                  # Chapter 6: Image Processing & Visualization
│   ├── Chapter6.md
│   └── images/                 # 17 figures
├── chapter07/                  # Chapter 7: Volume Rendering
├── chapter08/                  # Chapter 8: Advanced Topics
├── chapter09/                  # Chapter 9: Interaction
├── chapter10/                  # Chapter 10: Rendering
├── chapter11/                  # Chapter 11: Information Visualization
├── chapter12/                  # Chapter 12: Time-Varying Data
└── chapter13/                  # Chapter 13: Parallel Processing
```

## What's Been Converted

All chapters (3-13) have been converted with:

### ✓ Clean Text Formatting
- Removed PDF line breaks and artifacts
- Fixed hyphenation issues
- Proper paragraph and section breaks
- Clean heading hierarchy (H1/H2/H3)

### ✓ Properly Formatted Code
- Syntax-highlighted code blocks (C++, Tcl, Python, Java)
- Preserved indentation and structure
- All VTK class names and API calls properly formatted

### ✓ High-Resolution Images
- All figures extracted at 300 DPI
- Descriptive alt text and captions
- Relative paths for portability
- PNG format for universal compatibility

## Chapter Topics

- **Chapter 3: System Overview** - VTK architecture, object model, visualization pipeline, rendering engine
- **Chapter 4: The Basics** - Creating models, readers, filters, basic rendering examples
- **Chapter 5: Visualization Techniques** - Filters organized by data type (vtkDataSet, vtkPolyData, etc.)
- **Chapter 6: Image Processing & Visualization** - Working with vtkImageData, image filters
- **Chapter 7: Volume Rendering** - Direct volume rendering techniques
- **Chapter 8: Advanced Topics** - Advanced visualization algorithms
- **Chapter 9: Interaction** - User interaction and widgets
- **Chapter 10: Rendering** - Advanced rendering techniques
- **Chapter 11: Information Visualization** - Charts, graphs, and info-vis
- **Chapter 12: Time-Varying Data** - Temporal data handling
- **Chapter 13: Parallel Processing** - Distributed and parallel VTK

## Usage

The Markdown files are compatible with:
- **GitHub/GitLab/Bitbucket** - Native rendering with images
- **Static site generators** - Jekyll, Hugo, MkDocs, Docusaurus
- **Markdown editors** - Typora, Mark Text, VS Code, Obsidian
- **Documentation tools** - Sphinx (with MyST parser), Read the Docs

### Viewing on GitHub
Simply browse to any chapter directory and open the `.md` file. GitHub will render the Markdown with all images.

### Building Documentation
The Markdown files use standard CommonMark syntax with GitHub-flavored Markdown extensions. Image paths are relative, making the files portable across different documentation systems.

Example for MkDocs:
```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - System Overview: chapter03/Chapter3.md
  - The Basics: chapter04/Chapter4.md
  - Visualization Techniques: chapter05/Chapter5.md
  # ... etc
```

## Code Examples

The guide contains extensive code examples demonstrating VTK usage across multiple languages:

**C++ Example:**
```cpp
vtkSmartPointer<vtkCylinderSource> cylinder =
    vtkSmartPointer<vtkCylinderSource>::New();
cylinder->SetResolution(8);
vtkSmartPointer<vtkPolyDataMapper> mapper =
    vtkSmartPointer<vtkPolyDataMapper>::New();
mapper->SetInputConnection(cylinder->GetOutputPort());
```

**Python Example:**
```python
cylinder = vtk.vtkCylinderSource()
cylinder.SetResolution(8)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cylinder.GetOutputPort())
```

## Conversion Details

- **Source**: VTKUsersGuide.pdf
- **Format**: GitHub-flavored Markdown (CommonMark compatible)
- **Images**: 300 DPI PNG extraction
- **Tools**: pdfplumber, pdf2image, PIL
- **Date**: January-February 2026

## Contributing

When contributing improvements to this conversion:
1. Maintain technical accuracy of VTK API references
2. Preserve the H1→H2→H3 heading hierarchy
3. Keep image references with relative paths
4. Use proper code block syntax with language tags
5. Follow existing formatting conventions

## Related Resources

- [VTK Website](https://vtk.org)
- [VTK Documentation](https://docs.vtk.org)
- [VTK Examples](https://examples.vtk.org)
- [VTK Source Code](https://gitlab.kitware.com/vtk/vtk)

## License

Please refer to the original VTK Users Guide licensing terms. This repository contains converted formatting only.
