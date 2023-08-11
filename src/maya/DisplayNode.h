#pragma once

// System Includes
#include <string>
#include <sstream>
#include <cassert>

// Maya General Includes
#include <maya/MGlobal.h>
#include <maya/MCallbackIdArray.h>
#include <maya/MSceneMessage.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MPlug.h>
#include <maya/MPoint.h>
#include <maya/MDataHandle.h>w
#include <maya/MAnimControl.h>
#include <maya/MDrawRegistry.h>
#include <maya/MStringArray.h>

// Function Sets
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnData.h>
#include <maya/MFnDagNode.h>

// Iterators

// Viewport 2.0 Includes
#include <maya/MDrawRegistry.h>
#include <maya/MUserData.h>

// Proxies
#include <maya/MPxLocatorNode.h>
#include <maya/MPxDrawOverride.h>

// Custom
#include "api/Utils.h"
#include "api/LMAttribute.h"




// Node
class DisplayNode : public MPxNode {
public:
	// Node Data
	static const MString typeName;
	static const MTypeId typeId;
	static const MString drawDbClassification;
	static const MString drawRegistrationId;

	// // Node's Input Attributes
	// static MObject attrInMetaData;
	// static MObject attrInText;
	// static MObject attrInDisplayInViewport;

	// static MObject AttrTextPositionX;
	// static MObject AttrTextPositionY;
	// static MObject AttrTextSize;
	// static MObject AttrTextColor;
	// // Nodes's Output Attributes
	// static MObject AttrOutUpdate;

	// MObject SelfObj;

	// Constructors
	DisplayNode()
		: MPxNode()
	{};
	// Destructors
	~DisplayNode() override {};

	// Public methods - overrides
	static void* creator() {return new DisplayNode();}
	static MStatus initialize() {return MS::kSuccess;};
	// void getCacheSetup(
	// 	const MEvaluationNode& evalNode,
	// 	MNodeCacheDisablingInfo& disablingInfo,
	// 	MNodeCacheSetupInfo& cacheSetupInfo,
	// 	MObjectArray& monitoredAttributes
	// ) const override;
	// void postConstructor() override;
	// SchedulingType schedulingType() const override {return SchedulingType::kParallel;}
};



// User data
class DisplayNodeData : public MUserData {
public:

	// MPlug arrayMetaData;
	// unsigned int countMetaData;
	
	// std::vector<MString> vectorText;

	// MPoint TextPosition;
	// int TextSize;
	// MColor TextColor;

	// Constructors
	DisplayNodeData() 
		: MUserData()
	{};  // Don't delete after draw
	// Destructor
	virtual ~DisplayNodeData() override {};

	// void getText(const MObject& obj);
};



// Draw override
class DisplayNodeDrawOverride : public MHWRender::MPxDrawOverride {
public:
	// Constructors
	DisplayNodeDrawOverride(const MObject& Object)
		: MHWRender::MPxDrawOverride(Object, nullptr)
	{};
	// Destructors
	virtual ~DisplayNodeDrawOverride() override {};

	static MHWRender::MPxDrawOverride* creator(const MObject& Object) {return new DisplayNodeDrawOverride(Object);}
	virtual MHWRender::DrawAPI supportedDrawAPIs() const override {return MHWRender::kAllDevices;}
	virtual bool hasUIDrawables() const override {return true;}
	virtual void addUIDrawables(
		const MDagPath& objPath,
		MHWRender::MUIDrawManager& drawManager, 
		const MHWRender::MFrameContext& frameContext,
		const MUserData* data
	) override;
	virtual MUserData* prepareForDraw(
		const MDagPath& objPath,
		const MDagPath& cameraPath,
		const MHWRender::MFrameContext& frameContext,
		MUserData* oldData
	) override ;
};
