#pragma once

// System Includes
// #include <cmath>
#include <string.h>
#include <cassert>
#include <map>
#include <vector>
#include <set>

// Maya General Includes
#include <maya/MGlobal.h>
#include <maya/MAnimControl.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MMatrix.h>
#include <maya/MAngle.h>
#include <maya/MQuaternion.h>
#include <maya/MEulerRotation.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MString.h>
#include <maya/MDataHandle.h>
#include <maya/MSelectionList.h>

// Function Sets
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MFnToolContext.h>

// Iterators

// Proxies
#include <maya/MPxNode.h>

// Custom
#include "LMAttribute.h"
#include "LMGlobal.h"
#include "LMAnimControl.h"
#include "LMSolve.h"
#include "LMRigUtils.h"
#include "LMPlugin.h"
#include "Utils.h"
#include "MathUtility.h"




class Ik2bSolver : public MPxNode {
public:
	// Public Data
	static const MString typeName;
	static const MTypeId typeId;

	// Node's Input Attributes
	static Attribute attrInFkStart;
	static Attribute attrInFkMid;
	static Attribute attrInFkEnd;
	static Attribute attrInIkHandle;
	static MObject attrInPvX, attrInPvY, attrInPvZ, attrInPv;
	static Attribute attrInTwist;
	static MObject attrInSoftness;
	static MObject attrInFkIk;
	static MObject attrInTime;
	// Nodes's Output Attributes
	static Attribute attrOutUpdateX, attrOutUpdateY, attrOutUpdateZ, attrOutUpdate;

	// In data
	MMatrix matInFkStart, matInFkMid, matInFkEnd, matInIkHandle;
	MVector posInPv;
	MAngle twist;
	double softness, fkIk;
	bool bIsPvConnected;

	// Function sets
	MFnTransform fnRoot, fnFkStart, fnFkMid, fnFkEnd, fnIkHandle, fnPv;

	// Position
	MVector posFkRoot, posFkStart, posFkMid, posFkEnd, posFkHandle, posFkPv;
	MVector posIkRoot, posIkStart, posIkMid, posIkEnd, posIkHandle, posIkPv;
	MVector posOutStart, posOutMid, posOutEnd, posOutHandle, posOutPv;
	// Quats
	MQuaternion quatFkStart, quatFkMid, quatFkEnd, quatFkHandle;
	MQuaternion quatIkStart, quatIkMid, quatIkEnd, quatIkHandle;
	MQuaternion quatOutStart, quatOutMid, quatOutEnd, quatOutHandle;

	MTime timeCurrent, timeCached;

	MObject objSelf;

	// Helpers
	MSelectionList listSel;
	MAnimControl ctrlAnim;

	// Constructors
	Ik2bSolver()
		: MPxNode()
		, bIsPvConnected(false)
	{};
	// Destructors
	~Ik2bSolver() override {};

	// Public methods - overrides
	static void* creator() {return new Ik2bSolver();}
	static MStatus initialize();
	bool isPassiveOutput(const MPlug& plug)	const override;
	virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock) override;
	MStatus setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) override;
	void getCacheSetup(const MEvaluationNode& evalNode,	MNodeCacheDisablingInfo& disablingInfo,	MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const override;
	void postConstructor() override;
	SchedulingType schedulingType() const override {return SchedulingType::kParallel;}

	// Custom solver methods
	void getFkTransforms();
	void getIkTransforms();

	MStatus solveLimb();
	void solveFk();
	void solveIk();
	void blendFkIk();
	void solveFkIk();

	MStatus parseDataBlock(MDataBlock& dataBlock);
	MStatus updateOutput(const MPlug& plug, MDataBlock& dataBlock);
};