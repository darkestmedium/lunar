#pragma once

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
#include "Utils.h"
#include "MathUtility.h"
#include "LMObject.h"




namespace LMSolve {
	/* LMSolver
	 * Lunar Maya Solver utiliteis
	 */


	inline double softenIk(double lenAT, double lenAB, double vecBC, double lenABC, double softness) {
		/* Softness the AT length if required.
		*/
		lenAT = std::max(lenAT, lenAB - vecBC);
		double da = lenABC - softness;
		double softAT = da + softness * (1.0 - std::exp((da-lenAT)/softness));
		return (lenAT > da && da > 0.0) ? softAT : lenAT;
	}


	inline MStatus twoBoneIk(
		const MVector& vecA, const MVector& vecB, const MVector& vecC, const MVector& vecT, const MVector& vecPv,
		MAngle& twist, double softness, bool bIsPvConnected,
		MQuaternion& quatA, MQuaternion& quatB
		) {
		/* Calculates the ik for a two bone limb.
		
		Reference:
			https://theorangeduck.com/page/simple-two-joint
			https://github.com/chadmv/cmt/blob/master/src/ikRigNode.cpp

		*/
		// MStatus status;

		// From to Vectors - reusable
		MVector vecAB = vecB - vecA;
		MVector vecAC = vecC - vecA;
		MVector vecAT = vecT - vecA;
		MVector vecBC = vecC - vecB;
		MVector vecAPv = vecPv - vecA;
	
		// Direction vector
		MVector vecD = (vecB - (vecA + (vecAC * (vecAB * vecAC)))).normal();
	
		// Lengths
		double lenAB = vecAB.length();
		double lenCB = (vecB - vecC).length();
		double lenABC = lenAB + lenCB;
		double lenAT = clamp(vecAT.length(), kEpsilon, lenABC - kEpsilon);

		// Soften the edge if required
		if (softness > 0.0) {lenAT = softenIk(vecAT.length(), lenAB, vecBC.length(), lenABC, softness);}

		// Get current interior angles of start and mid
		double ac_ab_0 = acos(clamp((vecAC).normal() * (vecAB).normal(), -1.0, 1.0));
		double ba_bc_0 = acos(clamp((vecA - vecB).normal() * vecBC.normal(), -1.0, 1.0));
		double ac_at_0 = acos(clamp((vecAC).normal() * (vecAT).normal(), -1.0, 1.0));
		// Get desired interior angles
		double ac_ab_1 = acos(clamp((lenCB * lenCB - lenAB * lenAB - lenAT * lenAT) / (-2 * lenAB * lenAT), -1.0, 1.0));
		double ba_bc_1 = acos(clamp((lenAT * lenAT - lenAB * lenAB - lenCB * lenCB) / (-2 * lenAB * lenCB), -1.0, 1.0));

		MVector axis0 = (vecAC ^ vecD).normal();
		MVector axis1 = (vecAC ^ vecAT).normal();

		MQuaternion r0(ac_ab_1 - ac_ab_0, axis0);
		MQuaternion r1(ba_bc_1 - ba_bc_0, axis0);
		MQuaternion r2(ac_at_0, axis1);

		// Pole vector rotation
		// MQuaternion r3;
		// if (bIsPvConnected) {
		// Determine the rotation used to rotate the normal of the triangle formed by
		// a.b.c post r0*r2 rotation to the normal of the triangle formed by triangle a.pv.t
		MVector n1 = (vecAC ^ vecAB).normal().rotateBy(r0).rotateBy(r2);
		MVector n2 = (vecAT ^ vecAPv).normal();
		MQuaternion r3 = n1.rotateTo(n2);
		// } else {
		// 	MVector vecRA = vecA - vecR;
		// 	MVector n1 = (vecRA ^ vecAT).normal();
		// 	MVector n2 = (n1 ^ vecAT).normal();
		// 	r3 = vecAPv.rotateTo(n2);
		// }

		// Rotation cross vectors and twist
		MQuaternion quatTwist(twist.asRadians(), vecAT);

		quatA *= r0 * r2 * r3 * quatTwist;

		quatB *= r1 * r0 * r2 * r3 * quatTwist;

		return MS::kSuccess;
	}

	// inline MStatus threeBoneIk(
	// 	const MVector& vecA, const MVector& vecB, const MVector& vecC, const MVector& vecD, const MVector& vecT, const MVector& vecPv,
	// 	MAngle& twistA, MAngle& twistB, double softness,
	// 	MQuaternion& quatA, MQuaternion& quatB, MQuaternion& quatC
	// ) {
	// 	/* Calculates the ik for a three bone limb.

	// 	Reference:
	// 		https://github.com/keenanwoodall/Kinematic-Trees-3DB2/blob/master/src/ThreeJointSolver.cpp

	// 	*/

	// 	MStatus status;

	// 	// From to Vectors - reusable
	// 	MVector vecAB = vecB - vecA;
	// 	MVector vecAC = vecC - vecA;
	// 	MVector vecAD = vecD - vecA;
	// 	MVector vecAT = vecT - vecA;
	// 	MVector vecBC = vecC - vecB;
	// 	MVector vecBD = vecD - vecB;
	// 	MVector vecCD = vecD - vecC;

	// 	// Lengths
	// 	double lenAB = vecAB.length();
	// 	double lenAC = vecAC.length();
	// 	double lenAD = vecAD.length();
	// 	double lenBC = vecBC.length();
	// 	double lenBD = vecBD.length();
	// 	double lenCD = vecCD.length();
	// 	double lenABC = lenAB + lenBC;
	// 	double lenABD = lenAB + lenBD;
	// 	double lenABCD = lenAB + lenBC + lenCD;

	// 	// Soften the edge if required
	// 	if (softness > 0.0) {
	// 		lenAD = softenIk(lenAD, lenABD, lenBD, lenABCD, softness);
	// 		lenAT = softenIk(lenAT.length(), lenAB, lenBC, lenABC, softness);
	// 	}

	// 	// Get current interior angles of start and mid
	// 	double ac_ab_0 = acos(clamp((vecAC).normal() * (vecAB).normal(), -1.0, 1.0));
	// 	double ba_bc_0 = acos(clamp((vecA - vecB).normal() * vecBC.normal(), -1.0, 1.0));
	// 	double cd_bc_0 = acos(clamp((vecC - vecD).normal() * vecBD.normal(), -1.0, 1.0));
	// 	double ac_ad_0 = acos(clamp((vecAC).normal() * (vecAD).normal(), -1.0, 1.0));

	// 	// Calculate the twist angles
	// 	double abcPlaneDot = (vecAB ^ vecBC) * vecAC;
	// 	twistA = MAngle(-atan2(abcPlaneDot, lenAB * lenBC));

	// 	double bcdPlaneDot = (vecBC ^ vecCD) * vecBD;
	// 	twistB = MAngle(-atan2(bcdPlaneDot, lenBC * lenCD));

	// 	// Calculate the quaternions
	// 	quatA = MQuaternion(vecAB, -ac_ab_0 - twistA.asRadians(), MVector(1, 0, 0));
	// 	quatB = MQuaternion(vecBC, ba_bc_0 + twistA.asRadians() - twistB.asRadians(), vecAB);
	// 	quatC = MQuaternion(vecCD, cd_bc_0 + twistB.asRadians(), vecBC);

	// 	// Calculate the pole vector quaternion
	// 	MQuaternion quatPv = MQuaternion(vecA - vecPv, vecAT.normal());
	// 	MQuaternion quatPvInv = quatPv.inverse();

	// 	// Rotate the quaternions by the pole vector
	// 	quatA = quatPv * quatA * quatPvInv;
	// 	quatB = quatPv * quatB * quatPvInv;
	// 	quatC = quatPv * quatC * quatPvInv;

	// 	// Get the target angles for start and mid
	// 	double ac_ab_1 = getAngleForSideLengths(lenAB, lenAC, lenAT.length());
	// 	double ba_bc_1 = getAngleForSideLengths(lenBC, lenAB, lenAT.length());
	// 	double cd_bc_1 = getAngleForSideLengths(lenBC, lenBD, lenAD);

	// 	// Calculate the twist angles
	// 	double twist1 = twistA.asRadians() + (ac_ab_1 - ac_ab_0);
	// 	double twist2 = twistB.asRadians() + (cd_bc_1 - cd_bc_0);

	// 	// Get the joint quaternions
	// 	MQuaternion r1, r2, r3;
	// 	status = getQuaternionForTwoBone(vecAB, vecAC, vecAT, ac_ab_1, r1);
	// 	if (status != MS::kSuccess) {
	// 		return status;
	// 	}
	// 	status = getQuaternionForTwoBone(vecCD, vecBD, -vecAT, cd_bc_1, r2);
	// 	if (status != MS::kSuccess) {
	// 		return status;
	// 	}
	// 	status = getQuaternionForTwoBone(vecBC, vecAB, vecCD, ba_bc_1, r3);
	// 	if (status != MS::kSuccess) {
	// 		return status;
	// 	}

	// 	// Apply the twist rotations
	// 	applyTwistRotation(r1, vecAB, vecAT, twist1);
	// 	applyTwistRotation(r2, vecCD, -vecAT, twist2);

	// 	// Combine the quaternions
	// 	quatA = r1;
	// 	quatB = r3 * quatA;
	// 	quatC = r2 * quatB;

	// 	// Apply pole vector constraint
	// 	MVector effectorPos = vecC + quatC * vecCD;
	// 	MVector poleVectorDir = (vecPv - vecA).normal();
	// 	MVector effectorDir = (effectorPos - vecA).normal();
	// 	MQuaternion q = MVector::kIdentity;
	// 	if (!effectorDir.isParallel(poleVectorDir)) {
	// 		q = getQuaternionFromTo(effectorDir, poleVectorDir, vecAT);
	// 	}
	// 	if (!q.isEquivalent(MQuaternion::identity, 1e-10)) {
	// 		quatB = q * quatB;
	// 		quatC = q * quatC;
	// 	}

	// 	return MS::kSuccess;
	// }
};