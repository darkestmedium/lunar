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

// Custom
#include "LMObject.h"
#include "LMScene.h"




namespace LMAttribute {
	/* LMAttrUtilis
	 * Wrapper namespace for attribute utilities.
	 */


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
	};


	inline MStatus connectSceneTime(MObject& object, MString plug) {
		/* Connects the scene's default time1 node to the given target.
		 */
		MFnDependencyNode fnDestinationtNode = object;
		MPlug plugDestinationInTime = fnDestinationtNode.findPlug(plug, false);

		MFnDependencyNode fnTimeNode = LMScene::getTimeNode();
		MPlug plugTimeOutTime = fnTimeNode.findPlug("outTime", false);
		
		MDGModifier dgMod;
		dgMod.connect(plugTimeOutTime, plugDestinationInTime);
		dgMod.doIt();
	
		return MS::kSuccess;
	};


	inline MObject getSourceObjFromPlug(const MObject& object, const MObject& plug) {
		/* Gets the object from the given plug if it is connected.

		Args:
			Plug (MObject&): Object for the given plug.
		
		Returns:
			MObject: If the plug is a valid connection it will return the obj, otherwise a null object will
				be returned instead.

		*/
		MPlug plugDestination(object, plug);
		if (plugDestination.isConnected()) {
			return plugDestination.source().node();
		}

		return MObject::kNullObj;
	};

}
