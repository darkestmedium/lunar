set(MAYA_FILES
	MainPlugin.cpp
)

find_package(Maya REQUIRED)

add_library(mlunar SHARED ${MAYA_FILES})

# Link any dependencies needed for the root project
target_link_libraries(mlunar PRIVATE Maya::Maya)
target_include_directories(mlunar 
	PRIVATE Maya::Maya
	PUBLIC "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}"
)
MAYA_PLUGIN(mlunar)

# Add the subdirectory for the nested project
add_subdirectory("api")
add_subdirectory("ctrl")
add_subdirectory("solver")
add_subdirectory("misc")

# Link the nested project to the root project
# target_link_libraries(mlunar PUBLIC lunarmayaapi)
target_link_libraries(mlunar PUBLIC lunarmayactrl)
target_link_libraries(mlunar PUBLIC lunarmayasolver)
target_link_libraries(mlunar PUBLIC lunarmayamisc)