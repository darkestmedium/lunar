# Define the project name
project(lunarmayaapi LANGUAGES CXX)

set(API_FILES
	# Api
	LMAttribute.h
	LMGlobal.h
	LMAnimControl.h
	LMObject.h
	LMPlugin.h
	LMRigUtils.h
	LMScene.h
	LMSolve.h
	LMText.h
	MathUtility.h
	Utils.h
)

# # Add the source files for the nested project
# add_library(lunarmayaapi SHARED ${API_FILES})

# # Link any dependencies needed for the nested project
# target_link_libraries(lunarmayaapi PRIVATE Maya::Maya)