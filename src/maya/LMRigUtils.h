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




namespace LMRigUtils {
	/* LMRigUtils
	 * Lunar Maya Rig Utilities
	 */

	inline MVector getPoleVectorPosition(MVector& posStart, MVector& posMid, MVector& posEnd) {
		/* Calculates the perfect pole vector position for ik solving.

		From Greg's Hendrix tutorial https://www.youtube.com/watch?v=bB_HL1tBVHY

		*/
		MVector vecStartEnd(posEnd - posStart);
		MVector vecMidEnd(posEnd - posMid);

		double valScale = (vecStartEnd * vecMidEnd) / (vecStartEnd * vecStartEnd);
		MVector vecProjection = (vecStartEnd * valScale) + posStart;
		double lenLimb = (posMid - posStart).length() + vecMidEnd.length();

		return (posMid - vecProjection).normal() * lenLimb + posMid;
	}
};

