cmake_minimum_required(VERSION 3.12...3.28)
project(Antialiasing)

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

add_executable(Antialiasing Antialiasing.cxx)
target_link_libraries(Antialiasing PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS Antialiasing
  MODULES ${VTK_LIBRARIES})
