cmake_minimum_required(VERSION 3.12...3.28)
project(Cylinder)

find_package(VTK
  COMPONENTS
    CommonCore
    FiltersSources
    InteractionStyle
    RenderingCore
    RenderingOpenGL2)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "Example ${PROJECT_NAME}: Unable to find the VTK build folder.")
endif()

add_executable(Cylinder Cylinder.cxx)
target_link_libraries(Cylinder PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS Cylinder
  MODULES ${VTK_LIBRARIES})
