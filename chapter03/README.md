# Chapter 3: System Overview - VTK Users Guide

Complete conversion of Chapter 3 from the VTK Users Guide to clean, well-formatted Markdown with high-resolution images.

## Contents

- **Chapter3.md** - The complete chapter in Markdown format (45KB)
- **images/** - Directory containing 7 extracted figures

## What's Been Done

### Text Formatting
✓ Removed PDF line breaks within paragraphs  
✓ Preserved paragraph breaks between sections  
✓ Fixed hyphenation artifacts (e.g., "algo- rithms" → "algorithms")  
✓ Removed PDF artifacts (page numbers, headers, sidebar text)  
✓ Cleaned up column layout issues from the original PDF

### Code Formatting  
✓ 37 code blocks properly formatted with ```cpp``` syntax  
✓ All C++ code snippets (vtk classes, methods, etc.) in code blocks  
✓ Preserves original indentation and structure

### Images
✓ 7 figures extracted at 300 DPI (maximum resolution)  
✓ All figures referenced with proper Markdown image syntax  
✓ Each figure includes descriptive alt text and caption  
✓ Relative paths for easy portability

### Document Structure
✓ Proper heading hierarchy (H1 for chapter, H2 for sections)  
✓ Subsections marked with H3  
✓ Clean paragraph formatting throughout

## Figures Included

All images extracted at high resolution (300 DPI, 2175×2850 page size):

1. **Figure_3-1.png** (850×900 px) - VTK architecture with compiled core and interpreted wrappers
2. **Figure_3-2.png** (1820×1650 px) - Six dataset types (Image Data, Rectilinear Grid, Structured Grid, etc.)
3. **Figure_3-3.png** (1850×650 px) - Data attributes (part 1)
4. **Figure_3-3_continued.png** (1850×850 px) - Data attributes (part 2)
5. **Figure_3-4.png** (1850×700 px) - Visualization pipeline with filters
6. **Figure_3-5.png** (1850×1150 px) - Algorithm types (Sources, Filters, Mappers)
7. **Figure_3-6.png** (1850×1100 px) - Pipeline execution flow

## Chapter Sections

- **3.1 System Architecture** - Overview of VTK's two-tier architecture, object model, rendering engine, and visualization pipeline
- **3.2 Create An Application** - Building VTK applications in C++, Tcl, Java, and Python
- **3.3 Conversion Between Languages** - Working across different language bindings

## Usage

The markdown file uses standard syntax and will render properly in:
- GitHub, GitLab, Bitbucket
- Static site generators (Jekyll, Hugo, MkDocs)
- Markdown editors (Typora, Mark Text, VS Code)
- Documentation tools (Sphinx with MyST, Docusaurus)

All image references use relative paths:
```markdown
![Figure 3-1: Description](images/Figure_3-1.png)
```

## Source Information

- **Original PDF**: VTKUsersGuide.pdf  
- **Pages**: 33-54 (22 pages total)
- **Converted**: January 2026
- **Tools**: pdfplumber, pdf2image, PIL
