cmake_minimum_required(VERSION 3.16)

project(lunar VERSION 0.3.0 DESCRIPTION "Lunatic's Animation and Rigging Framework" LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# set(MAYA_VERSION 2023 CACHE STRING "Maya version")
set(MAYA_VERSION 2022 CACHE STRING "Maya version")
# set(MAYA_PYTHON YES CACHE STRING "Link the python module to mayapy")
# set(MAYA_2022_PYTHON 2 CACHE STRING "Major Version of python when compiling for Maya 2022")
# set(SYSTEM_PY_VERSON 3 CACHE STRING "If Not linking to mayapy, the installed version of python to use")
# set(BUILD_MAYA YES CACHE STRING "Build the maya plugin")
# set(BUILD_PYTHON YES CACHE STRING "Build the python module")


add_subdirectory("src/maya")

# if (${BUILD_MAYA})
# 	# Build the maya plugin
# 	add_subdirectory("src/maya")
# endif()
