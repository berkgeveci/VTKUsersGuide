cmake_minimum_required(VERSION 3.12...3.28)
project(CreateTree)

find_package(VTK
  COMPONENTS
    CommonCore
    CommonDataModel
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

add_executable(CreateTree CreateTree.cxx)
target_link_libraries(CreateTree PRIVATE ${VTK_LIBRARIES})

vtk_module_autoinit(
  TARGETS CreateTree
  MODULES ${VTK_LIBRARIES})
