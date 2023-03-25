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
#include "Utils.h"
#include "MathUtility.h"




class Ik2bSolver : public MPxNode {
public:
	// Public Data
	static const MString typeName;
	static const MTypeId typeId;

	// Node's Input Attributes
	static Attribute inFkStartAttr;
	static Attribute inFkMidAttr;
	static Attribute inFkEndAttr;
	static Attribute inIkHandleAttr;
	static MObject attrInPvX, attrInPvY, attrInPvZ, attrInPv;
	static Attribute inTwistAttr;
	static MObject inSoftnessAttr;
	static MObject inFkIkAttr;
	static MObject AttrInTime;
	// Nodes's Output Attributes
	static Attribute AttrOutUpdateX, AttrOutUpdateY, AttrOutUpdateZ, AttrOutUpdate;

	MObject objFkStart, objFkMid, objFkEnd, objIkhandle, objPoleVector;
	MDagPathArray InOutLinks;
	// In data
	MMatrix matInFkStart, matInFkMid, matInFkEnd, matInIkHandle;
	MVector posInPoleVector;
	double twist, softness, fkIk;
	bool bIsPoleVectorConnected;

	MDagPath pathFkStartParent;
	// Function sets
	MFnTransform FnFkStartParent, FnFkStart, FnFkMid, FnFkEnd, FnIkHandle, FnPoleVector;

	// Position
	// Fk
	MVector PosFkStart, PosFkMid, PosFkEnd, PosFkHandle, PosFkPoleVector;
	// Ik
	MVector PosIkStart, PosIkMid, PosIkEnd, PosIkHandle, PosIkPoleVector;
	// Out
	MVector PosOutStart, PosOutMid, PosOutEnd, PosOutHandle, PosOutPoleVector;
	// Quats
	// Fk
	MQuaternion QuatFkStart, QuatFkMid, QuatFkEnd, QuaFkHandle;
	// Ik
	MQuaternion QuatIkStart, QuatIkMid, QuatIkEnd, QuatIkHandle;
	// Out
	MQuaternion QuatOutStart, QuatOutMid, QuatOutEnd, QuatOutHandle;

	MTime timeCurrent, timeCached;

	MObject objSelf;

	// Helpers
	MSelectionList listSel;
	MAnimControl ctrlAnim;

	// Constructors
	Ik2bSolver()
		: MPxNode()
		// , bIsPoleVectorConnected(false)
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

	MStatus solveLimb(MDagPathArray& InOutLinks);
	void solveFk();
	void solveIk();
	void blendFkIk();
	void solveFkIk();

	MStatus parseDataBlock(MDataBlock& dataBlock, MDagPathArray& InOutLinks);
	MStatus updateOutput(const MPlug& plug, MDataBlock& dataBlock);
};