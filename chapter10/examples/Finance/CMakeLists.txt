cmake_minimum_required(VERSION 3.12...3.28)
project(Finance)

find_package(VTK
  COMPONENTS
    CommonCore
    CommonDataModel
    FiltersCore
    ImagingHybrid
    InteractionStyle
    RenderingAnnotation
    RenderingCore
    RenderingOpenGL2)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "Example ${PROJECT_NAME}: Unable to find the VTK build folder.")
endif()

add_executable(Finance Finance.cxx)
target_link_libraries(Finance PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS Finance
  MODULES ${VTK_LIBRARIES})
