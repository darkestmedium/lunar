# Define the project name
project(lunarmayactrl LANGUAGES CXX)

set(CTRL_FILES
	Ctrl.h
	CtrlCommand.h
	CtrlData.h
	CtrlDrawOverride.h
	ShapesDefinition.h
	Ctrl.cpp
	CtrlCommand.cpp
	CtrlData.cpp
	CtrlDrawOverride.cpp
)

# Add the source files for the nested project
add_library(lunarmayactrl SHARED ${CTRL_FILES})

# Link any dependencies needed for the nested project
target_link_libraries(lunarmayactrl PRIVATE Maya::Maya)
