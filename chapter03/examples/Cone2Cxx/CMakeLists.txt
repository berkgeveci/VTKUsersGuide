cmake_minimum_required(VERSION 3.12...3.28)
project(Cone2)

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

add_executable(Cone2 Cone2.cxx)
target_link_libraries(Cone2 PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS Cone2
  MODULES ${VTK_LIBRARIES})
