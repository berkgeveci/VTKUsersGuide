cmake_minimum_required(VERSION 3.12...3.28)
project(QtCone)

find_package(VTK
  COMPONENTS
    CommonCore
    FiltersSources
    GUISupportQt
    InteractionStyle
    RenderingCore
    RenderingOpenGL2)

if (NOT VTK_FOUND)
  message(FATAL_ERROR "Example ${PROJECT_NAME}: Unable to find the VTK build folder.")
endif()

find_package("Qt${VTK_QT_VERSION}" COMPONENTS Core Widgets REQUIRED)

set(CMAKE_AUTOMOC ON)

add_executable(QtCone QtCone.cxx)
target_link_libraries(QtCone
  PRIVATE
    ${VTK_LIBRARIES}
    "Qt${VTK_QT_VERSION}::Core"
    "Qt${VTK_QT_VERSION}::Widgets")

vtk_module_autoinit(
  TARGETS QtCone
  MODULES ${VTK_LIBRARIES})
