#pragma once

// #include "MathUtility.h"

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
#include "Utils.h"




class FootRollNode : public MPxNode
{
public:
	// Node Data
	static const MString typeName;
	static const MTypeId typeId;

	// Node's Input Attributes
	static MObject attrInHeel;
	static Attribute attrInBall;
	static Attribute attrInToe;
	static Attribute attrInAnkle;

	static Attribute attrInRoll;
	static Attribute attrInBendLimitAngle;
	static Attribute attrInToeLimitAngle;

	static MObject attrInTime;
	// Nodes's Output Attributes
	static Attribute attrOutUpdateX;
	static Attribute attrOutUpdateY;
	static Attribute attrOutUpdateZ;
	static Attribute attrOutUpdate;

	MVector posHeel;
	double roll;
	double bendLimitAngle;
	double toeLimitAngle;

	// Function sets
	// MFnTransform fnHeel;
	MFnTransform fnBall;
	MFnTransform fnToe;
	MFnTransform fnAnkle;

	MObject objSelf;

	// Constructors
	FootRollNode()
		: MPxNode()
		, posHeel(MVector::one)
	{};
	// Destructors
	~FootRollNode() override {};

	// Public methods - overrides
	static void* creator() {return new FootRollNode();}
	static MStatus initialize();
	bool isPassiveOutput(const MPlug& plug)	const override;
	virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock) override;
	MStatus setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) override;
	void getCacheSetup(
		const MEvaluationNode& evalNode,
		MNodeCacheDisablingInfo& disablingInfo,
		MNodeCacheSetupInfo& cacheSetupInfo,
		MObjectArray& monitoredAttributes
	) const override;
	void postConstructor() override;
	SchedulingType schedulingType() const override {return SchedulingType::kParallel;}

	MObject getSourceObjFromPlug(const MObject& object, const MObject& plug);

	MStatus parseDataBlock(MDataBlock& dataBlock);
	MStatus solve();
	MStatus updateOutput(const MPlug& plug, MDataBlock& dataBlock);
};
