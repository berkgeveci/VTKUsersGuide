cmake_minimum_required(VERSION 3.12...3.28)
project(HelloWorld)

find_package(VTK
  COMPONENTS
    FiltersSources
    InfovisCore
    InfovisLayout
    InteractionStyle
    RenderingCore
    RenderingOpenGL2
    ViewsInfovis)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "Example ${PROJECT_NAME}: Unable to find the VTK build folder.")
endif()

add_executable(HelloWorld HelloWorld.cxx)
target_link_libraries(HelloWorld PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS HelloWorld
  MODULES ${VTK_LIBRARIES})
