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

// Lunar
#include "../maya/api/LMAttribute.h"
#include "../maya/api/LMPlugin.h"
#include "../maya/api/Utils.h"




class FootRollSolver : public MPxNode {
public:
	// Node Data
	static const MString typeName;
	static const MTypeId typeId;

	// Node's Input Attributes
	static Attribute attrInAnkle;
	static Attribute attrInBall;
	static MObject attrInHeelX, attrInHeelY, attrInHeelZ, attrInHeel;
	static MObject attrInToeX, attrInToeY, attrInToeZ, attrInToe;
	
	static Attribute attrInRoll;
	static Attribute attrInBendLimitAngle;
	static Attribute attrInToeLimitAngle;
	static MObject attrInTime;
	
	// Nodes's Output Attributes
	static Attribute attrOutUpdateX, attrOutUpdateY, attrOutUpdateZ, attrOutUpdate;
	
	// In-data
	MMatrix matInAnkle, matInBall, matInToe;
	MVector posHeel, posToe;
	MAngle roll, bendLimitAngle, toeLimitAngle;
	MTime timeCurrent, timeCached;

	// Function sets
	MFnTransform fnAnkle;
	MFnTransform fnBall;
	// MFnTransform fnToe;

	MObject objSelf;

	// Constructors
	FootRollSolver()
		: MPxNode()
		, posHeel(MVector::one)
	{};
	// Destructors
	~FootRollSolver() override {};

	// Public methods - overrides
	static void* creator() {return new FootRollSolver();}
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

	MStatus parseDataBlock(MDataBlock& dataBlock);
	MStatus solve();
	MStatus updateOutput(const MPlug& plug, MDataBlock& dataBlock);
};
