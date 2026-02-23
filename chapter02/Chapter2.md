# Chapter 2: Installation

This chapter describes how to install VTK on your computer. For most users, installing a pre-built package is the quickest way to get started. Pre-built packages are available for Python (via pip), conda, Homebrew, and Linux distribution package managers. If you need to customize VTK's build -- for example, to enable optional features like MPI, Qt integration, or Java wrapping -- you will need to build VTK from source code using CMake.

## 2.1 Overview

VTK runs on Windows, macOS, and Linux. The best installation method depends on how you plan to use VTK:

- **Python users**: Install via `pip` or `conda`. This is the easiest approach and provides the full VTK Python API with no compilation required.
- **C++ users**: Install via a system package manager (Homebrew, apt, vcpkg, Spack) or build from source. Building from source gives you the most control over which modules and features are included.
- **Java users**: Build from source with `VTK_WRAP_JAVA` enabled.

The remainder of this chapter covers pre-built installation options first, then describes how to build VTK from source for users who need a custom build.

## 2.2 Pre-Built Packages

### Python (pip)

The simplest way to install VTK for Python is from PyPI. Wheels are available for Python 3.9 through 3.14 on Windows, macOS, and Linux (x86-64 and ARM64):

```bash
pip install vtk
```

It is good practice to use a virtual environment:

```bash
python -m venv ./vtk-env
source ./vtk-env/bin/activate   # Linux/macOS
pip install vtk
```

To verify the installation:

```python
import vtk
print(vtk.vtkVersion.GetVTKVersion())
```

Note that the PyPI wheels include VTK's core modules and Python wrapping but may not include every optional feature (for example, MPI support or Qt widgets). If you need these features, build from source.

For a higher-level, more Pythonic interface to VTK, consider the PyVista library (`pip install pyvista`), which wraps VTK with a simplified API.

### Conda

VTK is available on conda-forge for Windows, macOS, and Linux:

```bash
conda install conda-forge::vtk
```

The conda-forge package includes Python wrapping and many common optional dependencies.

### Homebrew (macOS and Linux)

On macOS (and Homebrew-on-Linux), VTK can be installed as a formula that includes C++ headers, libraries, and Python bindings:

```bash
brew install vtk
```

The Homebrew formula builds VTK with Qt support and a broad set of dependencies including Boost, Eigen, HDF5, NetCDF, and others.

### Linux Distribution Packages

Most Linux distributions ship VTK packages in their repositories. The Python bindings and the C++ development libraries are separate packages -- install only what you need.

**Ubuntu / Debian:**

```bash
# Python bindings only
sudo apt install python3-vtk9

# C++ development (headers and libraries)
sudo apt install libvtk9-dev

# Qt integration headers
sudo apt install libvtk9-qt-dev
```

**Fedora:**

```bash
# Python bindings only
sudo dnf install python3-vtk

# C++ development (headers and libraries)
sudo dnf install vtk-devel

# Python bindings with MPI support
sudo dnf install python3-vtk-openmpi
```

Distribution packages can lag behind the latest VTK release. For example, Ubuntu 24.04 ships VTK 9.1 while the latest release is 9.4. For the most current version, use pip or build from source.

### vcpkg (C++ Projects)

For C++ projects using Microsoft's vcpkg package manager:

```bash
vcpkg install vtk
```

Or in manifest mode, add to your project:

```bash
vcpkg add port vtk
```

vcpkg integrates with CMake via toolchain files, making it straightforward to use VTK in C++ projects on Windows, macOS, and Linux.

### Spack (HPC Environments)

Spack is a package manager designed for high-performance computing environments. It can build VTK with fine-grained control over variants such as MPI, Python, and rendering backends:

```bash
spack install vtk +python +mpi
spack load vtk
```

Spack is particularly useful on HPC clusters where you may not have root access and need to build against specific compiler and MPI combinations.

## 2.3 Building from Source

Building from source is required when you need features not included in pre-built packages, want to develop VTK itself, or need to link VTK into a custom C++ application. VTK uses CMake for its build system. CMake is an open-source, cross-platform tool that generates native build files (Makefiles, Ninja build files, Visual Studio solutions, Xcode projects) from platform-independent `CMakeLists.txt` files. For comprehensive and up-to-date build instructions, see https://docs.vtk.org/en/latest/build_instructions/index.html.

### Prerequisites

**Required:**

- **CMake** 3.12 or newer (latest recommended). Download from https://cmake.org.
- **A supported C++ compiler:**
  - GCC 8.0 or newer
  - Clang 7.0 or newer
  - Apple Clang 11.0 (Xcode 11.3.1) or newer
  - Microsoft Visual Studio 2017 or newer
  - Intel 19.0 or newer
- **C++17 support** is required. Ensure your compiler version supports the C++17 standard.

**Optional (depending on desired features):**

- **Python** 3.7 or newer -- for Python wrapping
- **Qt** 5.9 or newer -- for Qt-based GUI modules
- **MPI** (OpenMPI, MPICH, or Microsoft MPI) -- for parallel/distributed computing
- **Java JDK** -- for Java wrapping
- **FFmpeg** -- for video file writing on Unix-like systems
- **OSMesa** -- for software-based off-screen rendering on headless servers

### Platform Setup

**Linux (Ubuntu / Debian):**

```bash
sudo apt install build-essential cmake cmake-curses-gui libgl-dev \
    libegl-dev python3-dev ninja-build
```

The `libgl-dev` package provides the OpenGL development headers required for compilation. These headers are needed regardless of whether you use Mesa or proprietary NVIDIA drivers at runtime. The `libegl-dev` package provides EGL headers, which VTK uses for GPU-accelerated off-screen rendering -- particularly useful on headless servers with NVIDIA GPUs (see the `VTK_OPENGL_HAS_EGL` build option below).

**macOS:**

Install Xcode command line tools and CMake:

```bash
xcode-select --install
brew install cmake ninja
```

**Windows:**

Install CMake and Visual Studio Community Edition (with the "Desktop development with C++" workload). The Ninja build tool (version 1.10.1 or higher) is recommended for faster builds and is included with recent Visual Studio versions.

### Obtaining the Source Code

**From a release tarball:**

Download `VTK-X.Y.Z.tar.gz` from https://vtk.org/download/ and extract it:

```bash
mkdir -p ~/vtk
tar xzf VTK-X.Y.Z.tar.gz -C ~/vtk --strip-components=1 --one-top-level=source
```

**From Git (for latest development or contributing):**

```bash
mkdir -p ~/vtk
git clone --recursive https://gitlab.kitware.com/vtk/vtk.git ~/vtk/source
```

### Configuring the Build

VTK does not support in-source builds. Create a separate build directory and run CMake:

**Linux / macOS:**

```bash
mkdir -p ~/vtk/build
cd ~/vtk/build
ccmake -GNinja ~/vtk/source
```

**Windows (from an x64 Native Tools Command Prompt):**

```bash
ccmake -GNinja -S %HOMEPATH%\vtk\source -B %HOMEPATH%\vtk\build
```

The `-GNinja` flag tells CMake to generate Ninja build files. You can omit it to use the platform default (Unix Makefiles on Linux/macOS, or Visual Studio solution files on Windows). You can also use `cmake-gui` for a graphical interface.

Running CMake is an iterative process. After the initial configure step, CMake presents a list of cache variables that control the build. Modify any variables you need, then configure again. Repeat until no new variables appear, then generate the build files.

### Important Build Settings

VTK offers many CMake options to customize the build. Here are the most commonly used:

**Library type:**

- `BUILD_SHARED_LIBS` (default ON) -- Build shared libraries (`.so`, `.dylib`, `.dll`) rather than static libraries.

**Language wrapping:**

- `VTK_WRAP_PYTHON` (default OFF) -- Enable Python bindings.
- `VTK_WRAP_JAVA` (default OFF) -- Enable Java bindings.

**Feature flags:**

- `VTK_USE_MPI` (default OFF) -- Enable MPI for parallel processing.
- `VTK_USE_CUDA` (default OFF) -- Enable NVIDIA GPU acceleration.
- `VTK_SMP_IMPLEMENTATION_TYPE` (default `Sequential`) -- Select the threading backend for VTK's shared-memory parallel (SMP) filters. Options include `STDThread`, `TBB`, and `OpenMP`. Setting this to `TBB` or `STDThread` enables multithreaded execution of filters that support SMP parallelism.
- `VTK_GROUP_ENABLE_Qt` (default `DONT_WANT`) -- Set to `WANT` or `YES` to build Qt integration modules.
- `VTK_ENABLE_KITS` (default OFF) -- Consolidate VTK's many individual libraries into a smaller set of "kit" libraries. This significantly reduces the number of libraries to link against and speeds up linking. Requires `BUILD_SHARED_LIBS=ON`.
- `VTK_BUILD_TESTING` (default OFF) -- Build the test suite.
- `VTK_BUILD_EXAMPLES` (default OFF) -- Build example programs.

**Module control:**

VTK is organized into modules that can be individually enabled or disabled:

- `VTK_BUILD_ALL_MODULES` (default OFF) -- Enable all available modules.
- `VTK_MODULE_ENABLE_<name>` -- Set a specific module to `YES`, `WANT`, `DEFAULT`, `DONT_WANT`, or `NO`.
- `VTK_GROUP_ENABLE_<name>` -- Enable or disable an entire group of modules (e.g., `Rendering`, `IO`, `Qt`).
- `VTK_USE_EXTERNAL` (default OFF) -- Prefer system-installed third-party libraries (e.g., zlib, libpng, Eigen, HDF5) over VTK's bundled copies. Useful in HPC environments and Linux distributions where you want to link against shared system libraries.

**Rendering and display:**

- `VTK_USE_X` (default ON on Linux) -- Use X11 for render windows. Set to OFF for headless builds or to use Wayland instead.
- `VTK_OPENGL_HAS_EGL` (default ON on Linux, OFF elsewhere) -- Build with EGL support for GPU-accelerated off-screen rendering. Required for headless rendering on NVIDIA GPUs.
- `VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN` (default OFF) -- When ON, render windows default to off-screen mode. Useful for batch processing on servers.
- `VTK_DEFAULT_RENDER_WINDOW_HEADLESS` (default OFF) -- When ON, `vtkRenderWindow::New()` creates a headless (EGL) render window instead of an X11 or Wayland window. Only available when the build supports both on-screen and headless rendering.

The render window backend can also be overridden at runtime by setting the `VTK_DEFAULT_OPENGL_WINDOW` environment variable. For example, on a Linux build that includes both X11 and EGL support, setting `VTK_DEFAULT_OPENGL_WINDOW=vtkEGLRenderWindow` forces headless EGL rendering without rebuilding VTK.

**Installation:**

- `CMAKE_INSTALL_PREFIX` -- Where `make install` or `cmake --install` will place files (default `/usr/local` on Unix).
- `VTK_VERSIONED_INSTALL` (default ON) -- Include version numbers in installed paths.

For a complete list of build settings, see https://docs.vtk.org/en/latest/build_instructions/build_settings.html.

### Building

After configuration is complete:

**Linux / macOS:**

```bash
cmake --build ~/vtk/build
```

**Windows (Ninja):**

```bash
cmake --build %HOMEPATH%\vtk\build --config Release
```

**Windows (Visual Studio):**

Open the generated `VTK.sln` file, set the configuration to Release, and build the `ALL_BUILD` target.

Ninja and Make both support parallel builds. With Make, pass `-j N` where N is the number of parallel jobs (e.g., `cmake --build ~/vtk/build -- -j8`). Ninja uses parallel builds by default.

### Installing

After building, you can install VTK system-wide:

```bash
cmake --install ~/vtk/build
```

This installs headers, libraries, and CMake package files to the location specified by `CMAKE_INSTALL_PREFIX`. On Unix systems, the default is `/usr/local`. If you do not have root privileges, set `CMAKE_INSTALL_PREFIX` to a directory you own (e.g., `~/vtk/install`).

### Using VTK in Your C++ Project

Once VTK is installed (or built), you can use it in your own CMake-based project. In your `CMakeLists.txt`:

```cmake
find_package(VTK REQUIRED COMPONENTS CommonCore RenderingCore InteractionStyle)

add_executable(MyApp main.cpp)
target_link_libraries(MyApp PRIVATE ${VTK_LIBRARIES})
vtk_module_autoinit(TARGETS MyApp MODULES ${VTK_LIBRARIES})
```

The `vtk_module_autoinit` call is required to ensure that VTK's object factory overrides are properly initialized. The `COMPONENTS` listed should match the VTK modules your code uses -- check the VTK header file locations to determine which module provides each class.

If VTK is not installed to a standard system path, tell CMake where to find it:

```bash
cmake -DVTK_DIR=~/vtk/build ..
```

## 2.4 Cross-Compiling for Mobile and WebAssembly

VTK can be cross-compiled for iOS, Android, and WebAssembly (via Emscripten). Each platform uses a top-level CMake flag that configures the entire build for the target. For detailed and up-to-date instructions, see https://docs.vtk.org/en/latest/advanced/build_for_mobile.html.

### iOS

Set `VTK_IOS_BUILD=ON` to build `vtk.framework` for iOS. This delegates to an internal CMake script that cross-compiles for both device and simulator architectures:

```bash
mkdir ~/vtk/ios-build && cd ~/vtk/ios-build
cmake -DVTK_IOS_BUILD=ON -GNinja ~/vtk/source
ninja
```

Key iOS options:

- `IOS_DEVICE_ARCHITECTURES` (default `arm64`) -- Target architectures for physical devices.
- `IOS_SIMULATOR_ARCHITECTURES` (default `x86_64`) -- Target architectures for the simulator.
- `IOS_DEPLOYMENT_TARGET` -- Minimum iOS version (detected automatically from the SDK).

The build produces a `vtk.framework` that can be linked into Xcode projects. Static libraries are used (shared libraries are not supported on iOS).

### Android

Set `VTK_ANDROID_BUILD=ON` and point `ANDROID_NDK` to your NDK installation:

```bash
mkdir ~/vtk/android-build && cd ~/vtk/android-build
cmake -DVTK_ANDROID_BUILD=ON \
      -DANDROID_NDK=/path/to/android-ndk \
      -DANDROID_NATIVE_API_LEVEL=27 \
      -DANDROID_ARCH_ABI=arm64-v8a \
      -GNinja ~/vtk/source
ninja
```

Key Android options:

- `ANDROID_NDK` -- Path to the Android NDK (defaults to `$ANDROID_NDK` environment variable or `/opt/android-ndk`).
- `ANDROID_NATIVE_API_LEVEL` (default `27`) -- Target Android API level.
- `ANDROID_ARCH_ABI` (default `armeabi`) -- Target CPU architecture (e.g., `arm64-v8a`, `x86_64`).

Static libraries are used. OpenGL ES 3 and EGL are enabled automatically.

### WebAssembly (Emscripten)

VTK can be compiled to WebAssembly using Emscripten, enabling VTK-based applications to run in web browsers. This requires the Emscripten SDK, CMake 3.29 or newer, and Ninja:

```bash
source /path/to/emsdk/emsdk_env.sh
mkdir ~/vtk/wasm-build && cd ~/vtk/wasm-build
emcmake cmake -DBUILD_SHARED_LIBS=OFF \
              -DVTK_ENABLE_WEBGPU=ON \
              -GNinja ~/vtk/source
ninja
```

Key WebAssembly options:

- `VTK_ENABLE_WEBGPU` -- Enable the WebGPU rendering backend (required for WebAssembly rendering).
- `VTK_WEBASSEMBLY_64_BIT` (default OFF) -- Build for 64-bit WebAssembly (wasm64), allowing up to 16 GB of addressable memory.
- `VTK_WEBASSEMBLY_THREADS` (default OFF) -- Enable pthreads via WebWorkers.

Shared libraries are not supported; `BUILD_SHARED_LIBS` must be OFF.

## 2.5 Getting Help

If you run into problems during installation or building, the following resources are available:

- **VTK Discourse forum**: https://discourse.vtk.org -- The primary community support channel.
- **VTK documentation**: https://docs.vtk.org -- Official documentation including build instructions, API reference, and examples.
- **VTK issue tracker**: https://gitlab.kitware.com/vtk/vtk/-/issues -- For reporting bugs.
- **Commercial support**: Available from Kitware (https://www.kitware.com).
