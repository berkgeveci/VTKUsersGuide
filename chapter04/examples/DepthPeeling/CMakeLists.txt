cmake_minimum_required(VERSION 3.12...3.28)
project(DepthPeeling)

find_package(VTK
  COMPONENTS
    CommonCore
    FiltersSources
    FiltersGeometry
    ImagingSources
    InteractionStyle
    RenderingCore
    RenderingOpenGL2)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "Example ${PROJECT_NAME}: Unable to find the VTK build folder.")
endif()

add_executable(DepthPeeling DepthPeeling.cxx)
target_link_libraries(DepthPeeling PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS DepthPeeling
  MODULES ${VTK_LIBRARIES})
