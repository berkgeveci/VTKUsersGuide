# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Markdown conversion of the **VTK Users Guide**, a comprehensive documentation for the Visualization Toolkit (VTK). The original content exists as a PDF (`VTKUsersGuide.pdf`) and is being converted chapter-by-chapter into clean, well-formatted Markdown with extracted high-resolution images.

## Repository Structure

The repository is organized by chapters:
- `chapter03/` through `chapter13/` - Individual chapters in Markdown format
- Each chapter contains:
  - Main content file: `Chapter[N].md` or `ch[N].md`
  - `images/` subdirectory with extracted figures (PNG format, 300 DPI)
  - Optional `README.md` documenting conversion details

## Document Organization

### Chapter Naming
All chapters use consistent naming: `Chapter[N].md` (e.g., `Chapter3.md`, `Chapter4.md`, `Chapter5.md`)

### Content Structure
All chapters follow this Markdown hierarchy:
- H1 (`#`) - Chapter title
- H2 (`##`) - Major sections (e.g., "3.1 System Architecture")
- H3 (`###`) - Subsections

### Code Blocks
The guide contains extensive code examples in multiple languages:
- C++ examples using `vtkSmartPointer`, `vtkNew`, and VTK object model
- Tcl scripts (legacy but still present in examples)
- Python and Java examples
- Code blocks use proper language tagging: ` ```cpp `, ` ```tcl `, ` ```python `

### Images
- All figures extracted at 300 DPI from original PDF
- Named as `Figure_[N]-[M].png` (e.g., `Figure_3-1.png`, `Figure_6-15.png`)
- Referenced in Markdown with relative paths: `![Description](images/Figure_N-M.png)`
- Each figure includes descriptive alt text and caption

## VTK Concepts (for context)

Understanding these VTK concepts will help when editing content:

### Core Architecture
- **Two-tier system**: Compiled C++ core with interpreted language wrappers (Java, Tcl, Python)
- **Visualization pipeline**: Source objects → Filter objects → Mapper objects
- **Rendering engine**: vtkRenderer, vtkRenderWindow, vtkActor, vtkMapper

### Object Model
- All VTK objects derive from `vtkObject` or `vtkObjectBase`
- Reference counting with `New()`, `Delete()`, `Register()`, `UnRegister()`
- Smart pointers via `vtkSmartPointer<>` template
- Run-time type information with `GetClassName()`, `IsA()`, `SafeDownCast()`

### Data Types
Six main dataset types (see Figure 3-2):
- `vtkImageData` - Regular grids (CT/MRI scans)
- `vtkRectilinearGrid` - Rectilinear grids
- `vtkStructuredGrid` - Structured grids
- `vtkPolyData` - Polygonal data
- `vtkUnstructuredGrid` - Unstructured grids
- Parent class: `vtkDataSet`

## Editing Guidelines

### When modifying chapter content:
1. **Preserve technical accuracy** - VTK API references must remain correct
2. **Maintain heading hierarchy** - Don't break H1→H2→H3 structure
3. **Keep image references intact** - Verify relative paths work
4. **Preserve code formatting** - Maintain proper indentation and syntax highlighting
5. **Match existing style** - Follow capitalization and formatting of existing chapters

### Code example formatting:
- Use triple backticks with language identifier
- Preserve original indentation from PDF
- Include explanatory text before/after code blocks
- Reference actual VTK class names correctly (case-sensitive)

### Image handling:
- When adding new figures, use 300 DPI extraction
- Name consistently: `Figure_[Chapter]-[Number].png`
- Include both alt text and caption in Markdown
- Store in chapter's `images/` subdirectory

## Chapter Coverage

Current chapters (3-13):
- **Chapter 3**: System Overview - VTK architecture, object model, pipeline, rendering
- **Chapter 4**: The Basics - Creating models, readers, filters, rendering examples
- **Chapter 5**: Visualization Techniques - Filters organized by data type
- **Chapter 6**: Image Processing & Visualization - vtkImageData operations
- **Chapter 7-13**: Advanced topics (volume rendering, widgets, interaction, etc.)

## Source Material

- Original PDF: `VTKUsersGuide.pdf` in repository root
- Conversion tools used: pdfplumber, pdf2image, PIL
- Target format: GitHub-flavored Markdown with CommonMark compatibility
