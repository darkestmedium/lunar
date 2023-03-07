#pragma once

#include "Utils.h"
#include "MathUtility.h"

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



// class MLimbLink
// {
// public:
// 	// MDagPath DagPath;
// 	MFnTransform FnTransform;
// 	// Location of bone in component (or world?) space.
// 	MVector Location;

// 	// Distance to its parent
// 	float Length;

// 	// Axis utilites
// 	MVector LinkAxisZ;
// 	MVector RealBendDir;
// 	MVector BaseBendDir;

// 	// Constructors
// 	MLimbLink(const MDagPath& DagPath)
// 		: FnTransform(DagPath)
// 		, Location(GetLocation())
// 		, Length(0.f)
// 		, LinkAxisZ(MVector::zero)
// 		, RealBendDir(MVector::zero)
// 		, BaseBendDir(MVector::zero)
// 	{};

// 	MVector GetLocation() {return MVector(FnTransform.rotatePivot(MSpace::kWorld));}
// };



class Ik2bSolver : public MPxNode
{
public:
	// Public Data
	static const MString typeName;
	static const MTypeId typeId;

	// Node's Input Attributes
	static Attribute inFkStartAttr;
	static Attribute inFkMidAttr;
	static Attribute inFkEndAttr;
	static Attribute inIkHandleAttr;
	static Attribute inPoleVectorAttr;
	static Attribute inTwistAttr;
	static MObject inSoftnessAttr;
	static MObject inFkIkAttr;
	static MObject AttrInTime;
	// Nodes's Output Attributes
	static Attribute AttrOutUpdateX;
	static Attribute AttrOutUpdateY;
	static Attribute AttrOutUpdateZ;
	static Attribute AttrOutUpdate;

	bool bIsPoleVectorConnected;

	// Constructors
	Ik2bSolver()
		: MPxNode()
		, bIsPoleVectorConnected(false)
		, LimbLength(0.0)
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
	double softenEdge(double hardEdge, double chainLength, double dsoft);
	double softenIk(double startIkLen, double startMidLen, double midEndLen, double startMidEndLen, double softness);
	MObject getSourceObjFromPlug(const MObject& Object, const MObject& Plug);


	double GetLimbLength();
	bool TimeChanged(MAnimControl& AnimCtrl, MTime& TimeCached, MTime& TimeCurrent);
	MVector GetPoleVectorPosition(MVector& PosStart, MVector& PosMid, MVector& PosEnd);
	void BlendFkIk();

	void GetFkTransforms();
	void GetIkTransforms();

	MStatus solve(MDagPathArray& InOutLinks);
	bool SolveLimb(MDagPathArray& InOutLinks);
	void SolveFk();
	void SolveBlendedIk();
	void SolveIk();
	void SolveStraightLimb();
	void SolveTwoBoneIk();

	MStatus parseDataBlock(MDataBlock& dataBlock, MDagPathArray& InOutLinks);
	MStatus updateOutput(const MPlug& plug, MDataBlock& dataBlock);

private:
	// Private data
	MObject SelfObj;
	MSelectionList SelListTemp;

	// Function sets
	MFnTransform FnFkStart;
	MFnTransform FnFkMid;
	MFnTransform FnFkEnd;
	MFnTransform FnIkHandle;
	MFnTransform FnPoleVector;

	// Position
	// Fk
	MVector PosFkStart;
	MVector PosFkMid;
	MVector PosFkEnd;
	MVector PosFkHandle;
	MVector PosFkPoleVector;

	// Ik
	MVector PosIkStart;
	MVector PosIkMid;
	MVector PosIkEnd;
	MVector PosIkHandle;
	MVector PosIkPoleVector;

	// Out
	MVector PosOutStart;
	MVector PosOutMid;
	MVector PosOutEnd;
	MVector PosOutHandle;
	MVector PosOutPoleVector;

	// Quats
	// Fk
	MQuaternion QuatFkStart;
	MQuaternion QuatFkMid;
	MQuaternion QuatFkEnd;
	// Ik
	MQuaternion QuatIkStart;
	MQuaternion QuatIkMid;
	MQuaternion QuatIkEnd;
	MQuaternion QuatIkHandle;

	// Out
	MQuaternion QuatOutStart;
	MQuaternion QuatOutMid;
	MQuaternion QuatOutEnd;
	MQuaternion QuatOutHandle;

	double LimbLength;
	double RootTargetDistance;

	double twist;
	double softness;
	double fkIk;

	MTime TimeCurrent;
	MTime TimeCached;
	// Helpers
	MSelectionList __selList;
	MAnimControl AnimCtrl;
};
