# Define the project name
project(lunarmayamisc LANGUAGES CXX)

set(MISC_FILES
	MetaDataNode.h
	MetaDataCmd.h
	MetaDataNode.cpp
	MetaDataCmd.cpp
)

# Add the source files for the nested project
add_library(lunarmayamisc SHARED ${MISC_FILES})

# Link any dependencies needed for the nested project
target_link_libraries(lunarmayamisc PRIVATE Maya::Maya)
