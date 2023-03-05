# Define the project name
project(lunarmayasolver LANGUAGES CXX)

set(CTRL_FILES
	Ik2bSolver.h
	IkCommand.h
	FootRollNode.h
	Ik2bSolver.cpp
	IkCommand.cpp
	FootRollNode.cpp
)

# Add the source files for the nested project
add_library(lunarmayasolver SHARED ${CTRL_FILES})

# Link any dependencies needed for the nested project
target_link_libraries(lunarmayasolver PRIVATE Maya::Maya)
