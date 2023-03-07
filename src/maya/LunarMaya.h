#pragma once

#include "MathUtility.h"

// System Includes
#include <algorithm>
#include <cmath>
#include <limits>
#include <string>
#include <type_traits>
#include <vector>

// Maya General Includes
#include <maya/MSelectionList.h>
#include <maya/MAngle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MEulerRotation.h>
#include <maya/MGlobal.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MQuaternion.h>
#include <maya/MDGModifier.h>
#include <maya/MDagPath.h>

// Function Sets
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
// #include <maya/MFnPlugin.h>

// Iterators

// Proxies
#include <maya/MPxNode.h>




namespace LunarMaya {

	/* MObjectUtils
	 * Wrapper class for attribute utilities.
	 */

	inline MObject getObjFromString(MString name) {
		/* Gets the MObject from the given name.
		 */
		MStatus status;
		MSelectionList listSelection;
		status = listSelection.add(name);
		if (status == MS::kSuccess) {
			MObject mObject;
			listSelection.getDependNode(0, mObject);
			return mObject;
		} else {
			return MObject::kNullObj;
		}
	}


	inline MStatus getDagPathFromString(MString& objectName, MDagPath& path) {
		/* Gets the MDagPath from the given name.
		 */
		MStatus status;
		MSelectionList listSelection;

		status = listSelection.add(objectName);
		if (status == MS::kSuccess)	{
			listSelection.getDagPath(0, path);
			if (path.hasFn(MFn::kTransform) == true) {
				return MS::kSuccess;
			}	else {
				MGlobal::displayError("Given '" + objectName + "' is not a transform node.");
			}
		}	else {
			MGlobal::displayError("Given '" + objectName + "' does not exist.");
		}
		return MS::kFailure;
	};




	/* LMScene
	 * Lunar Maya Scene wrapper class.
	 */
	inline MObject getTimeNode() {return getObjFromString("time1");}




	//--------------------------------------------------------------------------------------------------
	// Utilities
	//--------------------------------------------------------------------------------------------------




	// LMAttrUtilis
	inline MStatus lockAndHideAttr(MPlug& plug) {
		/* Locks and hides the given plug from the channelbox.

		Returns:
			status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
				during the command.

		*/
		MStatus status;
		plug.setKeyable(false);
		plug.setChannelBox(false);
		plug.setLocked(true);

		return MS::kSuccess;
	}


	// MObjectUtils
	inline MStatus connectSceneTime(MObject& object, MString plug) {
		/* Connects the scene's default time1 node to the given target.
		 */
		MFnDependencyNode fnDestinationtNode = object;
		MPlug plugDestinationInTime = fnDestinationtNode.findPlug(plug, false);

		MFnDependencyNode fnTimeNode = getTimeNode();
		MPlug plugTimeOutTime = fnTimeNode.findPlug("outTime", false);
		
		MDGModifier dgMod;
		dgMod.connect(plugTimeOutTime, plugDestinationInTime);
		dgMod.doIt();
		return MS::kSuccess;
	}

};

