set(MAYA_FILES
# Plugins
	CtrlNode.h
	CtrlNode.cpp
	ComponentNode.h
	CtrlCommand.h
	CtrlCommand.cpp
	FootRollSolver.h
	FootRollSolver.cpp
	Ik2bSolver.h
	Ik2bSolver.cpp
	IkCommand.h
	IkCommand.cpp
	MetaDataCmd.h
	MetaDataCmd.cpp
	MetaDataNode.h
	MetaDataNode.cpp
	ShapesDefinition.h
	TwistSolver.cpp
	TwistSolver.h

	# footPrintNodeGeoOverride.h
	# DisplayNode.h
# # Api
# 	LMAttribute.h
# 	LMGlobal.h
# 	LMAnimControl.h
# 	LMObject.h
# 	LMPlugin.h
# 	LMRigUtils.h
# 	LMScene.h
# 	LMSolve.h
# 	LMText.h
# 	MathUtility.h
# 	Utils.h
# Main
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

# # Add the subdirectory for the nested project
add_subdirectory(api)
# add_subdirectory(ctrl)
# add_subdirectory(solver)
# add_subdirectory(misc)

# # Link the nested project to the root project
# target_include_directories(lunarmayactrl PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/ctrl)
# target_include_directories(lunarmayamisc PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/misc)
# target_include_directories(lunarmayasolver PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/solver)
